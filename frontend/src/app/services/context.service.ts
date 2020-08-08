import { Injectable } from '@angular/core';
import { Context } from './context';
import { environment } from '../../environments/environment'

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

  public getUsersUrl(ids: number[]): String{
    let url_builder = `${Context.USERS_ENDPOINT}?`;
    let index = 1;
    for(let id of ids){
      url_builder = url_builder.concat(`${Context.USERS_PARAM_ID}=${id}`)
      if (index < ids.length){
        url_builder = url_builder.concat('&')
        index++;
      }
    }
    return url_builder;
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

  public updateSINUrl(): String{
    return `${Context.SIN_UPDATE_ENDPOINT}`
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

  public getStatusUrl(id: Number): String{
    return `${Context.STATUS_ENDPOINT}?${Context.STATUS_PARAM_ID}=${id}`
  }

  public getStatusesUrl(): String{
    return `${Context.STATUSES_ENDPOINT}`
  }
}
