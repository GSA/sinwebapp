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
    return `${Context.USER_ENDPOINT}`
  }

  public getSINUserUrl(id: Number): String{
    return `${Context.SIN_USER_ENDPOINT}?${Context.SIN_USER_PARAM_ID}=${id}`
  }

  public postSINUrl() : String {
    return `${Context.SIN_ENDPOINT}/`
  }

  public getSINUrl(): String{
    return `${Context.SIN_ENDPOINT}`;
  }

  public getSINByEmailUrl(email: String): String {
    return `${Context.SIN_ENDPOINT}?${Context.SIN_PARAM_EMAIL}=${email}`
  }

  public getSINByStatusUrl(status: Number){
    return `${Context.SIN_ENDPOINT}?${Context.SIN_PARAM_STATUS}=${status}`
  }

  public getSINsUrl(): String {
    return `${Context.SINS_ENDPOINT}`
  }

}
