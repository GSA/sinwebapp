import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { SIN } from 'src/app/models/sin';
import { GROUPS } from 'src/app/models/user';
import { Status } from 'src/app/models/status';
import { LogService } from 'src/app/services/log.service';
import { StatusService } from 'src/app/services/status.service';

// EditDisplayComponent
// 
//  Description
//    
//  This component allows an authenticated user with valid group permissions
//  to edit the fields on a SIN submission. This component consumes user input
//  and passes it onto backend for processing. Once it is done with the user,
//  it will emit an event signalling to the parent component what type of 
//  transaction has occured. See Output Events for more information.
//
//  HTML Attribute Input
//  
//  As input, This component requires a SIN to edit and the user permission group
//    associated with the user currently using the form. They must be specified in the
//    HTML inline. For example, if thisSIN and thisGroup were variables in another 
//    Angular component, then in that component's HTML template the following tag,
//
//        <app-edit-display [input_SIN]="thisSIN" [user_group] ></app-edit-display>
//    
//    will create an HTML component binded to the Angular component defined in this
//    this class. 
//
//  Output Events
//
//   This component emits two types of events: save_events and cancel_events. Save_events
//    occur when the user saves their edits. Cancel_events occur when the user wishes to 
//    exit editing without saving. These events can be captured by the parent Angular
//    component by binding a method to these events and injecting in the emitted $event.
//    If doThis(object: Object) and doThat(object: Object) are methods in the parent component, 
//    then you can listen to the save_event and cancel_event with the following tag,
//
//        <app-edit-display [input_SIN]="thisSIN" [user_group] ></app-edit-display
//                      (save_event)="doThis($event)" (cancel_event)="doThat($event)"></app-edit-display>
//
//    The case of a save_event, the event Object will contain the SIN object the user edited
//    and passed to the backend application for persisting in the database. A cancel_event
//    will contain a null SIN

@Component({
  selector: 'app-edit-display',
  templateUrl: './edit-display.component.html'
})
export class EditDisplayComponent implements OnInit {
  
  private class_name = "EditDisplayComponent";

  public edit_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description: null, sin_title: null };
  public undo_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description: null, sin_title: null };
  public buffer_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description: null,  sin_title: null };
  public applied_SIN : boolean = false;
  public applied_Status: boolean = false;
  public applied_Title: boolean = false;
  public applied_Description: boolean = false;
  public status_lookup: Status[] = [];
  public permission_status_lookup: Status[] = [];

  @Input() public input_SIN : SIN;
  @Input() public user_group: string[];
  @Output() public cancel_event = new EventEmitter<String>();
  @Output() public save_event = new EventEmitter<SIN>();
  
  constructor(private logger: LogService,
              private statusService: StatusService) { }

  ngOnInit() {
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadComponentData();
  }

  private loadComponentData(){
    this.edit_SIN = Object.assign(this.edit_SIN, this.input_SIN);
    this.undo_SIN = Object.assign(this.undo_SIN, this.edit_SIN)
    // TODO: Possibly want to initialize buffer_SIN = input_SIN to 
    // get rid of validation errors. i.e., the form needs input so 
    // it is valid.
    this.buffer_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                           sin_description: null, sin_title: null };
    if(this.user_group.includes(GROUPS.approver) || this.user_group.includes(GROUPS.reviewer) || this.user_group.includes(GROUPS.admin)){
      this.logger.log(`Retrieving Statues For Role ${this.user_group[0]}`, `${this.class_name}.loadComponentData`)
      this.statusService.getStatuses().subscribe((statuses)=>{
        this.logger.log('Retrieved Statuses', `${this.class_name}.loadComponentData`)
        this.status_lookup = statuses;
      });
      this.statusService.getUserStatuses().subscribe((user_statuses)=>{
        this.logger.log('Retrieved User Statuses', `${this.class_name}.loadComponentData`)
        this.permission_status_lookup = user_statuses;
      })
    }
  }

  public cancel(): void {
    this.logger.log('Emitting Cancel Event', `${this.class_name}.cancel`)
    this.cancel_event.emit("cancel")
  }

  public applySIN(): void{
    this.logger.log(`Converting edit_SIN.sin_number = ${this.edit_SIN.sin_number} to ${this.buffer_SIN.sin_number}`,
                      `${this.class_name}.applySIN`)
    this.edit_SIN.sin_number = this.buffer_SIN.sin_number;
    this.buffer_SIN.sin_number = null;
    this.applied_SIN = true;
  }

  public applyStatus(): void{
    this.logger.log(`Converting edit_SIN.status_id = ${this.edit_SIN.status_id} to ${this.buffer_SIN.status_id}`,
                      `${this.class_name}.applyStatus`)
    this.edit_SIN.status_id = this.buffer_SIN.status_id;
    this.buffer_SIN.status_id = null;
    this.applied_Status = true;
  }

  public applyTitle(): void{
    this.logger.log(`Converting edit_SIN.sin_title = ${this.edit_SIN.sin_title} to ${this.buffer_SIN.sin_title}`,
                      `${this.class_name}.applyTitle`)
    this.edit_SIN.sin_title = this.buffer_SIN.sin_title;
    this.buffer_SIN.sin_title = null;
    this.applied_Title = true;
  }

  public applyDescription(): void{
    this.logger.log(`Converting edit_SIN.sin_description = ${this.edit_SIN.sin_description} to ${this.buffer_SIN.sin_description}`,
                      `${this.class_name}.applyDescription`);
    this.edit_SIN.sin_description = this.buffer_SIN.sin_description;
    this.buffer_SIN.sin_description= null;
    this.applied_Description = true;
  }

  public undoSIN(): void{
    this.logger.log(`Resetting edit_SIN.sin_number = ${this.edit_SIN.sin_number} to ${this.undo_SIN.sin_number}`,
                      `${this.class_name}.undoSIN`);
    this.edit_SIN.sin_number = this.undo_SIN.sin_number;
    this.applied_SIN=false;
  }

  public undoStatus(): void{
    this.logger.log(`Resetting edit_SIN.status_id = ${this.edit_SIN.status_id} to ${this.undo_SIN.status_id}`,
                      `${this.class_name}.undoStatus`);
    this.edit_SIN.status_id = this.undo_SIN.status_id;
    this.applied_Status = false;
  }

  public undoTitle(): void{
    this.logger.log(`Resetting edit_SIN.sin_title = ${this.edit_SIN.sin_title} to ${this.undo_SIN.sin_title}`,
                      `${this.class_name}.undoTitle`);
    this.edit_SIN.sin_title = this.undo_SIN.sin_title;
    this.applied_Title = false;
  }

  public undoDescription(): void{
    this.logger.log(`Resetting edit_SIN.sin_description = ${this.edit_SIN.sin_description} to ${this.undo_SIN.sin_description}`,
                      `${this.class_name}.undoDescription`)
    this.edit_SIN.sin_description = this.undo_SIN.sin_description;
    this.applied_Description = false;
  }

  public saveAll(): void {
    this.logger.log(`Emitting Save Event for SIN # ${this.edit_SIN.sin_number}`, `${this.class_name}.saveAll`);
    this.save_event.emit(this.edit_SIN);
  }
}
