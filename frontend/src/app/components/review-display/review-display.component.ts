import { Component, OnInit, Input, EventEmitter, Output, SimpleChanges } from '@angular/core';
import { SIN } from 'src/app/models/sin';
import { Status } from '../../models/status'
import { User } from 'src/app/models/user';
import { StatusService } from 'src/app/services/status.service';
import { UserService } from 'src/app/services/user.service';
import { SinService } from 'src/app/services/sin.service';
import { LogService } from 'src/app/services/log.service';

// ReviewDisplayComponent
// 
//  Implemented Hierarchy : App -> UserDisplay -> ReviewDisplay
//  
//  ReviewDisplayComponent is a child of the UserDisplayComponent. It 
//  receives information through input and passes information back to 
//  the parent through events the parent registers to listen to.
//
//  Description
//    
//  This component allows an authenticated user with valid group permissions
//  to view SIN submissions submitted by all users. This component consumes 
//  user input and passes up the parent component for further UI processing.
//
//  HTML Attribute Input: [user], [selectable], [save_message], [clear_switch]
//  
//  As input, this component requires the user authenticated with the current 
//  session, a boolean flag that determines whether or not the SINS displayed
//  will be selectable (i.e, clickable and highlightable), a boolean flag
//  that determines whether or not to display a save message to the user and
//  a boolean flag that will signal to the component to clear any highlighted
//  user selections anytime it changes value, true or false.
//  
//  In the application, the variable, save_message, signals to the child
//  component a save_event has occured in the parent component and an appropriate
//  message should be displayed on screen.
//
//  If thisUser is an object of type User, then
//
//        <app-review-display [user]="thisUser" [selectable]="true" 
//              [save_message]="true" [clear_switch]="true"></app-review-display>
//    
//    will create an HTML component binded to the Angular component defined in this
//    this class. 
//
//  Output Events
//
//   This component emits a selection_event. selection_events occur when the user
//   clicks on one of the SINs in the displayed list. If doThis(object: Object) is a 
//   method in the parent component, then you can listen to the save_event and cancel_event
//   with the following tag,
//
//        <app-review-display [user]="thisUser" [selectable]="true" [save_message]="true" 
//                      (selection_event)="doThis($event)"></app-review-display>
//
//    The case of a save_event, the event Object will contain the SIN object the user edited
//    and passed to the backend application for persisting in the database. A cancel_event 
//    will contain a null SIN.

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
                                sin_description1: null, sin_group_title: null };

  @Output() public selection_event = new EventEmitter<SIN>();
  @Input() public user: User;
  @Input() public selectable: boolean;
  @Input() public save_message: boolean;
  @Input() public clear_switch: boolean;
  
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
    if(changes.clear_switch !== undefined){ 
      this.selected_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description1: null, sin_group_title: null };
    }
  }
  private loadComponentData(): void{
    this.statusService.getStatuses().subscribe( (statuses) => {
      this.logger.log('Statuses Retrieved', `${this.class_name}.loadComponentData`)
      this.status_lookup = statuses;
    })
    
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
