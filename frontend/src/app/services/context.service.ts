import { Injectable } from '@angular/core';

const LOCAL: number = 0
const CLOUD: number = 1

@Injectable({
  providedIn: 'root'
})
export class ContextService {

  BASE_URL = "https://sinwebapp.app.cloud/gov"
  USER_ENDPOINT = "api/user"

  constructor() { }

  getUserUrl() : String {
    return `${this.BASE_URL}/${this.USER_ENDPOINT}`
  }
}
