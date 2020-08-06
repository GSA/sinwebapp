import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { SIN, null_SIN } from 'src/app/models/sin';
import { LogService } from 'src/app/services/log.service';
import { User } from 'src/app/models/user';



@Component({
  selector: 'app-submit-display',
  templateUrl: './submit-display.component.html'
})
export class SubmitDisplayComponent implements OnInit {

  private class_name = "SubmitDisplayComponent"

  // true = submit mode, false = status mode
  public whichMode : boolean = false;
  public submit_SIN : SIN = null_SIN;
  public selected_SIN: SIN = null_SIN;
  public user_SINs: SIN[] =[];
  @Input() 
  public user: User;
  @Output() 
  public selection_event = new EventEmitter<SIN>();


  constructor(private sin: SinService,
              private logger: LogService) { }

  ngOnInit() { 
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadUserSINs();
  }

  public submitSIN(): void{
    this.logger.log('Submitting SIN', `${this.class_name}.submitSIN`)
    this.sin.postSIN(this.submit_SIN).subscribe((response)=>{
      this.logger.log('SIN Submitted', `${this.class_name}.submitSIN`)
      this.submit_SIN = null_SIN;
      this.switchModes();
    })
  }

  public loadUserSINs(): void{
    this.logger.log('Loading User SINs', `${this.class_name}.loadUserSINs`)
    this.sin.getUserSINs(this.user).subscribe( (sins)=>{
      this.logger.log('User SINS Loaded', `${this.class_name}.loadUserSINs`)
      this.user_SINs = sins;
    })
  }
  
  public switchModes(): void{
    this.logger.log('Switching Modes', `${this.class_name}.switchModes`)
    this.whichMode = !this.whichMode;
    if(!this.whichMode){ 
      this.logger.log('Status Mode Activated', `${this.class_name}.switchModes`)
      this.loadUserSINs();
    }
    else{ 
      this.logger.log('Submission Mode Activated', `${this.class_name}.switchModes`)
      this.submit_SIN = null_SIN;
    }
  }

  public selectSIN(sin: SIN){
    this.logger.log(`Selecting SIN: # ${sin.sin_number}`, `${this.class_name}.selectSIN`)
    this.selected_SIN = sin;
    this.selection_event.emit(sin);
  }
  
}
