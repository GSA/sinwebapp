import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { SIN } from 'src/app/models/sin';
import { GROUPS } from 'src/app/models/user';
import { Status } from 'src/app/models/status';
import { LogService } from 'src/app/services/log.service';
import { StatusService } from 'src/app/services/status.service';

@Component({
  selector: 'app-edit-display',
  templateUrl: './edit-display.component.html'
})
export class EditDisplayComponent implements OnInit {
  
  private class_name = "EditDisplayComponent";

  public edit_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description1: null, sin_group_title: null };
  public undo_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description1: null, sin_group_title: null };
  public buffer_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description1: null,  sin_group_title: null };
  public applied_SIN : boolean = false;
  public applied_Status: boolean = false;
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
    this.buffer_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                           sin_description1: null, sin_group_title: null };
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

  public undoSIN(): void{
    this.logger.log(`Resetting edit_SIN.sin_number = ${this.edit_SIN.sin_number} to ${this.undo_SIN.sin_number}`,
                      `${this.class_name}.undoSIN`)
    this.edit_SIN.sin_number = this.undo_SIN.sin_number;
    this.applied_SIN=false;
  }

  public undoStatus(): void{
    this.logger.log(`Resetting edit_SIN.status_id = ${this.edit_SIN.status_id} to ${this.undo_SIN.status_id}`,
                      `${this.class_name}.undoStatus`)
    this.edit_SIN.status_id = this.undo_SIN.status_id;
    this.applied_Status = false;
  }

  public saveAll(): void {
    this.logger.log(`Emitting Save Event for SIN # ${this.edit_SIN.sin_number}`, `${this.class_name}.saveAll`)
    this.save_event.emit(this.edit_SIN)
  }
}
