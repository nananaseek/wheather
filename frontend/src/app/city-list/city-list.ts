import { Component, inject } from '@angular/core';
import { CityButton } from '../city-button/city-button';
import { CityButtonCreate } from '../city-button-create/city-button-create';
import { Api } from '../api';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-city-list',
  imports: [CommonModule, CityButton, CityButtonCreate],
  templateUrl: './city-list.html',
  styleUrl: './city-list.css',
})
export class CityList {
  public apiService = inject(Api);

  ngOnInit() {
    this.apiService.getAllCities();
  }
}
