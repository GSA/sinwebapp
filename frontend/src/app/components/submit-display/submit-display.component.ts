import { Component, OnInit, Input, Output, EventEmitter, SimpleChanges } from '@angular/core';
import { SIN } from 'src/app/models/sin';
import { User } from 'src/app/models/user';
import { Status } from 'src/app/models/status';
import { LogService } from 'src/app/services/log.service';
import { StatusService } from 'src/app/services/status.service';
import { SinService } from 'src/app/services/sin.service';

@Component({
  selector: 'app-submit-display',
  templateUrl: './submit-display.component.html'
})
export class SubmitDisplayComponent implements OnInit {

  private class_name = "SubmitDisplayComponent"

  public submit_mode : boolean = false;
  public exists : boolean;
  public submitted: boolean = false;
  public submit_SIN : SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                               sin_description1: null, sin_group_title: null };
  public selected_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                                sin_description1: null, sin_group_title: null };
  public existing_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                                sin_description1: null, sin_group_title: null };
  public user_SINs: SIN[] =[];
  public all_SINs: SIN[] =[]
  public status_lookup: Status[] = [];

  @Input() public user: User;
  @Input() public selectable: boolean; 
  @Input() public save_message: boolean;
  @Output() public selection_event = new EventEmitter<SIN>();

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

  public loadAllSINs(){
    this.logger.log('Loading All SINs',`${this.class_name}.loadAllSINs`);
    this.sinService.getSINs().subscribe( (sins) =>{
      this.logger.log('All SINs Loaded', `${this.class_name}.loadAllSINs`);
      this.all_SINs = sins;
    })
  }

  public loadUserSINs(): void{
    this.logger.log('Loading User SINs', `${this.class_name}.loadUserSINs`);
    this.sinService.getUserSINs(this.user).subscribe( (sins)=>{
      this.logger.log('User SINS Loaded', `${this.class_name}.loadUserSINs`);
      this.user_SINs = sins;
    })
  }
  public submitSIN(): void{
    if(!this.exists){
      this.logger.log('Submitting New SIN', `${this.class_name}.submitSIN`);
      this.sinService.postSIN(this.submit_SIN).subscribe((response)=>{
        this.logger.log('SIN Submitted', `${this.class_name}.submitSIN`);
        this.submit_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                              sin_description1: null, sin_group_title: null };
        this.submitted = true;
        this.switchModes(false);
      })
    }
    else{
      this.logger.log('Submitting Existing SIN', `${this.class_name}.submitSIN`);
      if(!this.submit_SIN.status_id) { this.submit_SIN.status_id = this.existing_SIN.status_id; };
      if(!this.submit_SIN.user_id) { this.submit_SIN.user_id = this.existing_SIN.user_id; };
      if(!this.submit_SIN.id) { this.submit_SIN.id = this.existing_SIN.id; };
      this.sinService.updateSIN(this.submit_SIN).subscribe((response)=>{
        this.submit_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
          sin_description1: null, sin_group_title: null };
          this.submitted = true;
          this.switchModes(false);
      });
    };
  }

  public clearMessage(): void {
    this.submitted = false;
  }
  
  public switchModes(exists: boolean): void{
    this.exists = exists;
    if(this.exists){ this.loadAllSINs(); }
    this.logger.log('Switching Modes', `${this.class_name}.switchModes`);
    this.submit_mode = !this.submit_mode;
    if(!this.submit_mode){ 
      this.logger.log('Status Mode Activated', `${this.class_name}.switchModes`);
      this.loadUserSINs();
    }
    else{ 
      if(this.exists){ this.logger.log('Submission Mode for Existing SINS Activated', `${this.class_name}.switchModes`);  }
      else {this.logger.log('Submission Mode for New SINs Activated', `${this.class_name}.switchModes`);  }
      this.submitted = false;
      // check if submit_SIN fields are null, set equal to selected_SIN if so
      this.submit_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description1: null, sin_group_title: null };
      this.selected_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description1: null, sin_group_title: null };
    }
  }

  public selectSIN(sin: SIN){
    this.logger.log(`Selecting SIN: # ${sin.sin_number}`, `${this.class_name}.selectSIN`);
    this.submitted = false;
    this.selected_SIN = sin;
    this.logger.log(`Emitting Selection Event`, `${this.class_name}.selectSIN`);
    this.selection_event.emit(sin);
  }

  public selectExistingSIN(sin: SIN){
    this.logger.log(`Selecting Pre-existing SIN to Edit: # ${sin.sin_number}`, `${this.class_name}.selectExistingSIN`);
    this.existing_SIN = sin;
  }
  
}
