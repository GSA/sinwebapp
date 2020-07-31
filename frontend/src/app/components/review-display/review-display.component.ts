import { Component, OnInit, Input } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { LogService } from 'src/app/services/log.service';
import { SIN } from 'src/app/models/sin';

@Component({
  selector: 'app-review-display',
  templateUrl: './review-display.component.html'
})
export class ReviewDisplayComponent implements OnInit {

  public sin_list : SIN[];

  // review and approve functionality are similar, so 
  // reuse component with flag to differentiate behavior
  @Input() approver: boolean;

  constructor(private sin: SinService,
              private logger: LogService) { }

  ngOnInit() {
    this.loadSINs();
  }

  private loadSINs(): void{
    this.sin.getSINs().subscribe(sins => {
      this.sin_list=sins;
    })
  }

}
