import { Component, OnInit, Input, Output, EventEmitter, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms'
import { SIN } from 'src/app/models/sin';
import { User } from 'src/app/models/user';
import { Status } from 'src/app/models/status';
import { LogService } from 'src/app/services/log.service';
import { StatusService } from 'src/app/services/status.service';
import { SinService } from 'src/app/services/sin.service';
import { FileService } from 'src/app/services/file.service';
import { Attachment } from 'src/app/models/attachment';
import { ContextService } from 'src/app/services/context.service';

// See docs/FRONTEND.md for full component documentation

@Component({
  selector: 'app-submit-display',
  templateUrl: './submit-display.component.html'
})
export class SubmitDisplayComponent implements OnInit {
  // TODO: Load in existing attachments to display for a given selected SIN

  private class_name = "SubmitDisplayComponent";

  // BINARY COMPONENT FLAGS
    // determines whether or not user will create new or edit existing sin
  public exists : boolean;
    // determines whether or not user is viewing all sins or submitting
  public submit_mode : boolean = false;
    // determines whether or not the user has submitted a SIN
  public submitted: boolean = false;
    // determines whether or not the user has selected a file to upload
  public file_selected: boolean = false;
    // determines if fields are entered
  public step_1_complete: boolean = false;
    // determines if file is attached, needs initialized to null to trick disabled HTML attribute
  public step_2_complete: boolean = false;


    // used in Submit Mode to hold the validated SIN to be submitted.
  public submit_SIN : SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                               sin_description: null, sin_title: null };
    // used in Status Mode to hold the user selected SIN to be displayed by parent component.
  public selected_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                                sin_description: null, sin_title: null };
    // used in Submit Existing Mode to hold the SIN the user has selected to edit.
  public existing_SIN: SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                                sin_description: null, sin_title: null };
    // list of all SINs associated with a user
  public user_SINs: SIN[] =[];
    // list of all publicly viewable SINs
  public all_SINs: SIN[] =[]
    // status dictionary
  public status_lookup: Status[] = [];
    // used to hold attachments during Submit Mode
  public attachments : Attachment[] = [];
  public fileForm: FormGroup;

  @Input() public user: User;
  @Input() public selectable: boolean; 
  @Input() public save_message: boolean;
  @Input() public clear_switch: boolean;
  @Output() public selection_event = new EventEmitter<SIN>();
  @Output() public clear_event = new EventEmitter<SIN>();

  constructor(private formBuilder: FormBuilder,
              private contextService: ContextService,
              private fileService: FileService,
              private sinService: SinService,
              private statusService: StatusService,
              private logger: LogService) {


  }

  ngOnInit() { 
    this.logger.log('Initializing', `${this.class_name}.ngOnInit`)
    this.logger.log('Building FormGroup for FileForm', `${this.class_name}.ngOnInit`)
    this.fileForm = this.formBuilder.group({ sin_number: [''], file: [''] })
    this.loadUserSINs();
    this.statusService.getStatuses().subscribe( (statuses) => {
      this.status_lookup = statuses;
    })
  }

  ngOnChanges(changes: SimpleChanges){
    if(changes.selectable !== undefined){ this.loadUserSINs(); }
    if(changes.clear_switch !== undefined) { 
      this.selected_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description: null, sin_title: null };
    };
    console.log('did something in NgOnChanges')
    console.log(`changes: ${changes}`)
  }

  public loadAllSINs(){
    this.logger.log('Loading All SINs',`${this.class_name}.loadAllSINs`);
    this.sinService.getSINs().subscribe( (sins) =>{
      this.logger.log('All SINs Loaded', `${this.class_name}.loadAllSINs`);
      this.all_SINs = sins;
    })
  }

  public loadUserSINs(): void{
    this.logger.log('Loading User SINs', `${this.class_name}.loadUserSINs`);
    this.sinService.getUserSINs(this.user).subscribe( (sins)=>{
      this.logger.log('User SINS Loaded', `${this.class_name}.loadUserSINs`);
      this.user_SINs = sins;
    })
  }

  public submitSIN(): void{
    if(!this.exists){
      this.logger.log('Submitting New SIN', `${this.class_name}.submitSIN`);
      this.sinService.postSIN(this.submit_SIN).subscribe((response)=>{
        this.logger.log('SIN Submitted', `${this.class_name}.submitSIN`);
        this.submit_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                              sin_description: null, sin_title: null };
        this.submitted = true;
        this.switchModes(false);
      })
    }
    else{
      this.logger.log('Submitting Existing SIN', `${this.class_name}.submitSIN`);
      if(!this.submit_SIN.status_id) { this.submit_SIN.status_id = this.existing_SIN.status_id; };
      if(!this.submit_SIN.user_id) { this.submit_SIN.user_id = this.existing_SIN.user_id; };
      if(!this.submit_SIN.id) { this.submit_SIN.id = this.existing_SIN.id; };
      this.sinService.updateSIN(this.submit_SIN).subscribe((response)=>{
        this.submit_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                              sin_description: null, sin_title: null };
          this.submitted = true;
          this.switchModes(false);
      });
    };
  }

  public clearMessage(): void { this.submitted = false; }
  
  public switchModes(exists: boolean): void{
    this.exists = exists;

    if(this.exists){ this.loadAllSINs(); }

    this.logger.log('Switching Modes', `${this.class_name}.switchModes`);
    this.submit_mode = !this.submit_mode;

    if(!this.submit_mode){ 
      // Initializing Status Mode
      this.logger.log('Status Mode Activated', `${this.class_name}.switchModes`);
      this.loadUserSINs();
      this.step_1_complete = false;
      this.step_2_complete = false;
      this.file_selected = false;
      this.fileForm.get('sin_number').setValue(null);
      this.fileForm.get('file').setValue(null);
      this.attachments = []
    }
    else{ 
      // Initializing Submission Mode
      if(this.exists){ this.logger.log('Submission Mode for Existing SINS Activated', `${this.class_name}.switchModes`);  }
      else {this.logger.log('Submission Mode for New SINs Activated', `${this.class_name}.switchModes`);  }
      this.submitted = false;
      this.submit_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description: null, sin_title: null };
      this.selected_SIN = { id: null, sin_number: null, user_id: null, status_id: null,
                            sin_description: null, sin_title: null };
      this.clear_event.emit(this.selected_SIN);
      this.logger.log('Emitting Clear Event', `${this.class_name}.switchModes`)
    }
  }

  // process selection_events for parent component, only used in Status Mode
  public selectSIN(sin: SIN){
    this.logger.log(`Selecting selected_SIN: # ${sin.sin_number}`, `${this.class_name}.selectSIN`);
    this.submitted = false;
    this.selected_SIN = sin;
    this.logger.log(`Emitting Selection Event`, `${this.class_name}.selectSIN`);
    this.selection_event.emit(sin);
  }

  // processes user clicks when in Submit Existing Mode, only used in Edit Existing Mode
  public selectExistingSIN(selection: string){
    let sin = JSON.parse(selection);
    this.logger.log(`Selecting existing_SIN to Edit: # ${sin.sin_number}`, `${this.class_name}.selectExistingSIN`);
    this.existing_SIN = { id: sin.id, sin_number: sin.sin_number, user_id: sin.user_id, status_id: sin.status_id,
                          sin_description: sin.sin_description, sin_title: sin.sin_title };
    this.getSINFileList(sin.sin_number);
  }

  // used to set step 1 to complete
  public submitFields(){ 
    this.logger.log(`Submit_SIN Processed: ${this.submit_SIN.sin_number}, ${this.submit_SIN.sin_title}`,
                     `${this.class_name}.submitFields`)
    this.step_1_complete = true; 
  }

  public selectFile(event){
    if(event.target.files.length > 0 ){
      const userFile = event.target.files[0];
      this.fileForm.get('sin_number').setValue(this.submit_SIN.sin_number);
      this.fileForm.get('file').setValue(userFile);
      this.file_selected = true;
    }
  }
  
  public submitFile(){
    this.fileService.uploadFile(this.fileForm).subscribe( () =>{
      this.logger.log('File Submitted', `${this.class_name}.submitFile`);
      this.step_2_complete = true;
    })
  }

  public getSINFileList(sin: string){
    this.fileService.getFileListForSIN(sin).subscribe((attach) =>{
      this.attachments = attach;
      this.logger.log(`File List Retrieved For SIN # ${sin}`, `${this.class_name}.getSINFileList`);
      if(attach.length>0){
        this.logger.log(`Attachment Exists For SIN #${sin}`,`${this.class_name}.getSINFileList`)
        this.logger.log('Bypassing File Upload Step of SIN Submission', `${this.class_name}.getSINFileList`)
        this.bypassFileUpload()
      }
    })
  }

  public test(msg: string){
    console.log(msg);
  }

  public bypassFileUpload(){ this.step_2_complete=true; }

  public editFields(){ this.step_1_complete = false; }

  public getDownloadURL(sin: string){ return this.contextService.getFileDownloadUrl(sin); }

}
