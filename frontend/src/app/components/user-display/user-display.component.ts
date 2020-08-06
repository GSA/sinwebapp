import { Component, OnInit } from '@angular/core';
import { User, null_User } from '../../models/user';
import { UserService } from '../../services/user.service'
import { LogService } from 'src/app/services/log.service';
import { null_SIN, SIN } from 'src/app/models/sin';
import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { SinService } from 'src/app/services/sin.service';

@Component({
  selector: 'app-user-display',
  templateUrl: './user-display.component.html'
})
export class UserDisplayComponent implements OnInit {

  private class_name = "UserDisplayComponent";

  public user : User = null_User;
  public selected_User: User = null_User;
  public selected_SIN: SIN = null_SIN;

  constructor(private userService: UserService,
                private logger: LogService) { }

  ngOnInit() {
    this.logger.log('Intializing', `${this.class_name}.ngOnInit`)
    this.getUser()
  }

  public getUser(): void {
    this.logger.log('Retrieving User', `${this.class_name}.getUser`)
    this.userService.getUser().subscribe((user : User) =>{
      this.logger.log('User Retrieved', `${this.class_name}.getUser`)
      this.user = user;
    })
  }

  public selectSIN(sin: SIN): void{
    this.logger.log(`Selecting SIN: #${sin.sin_number}`, `${this.class_name}.selectSIN`)
    this.selected_SIN = sin;
    this.logger.log('Retrieving User From SIN #', `${this.class_name}.selectSIN`)
    this.userService.getSINUser(sin.user_id).subscribe( (user)=>{
      this.logger.log(`User Retrieved from SIN #: ${user.email}`, `${this.class_name}.selectSIN`)
      this.selected_User = user;
    })

  }
}
