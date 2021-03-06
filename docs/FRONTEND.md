### Documentation Navigation
[<< S3](S3.md) | [^ ReadMe ^](../README.md) | [API >>](API.md)

# Frontend Application 

This page will describe in more detail the general structure of the frontend application.  

## Authentication

Before the user can access the Angular frontend, he will need to authenticate through cloud.gov (or its fake backend when running locally). The authentication server redirects the user to the <i>login_success.html</i> HTML template, which is configured to load in the static javascript files generated by the Angular build process, which are stored in the <i>static</i> directory in the backend.

In other words, the Angular applications enters on the page the user is redirected to after successfully logging in. 

## Angular App Structure

The Angular frontend application currently has the following component hierachy,

Top Level: 
- UserDisplayComponent<br>

Bottom Level: 
- SubmitDisplayComponent 
- ReviewDisplayComponent
- EditDisplayComponent<br>

Optional:
- LoggerDisplayComponent

Think of the <i>UserDisplayComponent</i> as the main container for the rest of the application. The <i>UserDisplayComponent</i>contains information about the state of the overall application and the user associated with the current sessions. The <i>UserDisplayComponent</i> processes events generated in its child components. 

For example, while viewing a list of SINs within the <i>UserDisplayComponent</i>, the user may select a SIN, which will then be feed as input into <I>EditDisplayComponent</i>. From within the <i>EditDisplayComponent</i>, the user can opt to edit the SIN information or clear the selection. Either type of event propagates up to the <i>UserDisplayComponent</i>, signalling to it to clear the user selection or display an appropriate 'saved' message to the user. 

Each component, its function and life-cycle are described in more detail below.

## Components

### UserDisplayComponent

<b>Implemented Hierarchy : AppComponent -> UserDisplayComponent</b>

<i>UserDisplayComponent</i> is a child of the main <i>AppComponent</i>.
 
<b>Description</b>
  
The <i>UserDisplayComponent</i> is the central hub of the UI application. All other components plug into it, receive information from it and pass information back to it. The UserDisplayComponent controls the flow of the application.

Think of the <i>UserDisplayComponent</i> as a grid with three slots. In the the first slot a panel has been inserted containing information about the currently logged in user. In the second slot is a panel containing group specific displays, i.e. displays formatted for submitters, reviewers or approvers. This second slot will change depending on the group the User has been added to in the backend logic. The third slot is a selection panel that changes based on user input. In the second slot, the panel will contain a list of SINs. If the user clicks on one, that SIN's details will be shown in the third slotted panel. In other words, a selection_event will be emitted from the component in the second slot, passed up to the parent component, i.e. this component, processed, and then passed down to the panel in the third slot. This is what is meant by saying the <i>UserDisplayComponent</i> is the central hub of the UI application.

### SubmitDisplayComponent

<b>Implemented Hierarchy : AppComponent -> UserDisplayComponent -> SubmitDisplayComponent </b>
  
<i>SubmitDisplayComponent</i> is a child of the <i>UserDisplayComponent</i>. It receives information through input and passes information back to the parent through events the parent registers to listen to. Within UserDisplay Component, this component is only exposed to users with 'submitter' group privileges. 

<b>Description</b>

This component allows an authenticated user with valid group permissions to submit a new SIN submission or edit an existing SIN submission. This component consumes user input and passes it onto the backend for processing. Once it is done with the user, it will emit an event signalling to the parent component what type of transaction has occured. See Output Events for more information.

<b>Component Life Cycle</b>

This component's life-cycle is broken into two parts: Status Mode and Submit Mode. Status Mode occurs when the user is viewing their personal SIN submissions. From this state, the user can choose to submit a new SIN or edit an existing SIN. Either choice will send the component to the next state in its life-cycle, Submit Mode.

The application in Submit Mode will receive an input of either <i>exists = true</i> or <i>exists=false</i>, depending on if the user opted to created a new SIN submission, i.e., <i>exists=false</i>, or if the user opted to edit an existing SIN submission, i.e <i>exists=true</i>'. 

This flag, <i>exists</i>, determines whether or not the component needs to load in all of the SIN data provided by the backend, or can go straight to the submission stage. It will also determine if the component needs to load attachments.
If editing an existing SIN, all previously uploaded attachments will be loaded for the user to download and edit. (TODO: This feature is not yet fully implemented...)

<b>HTML Attribute Inputs</b> 

[user], [selectable], [save_message], [clear_switch]

As input, this component requires the user authenticated with the current session [user], a boolean flag that determines whether or not the SINS displayed will be selectable (i.e, clickable and highlightable) [selectable], a boolean flag that determines whether or not to display a save message to the user [save_message] and a boolean flag that will signal to the parent component to clear any highlighted user selections anytime it changes value, true or false, [clear_switch].

