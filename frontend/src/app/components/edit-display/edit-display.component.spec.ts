import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditDisplayComponent } from './edit-display.component';

describe('EditDisplayComponent', () => {
  let component: EditDisplayComponent;
  let fixture: ComponentFixture<EditDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditDisplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
