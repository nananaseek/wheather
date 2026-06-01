import { Component, inject, Input } from '@angular/core';
import { Api } from '../api';

@Component({
  selector: 'app-city-button',
  imports: [],
  template: `
    <button 
      (click)="selectThisCity()" 
      class="w-full bg-white hover:bg-blue-50 hover:text-blue-600 text-gray-800 font-semibold py-2 px-4 border border-gray-200 rounded-xl shadow-sm transition flex items-center justify-between">
      <span>📍 {{ cityName }}</span>
      <span class="text-xs text-gray-400">Переглянути →</span>
    </button>
  `
  // templateUrl: './city-button.html',
  // styleUrl: './city-button.css',
})
export class CityButton {
@Input() cityId!: number;   // Приймаємо ID від списку міст
  @Input() cityName: string = ''; // Приймаємо назву від списку міст
  
  private apiService = inject(Api);

  selectThisCity() {
    // Викликаємо наш оновлений метод
    this.apiService.getWeather(this.cityId, this.cityName);
  }
}
