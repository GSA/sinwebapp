import { Component, OnInit } from '@angular/core';
import { User } from '../models/user';
import { UserService } from '../services/user.service'

@Component({
  selector: 'app-user-display',
  templateUrl: './user-display.component.html',
  styleUrls: ['./user-display.component.css']
})
export class UserDisplayComponent implements OnInit {

  user : User;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.getUser()
  }

  getUser(): void {
    this.userService.getUser().subscribe(user=>{
      this.user = user;
    })
  }
}
