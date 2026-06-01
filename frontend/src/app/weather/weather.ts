import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { Api } from '../api';

@Component({
  selector: 'app-weather',
  imports: [CommonModule],
  templateUrl: './weather.html',
  styleUrl: './weather.css',
})
export class Weather {
  public apiService = inject(Api);
}
