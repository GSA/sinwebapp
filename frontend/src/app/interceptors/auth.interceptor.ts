import { Injectable } from '@angular/core';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest
} from '@angular/common/http';

import { Observable } from 'rxjs';
import { LogService } from '../services/log.service';

/** Inject With Credentials into the request */
@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  class_name = "AuthInterceptor"
  constructor(private logger: LogService){
    
  }
  intercept(req: HttpRequest<any>, next: HttpHandler):
    Observable<HttpEvent<any>> {
    
      this.logger.log(`Intercepting Request: ${req.url}`, `${this.class_name}.intercept`)
      this.logger.log(`Appending Django Credentials...`, `${this.class_name}.intercept`)
      req = req.clone({
        withCredentials: true
      });
      
      return next.handle(req);
  }
}