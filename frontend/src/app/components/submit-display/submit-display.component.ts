import { Component, OnInit } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { SIN } from 'src/app/models/sin';

@Component({
  selector: 'app-submit-display',
  templateUrl: './submit-display.component.html',
  styleUrls: ['./submit-display.component.css']
})
export class SubmitDisplayComponent implements OnInit {

  // bind this to HTML with two way model
  public submit_SIN : SIN;

  constructor(private sin: SinService) { }

  ngOnInit() {
  }

}
