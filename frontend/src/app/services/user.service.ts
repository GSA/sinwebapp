import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { User } from '../models/user';
import { ContextService } from './context.service';
import { catchError, map, tap } from 'rxjs/operators';
import { LogService } from './log.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private class_name: String = "UserService";

  constructor(private http: HttpClient,
              private context: ContextService,
              private logger: LogService) { }

  public getUser() : Observable<User> {
    return this.http.get<User>(this.context.getUserUrl().toString()).pipe(
            tap(()=>{ this.logger.log('Retrieving User', `${this.class_name}.getUser`); }),
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