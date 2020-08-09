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

  // returns an array Status[] for all available Status types.
  public getStatuses():Observable<Status[]>{
    return this.http.get<Status[]>(this.context.getStatusesUrl().toString()).pipe(
                      tap(()=> { this.logger.log('Retrieving All Statuses', `${this.class_name}.getStatuses`)}),
                      catchError(this.handleError('getStatuses', []))
    )
  }
  
  // returns an array Status[] for all user permissibile Status types, i.e.
  // a 'submitter' can only change the state of a SIN to 'submitted', so if 
  // the user signed in is a 'submitter', this method will return an array 
  // containing the status 'submitted'. If the user is a reviewer, the 
  // method will return an array containing the statuses 'subtmitted',
  // 'reviewed' and 'change', all the statuses accessible to the role of 
  // reviewer.
  public getUserStatuses(): Observable<Status[]>{
    return this.http.get<Status[]>(this.context.getPermittedStatusesUrl().toString()).pipe(
      tap(()=> { this.logger.log('Retrieving All Statuses', `${this.class_name}.getUserStatuses`)}),
      catchError(this.handleError('getUserStatuses', []))
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
