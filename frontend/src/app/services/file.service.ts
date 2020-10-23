import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormGroup } from '@angular/forms'
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { LogService } from './log.service';
import { ContextService } from './context.service';
import { Attachment } from '../models/attachment';

const file_header = new HttpHeaders({'Content-Type':'application/pdf; charset=utf-8'});


@Injectable({
  providedIn: 'root'
})
export class FileService {

  private class_name : String = "FileService"

  constructor(private http: HttpClient,
              private context: ContextService,
              private logger: LogService) { }

  public uploadFile(form: FormGroup): Observable<any>{
    const formData = new FormData()
    formData.append('file', form.get('file').value)
    formData.append('sin_number', form.get('sin_number').value)
    
    return this.http.post<FormData>(this.context.getFileUploadUrl().toString(), formData).pipe( 
      tap( () => { this.logger.log( "Posting File Form", `${this.class_name}.uploadFiles`);}),
      catchError(this.handleError('uploadFile'))
    );
  }

  public getFileListForSIN(sin: string): Observable<Attachment[]>{
    let attachments : Attachment[];
    return this.http.get<Attachment[]>(this.context.getSINFileListUrl(sin).toString()).pipe(
      tap( ()=> {  this.logger.log( `Retrieving File List For SIN # ${sin} `, `${this.class_name}.getFileListForSIN`);}),
      catchError(this.handleError('getFileList', attachments))
    )
  }

  public downloadFile(sin){

  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      console.log(`${operation} failed: ${error.message}`);
      return of(result as T);
    };
  }
   
}
