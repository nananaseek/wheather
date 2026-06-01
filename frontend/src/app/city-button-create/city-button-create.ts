import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Api } from '../api';

@Component({
  selector: 'app-city-button-create',
  imports: [CommonModule, FormsModule],
  templateUrl: './city-button-create.html',
  styleUrl: './city-button-create.css',
})
export class CityButtonCreate {
  private apiService = inject(Api);

  // Стан компонента: показувати інпут чи просто кнопку
  isEditing = false;
  
  // Змінна, куди записуватиметься назва міста з інпуту
  newCityName = '';

  // Метод для відкриття режиму введення
  openForm() {
    this.isEditing = true;
  }

  // Метод для скасування
  closeForm() {
    this.isEditing = false;
    this.newCityName = ''; // Очищаємо інпут
  }

  // Метод відправки на бекенд
  submitCity() {
    // Перевіряємо, чи користувач не відправляє порожній рядок
    if (this.newCityName.trim()) {
      // Викликаємо метод сервісу (він сам зробить POST і оновить список міст)
      this.apiService.createCity(this.newCityName.trim());
      
      // Закриваємо форму
      this.closeForm();
    }
  }
}
