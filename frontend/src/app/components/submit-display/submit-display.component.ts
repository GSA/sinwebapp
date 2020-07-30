import { Component, OnInit } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { SIN } from 'src/app/models/sin';

@Component({
  selector: 'app-submit-display',
  templateUrl: './submit-display.component.html'
})
export class SubmitDisplayComponent implements OnInit {

  // bind this to HTML with two way model
  public submit_SIN : SIN = {
    sin_number: null,
    status: null
  };

  constructor(private sin: SinService) { }

  ngOnInit() { this.submit_SIN; }

  public submitSIN(): void{
    this.sin.postSIN(this.submit_SIN).subscribe((response)=>{
      console.log('submit-display.component.submitSIN: SIN Posted!')
      console.log(`Response: ${response}`)
    })
  }
}
