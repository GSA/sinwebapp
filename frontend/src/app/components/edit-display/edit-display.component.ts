import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { SIN, null_SIN } from 'src/app/models/sin';
import { LogService } from 'src/app/services/log.service';
import { Status } from 'src/app/models/status';
import { StatusService } from 'src/app/services/status.service';

@Component({
  selector: 'app-edit-display',
  templateUrl: './edit-display.component.html'
})
export class EditDisplayComponent implements OnInit {
  
  private class_name = "EditDisplayComponent";

  @Output() public cancel_event = new EventEmitter<String>();
  @Output() public save_event = new EventEmitter<SIN>();
  @Input() public edit_SIN : SIN;
  @Input() public user_group: string[];

  public undo_SIN: SIN = null_SIN;
  public buffer_SIN: SIN = null_SIN;
  public applied_SIN : boolean = false;
  public applied_Status: boolean = false;
  public status_lookup: Status[];
  
  constructor(private logger: LogService,
              private statusService: StatusService) { }

  ngOnInit() {
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadComponentData();
  }

  private loadComponentData(){
    // Load undo_SIN field by field since Typescript objects are 
    // assigned by reference and undo_SIN needs to be a distinct 
    // copy of edit_SIN in order for component to function properly.
    this.undo_SIN.id = this.edit_SIN.id;
    this.undo_SIN.sin_number = this.edit_SIN.sin_number;
    this.undo_SIN.status_id = this.edit_SIN.status_id;
    this.undo_SIN.user_id = this.edit_SIN.user_id;
    this.statusService.getStatuses().subscribe((statuses)=>{
      this.logger.log('Retrieved Statuses', `${this.class_name}.loadComponentData`)
      this.status_lookup = statuses;
    })
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
                      `${this.class_name}.applySIN`)
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
    this.logger.log(`Emitting Save Event for SIN # ${this.edit_SIN.sin_number}`, `${this.class_name}.save`)
    this.save_event.emit(this.edit_SIN)
  }
}
