import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { CookieService } from 'ngx-cookie-service'; 

import { LogService } from './log.service';
import { ContextService } from './context.service';
import { User } from '../models/user';
import { Status } from '../models/status';
import { SIN } from '../models/sin';

@Injectable({
  providedIn: 'root'
})
export class SinService {

  private class_name : String = "SinService";

  constructor(private http: HttpClient,
                private context: ContextService,
                private cookie: CookieService,
                private logger: LogService) { }


  public postSIN(sin : SIN): Observable<SIN>{
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    };
    return this.http.post<SIN>(this.context.postSINUrl().toString(), sin, httpOptions).pipe( 
                      tap( () => { this.logger.log( "Posting SIN", `${this.class_name}.postSIN`);}),
                      catchError(this.handleError('postSIN', sin))
                      );
  }

  public getSINs(): Observable<SIN[]>{
    return this.http.get<SIN[]>(this.context.getSINsUrl().toString()).pipe( 
                    tap(()=>{ this.logger.log( "Retrieving All SINs", `${this.class_name}.getSINs`);}),
                    catchError(this.handleError('getSINs', []))
                    );
  }

  public getUserSINs(user : User): Observable<SIN[]>{
    let user_url = this.context.getSINByEmailUrl(user.email).toString()
    return this.http.get<SIN[]>(this.context.getSINByEmailUrl(user.email).toString()).pipe(
                      tap( () => { this.logger.log(`Fetching All SINs From ${user.email}`, `${this.class_name}.getUserSINs`)}),
                      catchError(this.handleError('getUserSINS',[]))
                      );
  }

  public getStatusSINs(id: number){
    return this.http.get<SIN[]>(this.context.getSINByStatusUrl(id).toString()).pipe(
                      tap( () => { this.logger.log(`Fetching All SINs With Status ID #${id}`, 
                                                    `${this.class_name}.getStatusSINs`)}),
                      catchError(this.handleError('getStatusSINS',[]))
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
