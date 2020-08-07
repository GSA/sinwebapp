import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { LogService } from 'src/app/services/log.service';
import { SIN, null_SIN } from 'src/app/models/sin';
import { STATUS_STATE, Status } from '../../models/status'
import { User } from 'src/app/models/user';
import { StatusService } from 'src/app/services/status.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-review-display',
  templateUrl: './review-display.component.html'
})
export class ReviewDisplayComponent implements OnInit {

  private class_name = "ReviewDisplayComponent"
  
  @Output() selection_event = new EventEmitter<SIN>();
  @Input() approver: boolean;
  @Input() user: User;
  public sin_list : SIN[];
  public user_lookup: User[];
  public status_lookup: Status[];
  public selected_SIN: SIN = null_SIN;
  
  constructor(private sinService: SinService,
              private statusService: StatusService,
              private userService: UserService,
              private logger: LogService) { }

  ngOnInit() {
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadComponentData();
  }

  private loadComponentData(): void{
    this.sinService.getSINs().subscribe(sins => {
      this.logger.log('SINs Retrieved', `${this.class_name}.loadComponentData`)
      this.sin_list=sins;
      let id_list : Number[] = [];
      for(let sin of sins){ 
        this.logger.log(`Storing User ID: ${sin.user_id} from SIN # ${sin.sin_number}`, `${this.class_name}.loadComponentData`)
        id_list.push(sin.user_id);
      }
      this.userService.getUsers(id_list).subscribe( (users) => {
        this.logger.log('Users Retrieved', `${this.class_name}.loadComponentData`)
        this.user_lookup = users;
      })
    })
    this.statusService.getStatuses().subscribe( (statuses) => {
      this.logger.log('Statuses Retrieved', `${this.class_name}.loadComponentData`)
      this.status_lookup = statuses;
    })
  }

  public selectSIN(sin: SIN){
    this.logger.log(`Selecting SIN: # ${sin.sin_number}`, `${this.class_name}.selectSIN`)
    this.selected_SIN = sin;
    this.logger.log(`Emitting Selection Event`, `${this.class_name}.selectSIN`)
    this.selection_event.emit(sin);
  }

}
