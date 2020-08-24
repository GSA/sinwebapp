import { Component, OnInit, Input, EventEmitter, Output, SimpleChanges } from '@angular/core';
import { SIN } from 'src/app/models/sin';
import { Status } from '../../models/status'
import { User } from 'src/app/models/user';
import { StatusService } from 'src/app/services/status.service';
import { UserService } from 'src/app/services/user.service';
import { SinService } from 'src/app/services/sin.service';
import { LogService } from 'src/app/services/log.service';

@Component({
  selector: 'app-review-display',
  templateUrl: './review-display.component.html'
})
export class ReviewDisplayComponent implements OnInit {

  private class_name = "ReviewDisplayComponent"
  
  public sin_list : SIN[] = [];
  public user_lookup: User[] = [];
  public status_lookup: Status[] = [];
  public selected_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                                sin_description1: null, sin_description2: null, sin_group_title: null };

  @Output() public selection_event = new EventEmitter<SIN>();
  @Input() public user: User;
  @Input() public selectable: boolean;
  @Input() public save_message: boolean;
  
  constructor(private sinService: SinService,
              private statusService: StatusService,
              private userService: UserService,
              private logger: LogService) { }

  ngOnInit() {
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadComponentData();
  }

  ngOnChanges(changes: SimpleChanges){
    if(changes.selectable !== undefined){ this.loadComponentData(); }
  }
  private loadComponentData(): void{
    this.sinService.getSINs().subscribe(sins => {

      this.logger.log('SINs Retrieved', `${this.class_name}.loadComponentData`)
      this.sin_list=sins;
      let id_list : number[] = [];
      for(let sin of sins){ 
        if(!id_list.includes(sin.user_id)){ 
          this.logger.log(`Storing User ID: ${sin.user_id} from SIN # ${sin.sin_number}`, `${this.class_name}.loadComponentData`)
          id_list.push(sin.user_id); 
        }
      }

      for(let id of id_list){ this.logger.log(`Stored User ID: ${id}`, `${this.class_name}.loadComponentData`) }
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

  public lookupUserEmail(sin_id: Number){
    for(let user of this.user_lookup){
      if(user.id == sin_id){ return user.email; }
    }
  }
  public selectSIN(sin: SIN){
    this.logger.log(`Selecting SIN: # ${sin.sin_number}`, `${this.class_name}.selectSIN`)
    this.selected_SIN = sin;
    this.logger.log(`Emitting Selection Event`, `${this.class_name}.selectSIN`)
    this.selection_event.emit(sin);
  }

}
