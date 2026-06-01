import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { CityGet } from './models/city-get';
import { WeatherGet } from './models/weather-get';

@Injectable({
  providedIn: 'root',
})
export class Api {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000';

  private loadingSubject$ = new BehaviorSubject<boolean>(false);
  public isLoading$ = this.loadingSubject$.asObservable();

  private citiesSubject$ = new BehaviorSubject<CityGet[]>([]);
  public cities$ = this.citiesSubject$.asObservable();

  private weatherSubject$ = new BehaviorSubject<WeatherGet | null>(null);
  public weather$ = this.weatherSubject$.asObservable();

  public selectedCityName$ = new BehaviorSubject<string | null>(null);


  getAllCities(): void {
    this.loadingSubject$.next(true);

    this.http.get<CityGet[]>(`${this.baseUrl}/get-all-city`).subscribe({
      next: (cities) => {
        this.citiesSubject$.next(cities);
        
        const currentCityName = this.selectedCityName$.value;
        if (currentCityName) {
          const updatedCity = cities.find(c => c.name === currentCityName);
          if (updatedCity) {
            this.weatherSubject$.next(updatedCity.weather);
          }
        }
        this.loadingSubject$.next(false);
      },
      error: (err) => {
        this.loadingSubject$.next(false);
        console.error('Помилка отримання міст та погоди:', err)
      }
    });
  }


  selectCityWeather(city: CityGet): void {
    this.selectedCityName$.next(city.name);
    this.weatherSubject$.next(city.weather);
  }


  updateWeatherRequest(cityId: number): void {
    const params = new HttpParams().set('city_id', cityId);

    this.http.get<any>(`${this.baseUrl}/update-weather`, { params }).subscribe({
      next: () => {
        console.log('Celery оновив погоду в БД. Перезавантажуємо список міст...');
        this.getAllCities();
      },
      error: (err) => console.error('Помилка Celery оновлення:', err)
    });
  }


  createCity(cityName: string): void {
    const params = new HttpParams().set('city', cityName);
    this.http.post<CityGet>(`${this.baseUrl}/create-city`, {}, { params }).subscribe({
      next: () => {
        this.getAllCities();
      },
      error: (err) => console.error(err)
    });
  }


  deleteCity(cityId: number): void {
    const params = new HttpParams().set('city_id', cityId);
    this.http.delete<boolean>(`${this.baseUrl}/delete-city-id/`, { params }).subscribe({
      next: (success) => {
        if (success) {
          this.getAllCities();
          this.weatherSubject$.next(null);
          this.selectedCityName$.next(null);
        }
      }
    });
  }
}
