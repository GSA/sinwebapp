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

  private getBackEndUrlBase() : String {
    if (environment.production){ return `${Context.CLOUD_URL}` }
    else{ return `${Context.LOCAL_URL}`}
  }
  public getUserUrl() : String {
    return `${this.getBackEndUrlBase()}/${Context.USER_ENDPOINT}`
  }

  public getSINUrl() : String {
    return `${this.getBackEndUrlBase()}/${Context.SIN_ENDPOINT}`
  }

}
