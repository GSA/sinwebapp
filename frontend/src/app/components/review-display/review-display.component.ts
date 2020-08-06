import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { LogService } from 'src/app/services/log.service';
import { SIN, null_SIN } from 'src/app/models/sin';
import { STATUS_STATE, Status } from '../../models/status'
import { User } from 'src/app/models/user';
import { StatusService } from 'src/app/services/status.service';

@Component({
  selector: 'app-review-display',
  templateUrl: './review-display.component.html'
})
export class ReviewDisplayComponent implements OnInit {

  private class_name = "ReviewDisplayComponent"
  public sin_list : SIN[];
  public user_lookup: boolean[] = [];
  public loaded_lookup: boolean[] = [];

  public selected_SIN: SIN = null_SIN;
  public status_lookup: Status[] = [];
  @Output() selection_event = new EventEmitter<SIN>();
  // review and approve functionality are similar, so 
  // reuse component with flag to differentiate behavior
  @Input() approver: boolean;
  @Input() user: User;

  constructor(private sinService: SinService,
              private statusService: StatusService,
              private logger: LogService) { }

  ngOnInit() {
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadSINs();
    this.statusService.getStatuses().subscribe( (statuses) => {
      this.status_lookup = statuses;
    })
  }

  private loadSINs(): void{
    this.sinService.getSINs().subscribe(sins => {
      this.logger.log('SINs Retrieved', `${this.class_name}.loadSINs`)
      this.sin_list=sins;
      this.logger.log('Initializing Component Controls', `${this.class_name}.loadSINs`)
      for(let sin of sins){ 
        if(sin.status_id == STATUS_STATE.submitted){ 
          this.user_lookup.push(false); 
          this.loaded_lookup.push(false);
        }
        else{ 
          this.user_lookup.push(true); 
          this.loaded_lookup.push(true);
        }
        this.logger.log(`Component Controls For # ${sin.sin_number} Initialized`, 
                          `${this.class_name}.loadSINs`)
      }
    })
  }

  public change(i: number): void{
    this.logger.log(`Component Control For # ${this.sin_list[i].sin_number} Changed`, 
                      `${this.class_name}.loadSINs`)
    this.user_lookup[i] = !this.user_lookup[i];
  }

  public selectSIN(sin: SIN){
    this.logger.log(`Selecting SIN: # ${sin.sin_number}`, `${this.class_name}.selectSIN`)
    this.selected_SIN = sin;
    this.logger.log(`Emitting Selection Event`, `${this.class_name}.selectSIN`)
    this.selection_event.emit(sin);
  }

  public submitChanges(i: number): void{
    // todo: post changes to database
    // then set loaded_lookup = user_lookup
  }

}
