import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { User } from '../models/user';
import { ContextService } from './context.service';
import { catchError, map, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient,
              private context: ContextService) { }

  public getUser() : Observable<User> {
    return this.http.get<User[]>(this.context.getUserUrl().toString()).pipe(
            map(res=> res[0]),
            catchError(this.handleError<User>("getUser"))
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