import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SubmitDisplayComponent } from './submit-display.component';

describe('SubmitDisplayComponent', () => {
  let component: SubmitDisplayComponent;
  let fixture: ComponentFixture<SubmitDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SubmitDisplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SubmitDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
