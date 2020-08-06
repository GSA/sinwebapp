import { Component, OnInit } from '@angular/core';
import { User, null_User } from '../../models/user';
import { UserService } from '../../services/user.service'
import { LogService } from 'src/app/services/log.service';

@Component({
  selector: 'app-user-display',
  templateUrl: './user-display.component.html'
})
export class UserDisplayComponent implements OnInit {

  private class_name = "UserDisplayComponent";

  public user : User = null_User

  constructor(private userService: UserService,
                private logger: LogService) { }

  ngOnInit() {
    this.logger.log('Intializing', `${this.class_name}.ngOnInit`)
    this.getUser()
  }

  getUser(): void {
    this.userService.getUser().subscribe((user : User) =>{
      this.logger.log('User Retrieved', `${this.class_name}.getUser`)
      this.user = user;
    })
  }
}
