import { Injectable } from '@angular/core';
import { Context } from './context';
import { environment } from '../../environments/environment'

@Injectable({
  providedIn: 'root'
})
export class ContextService {

  constructor() { }

  private getBackEndUrlBase() : string {
    if (environment.development){ return `${Context.DEV_HOST}` }
    else{ return ''}
  }

  public getUserUrl() : string {
    return `${this.getBackEndUrlBase()}/${Context.USER_ENDPOINT}`
  }

  public getUsersUrl(ids: number[]): string{
    let url_builder = `${this.getBackEndUrlBase()}/${Context.USERS_ENDPOINT}?`;
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
    return `${this.getBackEndUrlBase()}/${Context.SIN_USER_ENDPOINT}?${Context.SIN_USER_PARAM_ID}=${id}`
  }

  public postSINUrl() : string {
    return `${this.getBackEndUrlBase()}/${Context.SIN_ENDPOINT}/`
  }

  public getSINUrl(): string{
    return `${this.getBackEndUrlBase()}/${Context.SIN_ENDPOINT}`;
  }

  public updateSINUrl(): string{
    return `${this.getBackEndUrlBase()}/${Context.SIN_UPDATE_ENDPOINT}/`
  }

  public getSINByEmailUrl(email: string): String {
    return `${this.getBackEndUrlBase()}/${Context.SIN_ENDPOINT}?${Context.SIN_PARAM_EMAIL}=${email}`
  }

  public getSINByStatusUrl(status: number){
    return `${this.getBackEndUrlBase()}/${Context.SIN_ENDPOINT}?${Context.SIN_PARAM_STATUS}=${status}`
  }

  public getSINsUrl(): string {
    return `${this.getBackEndUrlBase()}/${Context.SINS_ENDPOINT}`
  }

  public getStatusUrl(id: Number): string{
    return `${this.getBackEndUrlBase()}/${Context.STATUS_ENDPOINT}?${Context.STATUS_PARAM_ID}=${id}`
  }

  public getStatusesUrl(): string{
    return `${this.getBackEndUrlBase()}/${Context.STATUSES_ENDPOINT}`
  }

  public getPermittedStatusesUrl(): string{
    return `${this.getBackEndUrlBase()}/${Context.USER_STATUS_ENDPOINT}`
  }

  public getGroupsUrl(): string{
    return `${this.getBackEndUrlBase()}/${Context.GROUPS_ENDPOINT}`
  }

  public getFileUploadUrl(): string{
    return `${this.getBackEndUrlBase()}/${Context.FILE_UPLOAD_ENDPOINT}/`
  }

  public getFileDownloadUrl(sin: string): string{
    return `${this.getBackEndUrlBase()}/${Context.FILE_DOWNLOAD_ENDPOINT}?${Context.FILE_DOWNLOAD_PARAM_SIN}=${sin}`
  }

  public getAllFileListUrl(): string{
    return `${this.getBackEndUrlBase()}/${Context.FILE_LIST_ENDPOINT}`
  }

  public getSINFileListUrl(sin: string): string{
    return `${this.getBackEndUrlBase()}/${Context.FILE_LIST_ENDPOINT}?${Context.FILE_LIST_PARAM_SIN}=${sin}`
  }
}
