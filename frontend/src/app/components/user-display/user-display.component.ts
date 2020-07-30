import { Component, OnInit } from '@angular/core';
import { User } from '../../models/user';
import { UserService } from '../../services/user.service'

const null_User : User = {
  email: null,
  groups: null
}

@Component({
  selector: 'app-user-display',
  templateUrl: './user-display.component.html'
})
export class UserDisplayComponent implements OnInit {

  user : User;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.user = null_User;
    this.getUser()
  }

  getUser(): void {
    this.userService.getUser().subscribe((user : User) =>{
      this.user = user;
    })
  }
}
