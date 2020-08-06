import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LogService } from './log.service';
import { ContextService } from './context.service';
import { Status } from '../models/status';
import { Observable, of } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class StatusService {

  private class_name : String = "StatusService";
  
  constructor(private http: HttpClient,
              private context: ContextService,
              private logger: LogService) { }

  public getStatus(id: Number): Observable<Status>{
    return this.http.get<Status>(this.context.getStatusUrl(id).toString()).pipe(
                      tap(()=>{ this.logger.log('Retrieving Status', `${this.class_name}.getStatus`)}),
                      catchError(this.handleError('postSIN', null))
    );
  }

  public getStatuses():Observable<Status[]>{
    return this.http.get<Status[]>(this.context.getStatusesUrl().toString()).pipe(
                      tap(()=> { this.logger.log('Retrieving All Statuses', `${this.class_name}.getStatuses`)}),
                      catchError(this.handleError('getStatuses', []))
    )
  }
  
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      console.log(`${operation} failed: ${error.message}`);
      return of(result as T);
    };
  }
}
