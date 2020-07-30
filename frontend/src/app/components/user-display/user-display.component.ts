import { Component, OnInit } from '@angular/core';
import { User } from '../../models/user';
import { UserService } from '../../services/user.service'
import { LogService } from 'src/app/services/log.service';

@Component({
  selector: 'app-user-display',
  templateUrl: './user-display.component.html'
})
export class UserDisplayComponent implements OnInit {

  user : User = {
    email: null,
    groups: null
  };

  constructor(private userService: UserService,
                private logger: LogService) { }

  ngOnInit() {
    this.getUser()
  }

  getUser(): void {
    this.userService.getUser().subscribe((user : User) =>{
      this.user = user;
    })
  }
}
