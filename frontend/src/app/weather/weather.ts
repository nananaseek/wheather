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

  getLocalTime(timezoneOffsetInSeconds: string | number): Date {
    const offset = Number(timezoneOffsetInSeconds);
    
    const now = new Date();
    const utcTimestamp = now.getTime() + (now.getTimezoneOffset() * 60000);
    
    return new Date(utcTimestamp + (offset * 1000));
  }
}
