import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { User } from '../models/user';
import { ContextService } from './context.service';
import { catchError, map, tap } from 'rxjs/operators';
import { SIN } from '../models/sin';
import { LogService } from './log.service';


const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json',
  })
};

@Injectable({
  providedIn: 'root'
})
export class SinService {

  private class_name : String = "SinService";

  constructor(private http: HttpClient,
                private context: ContextService,
                private logger: LogService) { }


  public postSIN(sin : SIN): Observable<SIN>{
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

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      console.log(`${operation} failed: ${error.message}`);
      return of(result as T);
    };
  }
}
