import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LogService {

  public now: Date = new Date();
  public logue : String[] = [];

  constructor() { }

  public log(msg: String, location: String){
    this.logue.push(`${location}: ${msg}`)
    console.log(`${location}: ${msg}`)
  }

  public getLog(): String[] { return this.logue; }
}
