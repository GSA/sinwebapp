import { TestBed } from '@angular/core/testing';

import { SinService } from './sin.service';

describe('SinService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SinService = TestBed.get(SinService);
    expect(service).toBeTruthy();
  });
});
