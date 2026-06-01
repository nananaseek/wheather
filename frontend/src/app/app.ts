import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CityList } from './city-list/city-list';
import { Weather } from './weather/weather';

@Component({
  selector: 'app-root',
  imports: [CityList, Weather],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
