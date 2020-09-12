import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormGroup } from '@angular/forms'
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { LogService } from './log.service';
import { ContextService } from './context.service';



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

    return this.http.post<FormData>(this.context.getFileUploadUrl(), formData).pipe( 
      tap( () => { this.logger.log( "Posting SIN", `${this.class_name}.postSIN`);}),
      catchError(this.handleError('postSIN'))
    );
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      console.log(`${operation} failed: ${error.message}`);
      return of(result as T);
    };
  }
   
}
