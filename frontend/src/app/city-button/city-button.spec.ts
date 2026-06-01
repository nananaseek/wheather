import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CityButton } from './city-button';

describe('CityButton', () => {
  let component: CityButton;
  let fixture: ComponentFixture<CityButton>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CityButton],
    }).compileComponents();

    fixture = TestBed.createComponent(CityButton);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
