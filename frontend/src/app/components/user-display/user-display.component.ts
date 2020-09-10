import { Component, OnInit } from '@angular/core';
import { User } from '../../models/user';
import { SIN } from 'src/app/models/sin';
import { Status } from 'src/app/models/status';
import { SinService } from 'src/app/services/sin.service';
import { UserService } from '../../services/user.service'
import { LogService } from 'src/app/services/log.service';
import { StatusService } from 'src/app/services/status.service';

// ReviewDisplayComponent
// 
//  Implemented Hierarchy : App -> UserDisplay
//  
//  UserDisplayComponent is a child of the AppComponent.
//
//  Description
//  
//  The UserDisplayComponent is the central hub of the UI application.
//  All other components plug into it, receive information from it and
//  and pass information back to it. The UserDisplayComponent controls
//  the flow of the application.
//
//  Think of the UserDisplayComponent as a grid with three slots. In the
//  the first slot a panel has been inserted containing information about 
//  the currently logged in user. In the second slot is a panel containing 
//  group specific displays, i.e. displays formatted for submitters, 
//  reviewers or approvers. This second slot will change depending on the 
//  group the User has been added to in the backend logic. The third slot
//  is a selection panel that changes based on user input. In the second slot,
//  the panel will contain a list of SINs. If the user clicks on one, that
//  SIN's details will be shown in the third slotted panel.
//
//  In other words, a selection_event will be emitted from the component in
//  in the second slot, passed up to the parent component, i.e. this component,
//  processed, and then passed down to the panel in the third slot. This is what
//  is meant by saying the UserDisplayComponent is the central hub of the UI
//  application.

@Component({
  selector: 'app-user-display',
  templateUrl: './user-display.component.html'
})
export class UserDisplayComponent implements OnInit {

    // Location for Debug Logging
  private class_name = "UserDisplayComponent";
    // TODO: configure debug based on environment.ts file
  public DEBUG : boolean = false;
    // User logged into backend
  public user : User = { id: null, email: null, groups: null}
    // User associated with the selected_SIN
  public selected_User: User = { id: null, email: null, groups: null}
    // User selected SIN from list. This variable is set through 
    // events emitted from child components. 
  public selected_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null, 
                                sin_description: null, sin_title: null };
    // determines whether or not the third panel is a SIN field viewer or editor pane.
  public edit_mode : boolean = false;
    // determines whether or not to display a saved message on screen
  public saved : boolean = false;
    // feeds into SubmitDisplayComponent and ReviewDisplayComponent to signal a selection
    // has been cleared from within this component.
  public switcher: boolean = false;
    // flag to allow admin to view page as basic user
  public admin_view_as_user : boolean = false;
    // table for converting status_ids into status names.
  public status_lookup: Status[] = [];


  constructor(private userService: UserService,
                private statusService: StatusService,
                private sinService: SinService,
                private logger: LogService) { }

  ngOnInit() {
    this.logger.log('Intializing', `${this.class_name}.ngOnInit`)
    this.getUser()
    this.statusService.getStatuses().subscribe( (statuses)=>{
      this.logger.log('Statuses Retrieved', `${this.class_name}.ngOnInit`)
      this.status_lookup = statuses;
    })
  }

  public getUser(): void {
    this.logger.log('Retrieving User', `${this.class_name}.getUser`)
    this.userService.getUser().subscribe((user : User) =>{
      this.logger.log('User Retrieved', `${this.class_name}.getUser`)
      this.user = user;
    })
  }

  public selectSIN(sin: SIN): void{
    if(!this.edit_mode){
      this.saved = false;
      this.logger.log(`Selecting SIN: #${sin.sin_number}`, `${this.class_name}.selectSIN`)
      this.selected_SIN = sin;
      this.logger.log('Retrieving User From SIN #', `${this.class_name}.selectSIN`)
      this.userService.getSINUser(sin.user_id).subscribe( (user)=>{
        this.logger.log(`User Retrieved For User: ${user.email}`, `${this.class_name}.selectSIN`)
        this.selected_User = user;
      })
    }
  }

  public clearSelectedSIN(sin: SIN, fromEvent : boolean):void{
    this.logger.log('Clearing Selected SIN', `${this.class_name}.clearSelecetedSIN`)
    this.selected_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
      sin_description: null, sin_title: null };
    if(!fromEvent){ this.switcher=!this.switcher;}
  }

  public switchModes(): void{
    this.edit_mode = !this.edit_mode
    if(this.edit_mode){ 
      this.logger.log('Edit Mode Activated', `${this.class_name}.switchModes`); 
      this.saved = false;
    }
    else{ 
      this.logger.log('View Mode Activated', `${this.class_name}.switchModes`) 
    }
  }

  public saveSIN(sin: SIN): void{
    this.logger.log(`Saving User Edited SIN # ${sin.sin_number}`, `${this.class_name}.saveSIN`)
    this.sinService.updateSIN(sin).subscribe((updateSIN)=>{
      this.logger.log(`Sin #${updateSIN.sin_number} Updated`, `${this.class_name}.saveSIN`)
    })
    this.selected_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description: null, sin_title: null };
    this.saved = true;
    this.switchModes();
  }

  public cancel(msg: String): void{ 
    this.logger.log('Cancelling Edit Mode', `${this.class_name}.cancel`);
    this.selected_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description: null, sin_title: null };
    this.switchModes(); 
  }
}
