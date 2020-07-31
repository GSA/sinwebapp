import { Component, OnInit } from '@angular/core';
import { environment } from '../../../environments/environment'
import { LogService } from 'src/app/services/log.service';

@Component({
  selector: 'app-logger',
  templateUrl: './logger.component.html'
})
export class LoggerComponent implements OnInit {

  public debug : boolean = environment.debug;
  public display: boolean = false;
  public log : String[];

  constructor(private logger: LogService) { }

  ngOnInit() {
    this.getLogs()
  }

  private getLogs(): void{
   this.log = this.logger.getLogs();
  }

}
