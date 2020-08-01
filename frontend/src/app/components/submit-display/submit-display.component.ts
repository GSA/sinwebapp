import { Component, OnInit } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { SIN } from 'src/app/models/sin';
import { LogService } from 'src/app/services/log.service';

@Component({
  selector: 'app-submit-display',
  templateUrl: './submit-display.component.html'
})
export class SubmitDisplayComponent implements OnInit {

  private class_name = "SubmitDisplayComponent"
  public submit_SIN : SIN = {
    sin_number: null,
    status_id: null,
    user_id: null
  };

  public submitted : boolean = false;

  constructor(private sin: SinService,
              private logger: LogService) { }

  ngOnInit() { 
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.submit_SIN; 
  }

  public submitSIN(): void{
    this.sin.postSIN(this.submit_SIN).subscribe((response)=>{
      this.logger.log('SIN Posted', `${this.class_name}.submitSIN`)
      this.submit_SIN = { sin_number: null, status_id: null, user_id: null }
      this.submitted = true;
    })
  }
  
  public clear(){
    this.submitted = false;
  }
}
