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
  public buffer_SIN: SIN = null_SIN;

  public status_lookup: Status[];
  
  constructor(private logger: LogService,
              private statusService: StatusService) { }

  ngOnInit() {
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadComponentData();
  }

  private loadComponentData(){
    this.statusService.getStatuses().subscribe((statuses)=>{
      this.logger.log('Retrieved Statuses', `${this.class_name}.loadComponentData`)
      this.status_lookup = statuses;
    })
  }

  public cancel(): void {
    this.logger.log('Emitting Cancel Event', `${this.class_name}.cancel`)
    this.cancel_event.emit("cancel")
  }

  public save(): void {
    this.logger.log(`Emitting Save Event for SIN # ${this.edit_SIN.sin_number}`, `${this.class_name}.save`)
    this.save_event.emit(this.edit_SIN)
  }
}
