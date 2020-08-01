import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LogService {

  public now: Date;
  public logue : String[] = [];

  constructor() { }

  public log(msg: String, location: String){
    let now = new Date().toLocaleTimeString()
    this.logue.push(`${now}: ${location}: ${msg}`)
    console.log(`${now}: ${location}: ${msg}`)
  }

  public getLogs(): String[] { return this.logue; }
}
