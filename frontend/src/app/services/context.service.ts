import { Injectable } from '@angular/core';
import { Context } from './context';
import { environment } from '../../environments/environment'

@Injectable({
  providedIn: 'root'
})
export class ContextService {

  constructor() { }

  private getBackEndUrlBase() : string {
    if (environment.production){ return `${Context.CLOUD_URL}` }
    else{ return `${Context.LOCAL_URL}`}
  }

  public getUserUrl() : string {
    return `${Context.USER_ENDPOINT}`
  }

  public getUsersUrl(ids: number[]): string{
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

  public getSINUserUrl(id: Number): string{
    return `${Context.SIN_USER_ENDPOINT}?${Context.SIN_USER_PARAM_ID}=${id}`
  }

  public postSINUrl() : string {
    return `${Context.SIN_ENDPOINT}/`
  }

  public getSINUrl(): string{
    return `${Context.SIN_ENDPOINT}`;
  }

  public updateSINUrl(): string{
    return `${Context.SIN_UPDATE_ENDPOINT}/`
  }

  public getSINByEmailUrl(email: string): String {
    return `${Context.SIN_ENDPOINT}?${Context.SIN_PARAM_EMAIL}=${email}`
  }

  public getSINByStatusUrl(status: number){
    return `${Context.SIN_ENDPOINT}?${Context.SIN_PARAM_STATUS}=${status}`
  }

  public getSINsUrl(): string {
    return `${Context.SINS_ENDPOINT}`
  }

  public getStatusUrl(id: Number): string{
    return `${Context.STATUS_ENDPOINT}?${Context.STATUS_PARAM_ID}=${id}`
  }

  public getStatusesUrl(): string{
    return `${Context.STATUSES_ENDPOINT}`
  }

  public getPermittedStatusesUrl(): string{
    return `${Context.USER_STATUS_ENDPOINT}`
  }

  public getFileUploadUrl(): string{
    return `${Context.FILE_UPLOAD_ENDPOINT}/`
  }

  public getFileDownloadUrl(sin: string): string{
    return `${Context.FILE_DOWNLOAD_ENDPOINT}?${Context.FILE_DOWNLOAD_PARAM_SIN}=${sin}`
  }

  public getAllFileListUrl(): string{
    return `${Context.FILE_LIST_ENDPOINT}`
  }

  public getSINFileListUrl(sin: string): string{
    return `${Context.FILE_LIST_ENDPOINT}?${Context.FILE_LIST_PARAM_SIN}=${sin}`
  }
}
