import { Component, inject, Input } from '@angular/core';
import { Api } from '../api';
import { CityGet } from '../models/city-get';

@Component({
  selector: 'app-city-button',
  imports: [],
  // template: 
  templateUrl: './city-button.html',
  styleUrl: './city-button.css',
})
export class CityButton {
  @Input() cityData!: CityGet;
  
  private apiService = inject(Api);

  selectThisCity() {
    this.apiService.selectCityWeather(this.cityData);
  }

  deleteThisCity(event: Event) {
    event.stopPropagation();
    if (confirm(`Ви впевнені, що хочете видалити місто ${this.cityData.name}?`)) {
      this.apiService.deleteCity(this.cityData.id);
    }
  }
}
