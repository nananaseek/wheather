import { Component, inject, Input } from '@angular/core';
import { Api } from '../api';

@Component({
  selector: 'app-city-button',
  imports: [],
  // template: 
  templateUrl: './city-button.html',
  styleUrl: './city-button.css',
})
export class CityButton {
  @Input() cityId!: number;   // Приймаємо ID від списку міст
  @Input() cityName: string = ''; // Приймаємо назву від списку міст

  private apiService = inject(Api);

  selectThisCity() {
    // Викликаємо наш оновлений метод
    this.apiService.getWeather(this.cityId, this.cityName);
  }
  deleteThisCity(event: Event) {
    // Цей рядок зупиняє подію кліку і не дає їй спрацювати на батьківській кнопці!
    event.stopPropagation();

    if (confirm(`Ви впевнені, що хочете видалити місто ${this.cityName}?`)) {
      this.apiService.deleteCity(this.cityId);
    }
  }
}
