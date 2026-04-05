import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActList } from './act-list';

describe('ActList', () => {
  let component: ActList;
  let fixture: ComponentFixture<ActList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ActList],
    }).compileComponents();

    fixture = TestBed.createComponent(ActList);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
