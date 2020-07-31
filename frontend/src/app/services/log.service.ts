import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LogService {

  public now: Date = new Date();
  public logue : String[] = [];

  constructor() { }

  public log(msg: String, location: String){
    let now = new Date().toLocaleTimeString()
    this.logue.push(`${now}: ${location}: ${msg}`)
    console.log(`${location}: ${msg}`)
  }

  public getLogs(): String[] { return this.logue; }
}
