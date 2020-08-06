import { Component, OnInit, Input } from '@angular/core';
import { SinService } from 'src/app/services/sin.service';
import { SIN, null_SIN } from 'src/app/models/sin';
import { LogService } from 'src/app/services/log.service';
import { User } from 'src/app/models/user';



@Component({
  selector: 'app-submit-display',
  templateUrl: './submit-display.component.html'
})
export class SubmitDisplayComponent implements OnInit {

  private class_name = "SubmitDisplayComponent"

  // true = submit mode, false = status mode
  public whichMode : boolean = false;
  public submitted : boolean = false;
  public submit_SIN : SIN = null_SIN;
  public user_SINS: SIN[] =[];
  @Input() user: User;


  constructor(private sin: SinService,
              private logger: LogService) { }

  ngOnInit() { 
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.loadUserSINs();
  }

  public submitSIN(): void{
    this.sin.postSIN(this.submit_SIN).subscribe((response)=>{
      this.logger.log('SIN Posted', `${this.class_name}.submitSIN`)
      this.submit_SIN = null_SIN;
      this.submitted = true;
      this.whichMode = false;
    })
  }

  public changeModes(): void{
    this.whichMode = !this.whichMode;
    if(!this.whichMode){ this.loadUserSINs();}
  }

  public loadUserSINs(): void{
    this.sin.getUserSINs(this.user).subscribe( (sins)=>{
      this.logger.log('User SINS Retrieved', `${this.class_name}.loadUserSINs`)
      this.user_SINS = sins;
    })
  }
  
}
