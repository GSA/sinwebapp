import { Component, OnInit, Input, Output, EventEmitter, SimpleChanges } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { SIN, null_SIN } from 'src/app/models/sin';
import { LogService } from 'src/app/services/log.service';
import { User } from 'src/app/models/user';
import { Status } from 'src/app/models/status';
import { StatusService } from 'src/app/services/status.service';



@Component({
  selector: 'app-submit-display',
  templateUrl: './submit-display.component.html'
})
export class SubmitDisplayComponent implements OnInit {

  private class_name = "SubmitDisplayComponent"

  // true = submit mode, false = status mode
  public whichMode : boolean = false;
  public submitted: boolean = false;
  public submit_SIN : SIN = null_SIN;
  public selected_SIN: SIN = null_SIN;
  public user_SINs: SIN[] =[];
  public status_lookup: Status[] = [];
  @Input() 
  public user: User;
  @Input()
  public selectable: boolean; 
  @Input()
  public save_message: boolean;
  @Output() 
  public selection_event = new EventEmitter<SIN>();


  constructor(private sinService: SinService,
              private statusService: StatusService,
              private logger: LogService) { }

  ngOnInit() { 
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadUserSINs();
    this.statusService.getStatuses().subscribe( (statuses) => {
      this.status_lookup = statuses;
    })
  }

  ngOnChanges(changes: SimpleChanges){
    if(changes.selectable !== undefined){ this.loadUserSINs(); }
  }

  public submitSIN(): void{
    this.logger.log('Submitting SIN', `${this.class_name}.submitSIN`)
    this.sinService.postSIN(this.submit_SIN).subscribe((response)=>{
      this.logger.log('SIN Submitted', `${this.class_name}.submitSIN`)
      this.submit_SIN = null_SIN;
      this.submitted = true;
      this.switchModes();
    })
  }

  public clearMessage(): void {
    this.submitted = false;
  }

  public loadUserSINs(): void{
    this.logger.log('Loading User SINs', `${this.class_name}.loadUserSINs`)
    this.sinService.getUserSINs(this.user).subscribe( (sins)=>{
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
      this.submitted = false;
      this.submit_SIN = null_SIN;
      this.selected_SIN = null_SIN;
    }
  }

  public selectSIN(sin: SIN){
    this.logger.log(`Selecting SIN: # ${sin.sin_number}`, `${this.class_name}.selectSIN`)
    this.submitted = false;
    this.selected_SIN = sin;
    this.logger.log(`Emitting Selection Event`, `${this.class_name}.selectSIN`)
    this.selection_event.emit(sin);
  }
  
}
