import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CityButtonCreate } from './city-button-create';

describe('CityButtonCreate', () => {
  let component: CityButtonCreate;
  let fixture: ComponentFixture<CityButtonCreate>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CityButtonCreate],
    }).compileComponents();

    fixture = TestBed.createComponent(CityButtonCreate);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
