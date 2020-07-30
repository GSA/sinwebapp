import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { User } from '../models/user';
import { ContextService } from './context.service';
import { catchError, map, tap } from 'rxjs/operators';
import { SIN } from '../models/sin';


const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json',
  })
};

@Injectable({
  providedIn: 'root'
})
export class SinService {

  constructor(private http: HttpClient,
                private context: ContextService) { }


  public postSIN(sin : SIN): Observable<SIN>{
    console.log("SinService.postSIN: Posting SIN...")
    return this.http.post<SIN>(this.context.getSINUrl().toString(), sin, httpOptions)
                      .pipe( catchError(this.handleError('postSIN', sin)));
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      console.log(`${operation} failed: ${error.message}`);
      return of(result as T);
    };
  }
}
