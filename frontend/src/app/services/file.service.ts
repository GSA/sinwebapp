import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup, FormData } from '@angular/forms'
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { LogService } from './log.service';



@Injectable({
  providedIn: 'root'
})
export class FileService {

  private class_name : String = "FileService"

  constructor(private http: HttpClient,
              private logger: LogService) { }

  public uploadFile(form: FormGroup): Observable{
    const formData = new FormData()
    formData.append('file', form.get('file').value)
    formData.append('sin_number', form.get('sin_number').value)

    this.http.post<FormData>('url goes here', formData).pipe( 
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
