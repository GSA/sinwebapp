import { Component, OnInit, Input } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { LogService } from 'src/app/services/log.service';
import { SIN } from 'src/app/models/sin';
import { STATUS_STATE } from '../../models/status'

@Component({
  selector: 'app-review-display',
  templateUrl: './review-display.component.html'
})
export class ReviewDisplayComponent implements OnInit {

  private class_name = "ReviewDisplayComponent"
  public sin_list : SIN[];
  public reviewed_lookup: boolean[] = [];
  public changed_lookup: boolean[] = [];

  // review and approve functionality are similar, so 
  // reuse component with flag to differentiate behavior
  @Input() approver: boolean;

  constructor(private sin: SinService,
              private logger: LogService) { }

  ngOnInit() {
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadSINs();
  }

  private loadSINs(): void{
    this.sin.getSINs().subscribe(sins => {
      this.logger.log('SINs Retrieved', `${this.class_name}.loadSINs`)
      this.sin_list=sins;
      this.logger.log('Initializing Component Controls', `${this.class_name}.loadSINs`)
      for(let sin of sins){ 
        this.changed_lookup.push(false);
        if(sin.status_id == STATUS_STATE.submitted){ this.reviewed_lookup.push(false); }
        else{ this.reviewed_lookup.push(true); }
        this.logger.log(`Component Controls For # ${sin.sin_number} Initialized`, 
                          `${this.class_name}.loadSINs`)
      }
    })
  }

  public change(i: number): void{
    this.logger.log(`Component Control For # ${this.sin_list[i].sin_number} Changed`, 
                      `${this.class_name}.loadSINs`)
    this.reviewed_lookup[i] = !this.reviewed_lookup[i];
    this.changed_lookup[i] = !this.changed_lookup[i];
  }

  public submitChanges(): void{
    // todo: post changes to database
  }

}
