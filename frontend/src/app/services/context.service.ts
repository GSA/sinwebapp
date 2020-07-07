import { Injectable } from '@angular/core';
import { Context } from './context';
import { environment } from '../../environments/environment'
const LOCAL: number = 0
const CLOUD: number = 1

@Injectable({
  providedIn: 'root'
})
export class ContextService {

  constructor() { }

  getUserUrl() : String {
    if (environment.production){
      return `${Context.CLOUD_URL}/${Context.USER_ENDPOINT}`
    }
    else{
      return `${Context.LOCAL_URL}/${Context.USER_ENDPOINT}`
    }
    
  }
}