In the application, the variable, [save_message], signals to the child component a save_event has occured in the parent component and an appropriate message should be displayed on screen.

If thisUser is an object of type User, then

> <app-submit-display [user]="thisUser" [selectable]="true" [save_message]="true" [clear_switch]="true"></app-submit-display>
  
  will create an HTML component binded to the Angular component defined in this class. 

<b>Output Events</b>

This component emits two types of events: <i>selection_events</i> and <i>clear_events</i>. <i>selection_events</i> occur when the user clicks on one of the SINs in the displayed list. A <i>clear_event</i> occurs when the user causes the selection to clear. If doThis(object: Object) and doThat(object: Object) are methods in the parent component, then you can listen to the selection_event and clear_event with the following tag,

> <app-submit-display [user]="thisUser" [selectable]="true" [save_message]="true" (clear_event)="doThis($event)" (selection_event)="doThat($event)"></app-submit-display>

A selection_event will contain the SIN that has been selected by the user. A clear_event will contain the SIN that has been cleared from the selection.

### ReviewDisplayComponent

<b>Implemented Hierarchy : AppComponent -> UserDisplayComponent -> ReviewDisplayComponent </b>

<i>ReviewDisplayComponent</i> is a child of the <i>UserDisplayComponent</i>. It receives information through input and passes information back to the parent through events the parent registers to listen to.

<b>Description</b>

This component allows an authenticated user with valid group permissions (either reviewer, approver or admin) to view SIN submissions submitted by all users. This component consumes user input and passes up an event flag to the parent component for further UI processing.

<b>HTML Attribute Input</b> 

[user], [selectable], [save_message], [clear_switch]
 
As input, this component requires the user authenticated with the current session [user], a boolean flag that determines whether or not the SINS displayed will be selectable (i.e, clickable and highlightable) [selectable], a boolean flag that determines whether or not to display a save message to the user [save_message] and a boolean flag that will signal to the component to clear any highlighted user selections anytime it changes value, true or false [clear_switch].

In the application, the variable, save_message, signals to the child component a save_event has occured in the parent component and an appropriate message should be displayed on screen.

If thisUser is an object of type User, then

> <app-review-display [user]="thisUser" [selectable]="true" [save_message]="true" [clear_switch]="true"></app-review-display>
   
will create an HTML component binded to the Angular component defined in this class. 

<b>Output Events</b>

This component emits a selection_event. selection_events occur when the user clicks on one of the SINs in the displayed list. If doThis(object: Object) is a  method in the parent component, then you can listen to the selection_event with the following tag,

> <app-review-display [user]="thisUser" [selectable]="true" [save_message]="true" [clear_switch]="true" (selection_event)="doThis($event)"></app-review-display>


### EditDisplayComponent

<b>Implemented Hierarchy : AppComponent -> UserDisplayComponent -> Edit DisplayComponent </b>
 
<i>EditDisplayComponent</i> is a child of the <i>UserDisplayComponent</i>. It receives information through input and passes information back to the parent through events the parent registers to listen to.

<b>Description</b>

This component allows an authenticated user with valid group permissions to edit the fields on a SIN submission. This component consumes user input and passes it onto backend for processing. Once it is done with the user, it will emit an event signalling to the parent component what type of transaction has occured. See Output Events for more information.

<b>HTML Attribute Input</b>

As input, This component requires a SIN to edit and the user permission group associated with the user currently using the form. They must be specified in the HTML inline. For example, if thisSIN and thisGroup were variables in the parent component, the following tag,

> <app-edit-display [input_SIN]="thisSIN" [user_group] ></app-edit-display>
 
will create an HTML component binded to the Angular component defined in this this class. 

<b>Output Events</b>

This component emits two types of events: save_events and cancel_events. save_events occur when the user saves their edits. cancel_events occur when the user wishes to exit editing without saving. These events can be captured by the parent Angular component by binding a method to these events and injecting in the emitted $event. If doThis(object: Object) and doThat(object: Object) are methods in the parent component, then you can listen to the save_event and cancel_event with the following tag,

> <app-edit-display [input_SIN]="thisSIN" [user_group] (save_event)="doThis($event)" (cancel_event)="doThat($event)"></app-edit-display>

In the case of a save_event, the event object will contain the SIN object the user edited and passed to the backend application for persisting in the database. A cancel_event will contain a null SIN object.

## Services 
### ContextService
todo: document
### FileService
todo: document
### SinService
todo: document
### StatusService
todo: document
### UserService
todo: document

## Interceptors
### AuthInterceptor
todo: document

### Documentation Navigation
[<< S3](S3.md) | [^ ReadMe ^](../README.md) | [API >>](API.md)