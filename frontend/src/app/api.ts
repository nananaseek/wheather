import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { City } from './models/city';
import { Weather } from './models/weather';
import { CityGet } from './models/city-get';
import { WeatherGet } from './models/weather-get';

@Injectable({
  providedIn: 'root',
})
export class Api {
  private http = inject(HttpClient);

  // Базовий URL твого FastAPI додатку
  private baseUrl = 'http://localhost:8000';

  // Джерело правди для погоди та списку міст
  private weatherSubject$ = new BehaviorSubject<WeatherGet | null>(null);
  public weather$ = this.weatherSubject$.asObservable();

  private citiesSubject$ = new BehaviorSubject<CityGet[]>([]);
  public cities$ = this.citiesSubject$.asObservable();

  public selectedCityName$ = new BehaviorSubject<string | null>(null);
  // ==========================================
  // МЕТОДИ ДЛЯ РОБОТИ З ПОГОДОЮ (Weather)
  // ==========================================

  /**
   * GET /get_weather?city_id=...
   * Отримує погоду для конкретного міста та оновлює потік
   */
  getWeather(cityId: number, cityName: string): void {
    // 1. Одразу очищаємо стару погоду (щоб увімкнувся стан завантаження)
    this.weatherSubject$.next(null);

    // 2. Запам'ятовуємо назву міста, на яке клікнули
    this.selectedCityName$.next(cityName);

    // 3. Робимо запит до FastAPI за ID міста
    const params = new HttpParams().set('city_id', cityId);
    this.http.get<WeatherGet>(`${this.baseUrl}/get_weather`, { params }).subscribe({
      next: (weather) => this.weatherSubject$.next(weather),
      error: (err) => {
        console.error('Помилка отримання погоди:', err);
        // Якщо сталася помилка (наприклад, 404), ми залишаємо weather$ як null,
        // і наш компонент автоматично покаже, що "дані ще не готові"
      }
    });
  }

  /**
   * GET /update-weather?city_id=...
   * Трігерить Celery-таску на бекенді для оновлення погоди,
   * а після успішного оновлення автоматично перезавантажує погоду в інтерфейсі
   */
  updateWeatherRequest(cityId: number): void {
    const params = new HttpParams().set('city_id', cityId);

    this.http.get<WeatherGet>(`${this.baseUrl}/update-weather`, { params }).subscribe({
      next: (updatedWeather) => {
        console.log('Погоду успішно оновлено');
        // Одразу пускаємо оновлені дані в потік
        this.weatherSubject$.next(updatedWeather);
      },
      error: (err) => console.error('Помилка оновлення погоди:', err)
    });
  }

  // ==========================================
  // МЕТОДИ ДЛЯ РОБОТИ З МІСТАМИ (City)
  // ==========================================

  /**
   * GET /get-all-city
   * Завантажує список усіх міст і оновлює потік
   */
  getAllCities(): void {
    this.http.get<CityGet[]>(`${this.baseUrl}/get-all-city`).subscribe({
      next: (cities) => this.citiesSubject$.next(cities),
      error: (err) => console.error('Помилка отримання списку міст:', err)
    });
  }

  /**
   * POST /create-city?city=...
   * Створює нове місто за назвою і після цього оновлює список міст
   */
  createCity(cityName: string): void {
    const params = new HttpParams().set('city', cityName);

    // Оскільки FastAPI приймає параметр у query, body залишаємо порожнім {}
    this.http.post<City>(`${this.baseUrl}/create-city`, {}, { params }).subscribe({
      next: (newCity) => {
        console.log('Місто успішно додано:', newCity);
        // Перезавантажуємо список міст, щоб нове місто з'явилося в інтерфейсі
        this.getAllCities();
      },
      error: (err) => {
        if (err.status === 409) {
          alert('Таке місто вже є в базі даних!');
        } else {
          console.error('Помилка створення міста:', err);
        }
      }
    });
  }

  /**
   * DELETE /delete-city-id/?city_id=...
   * Видаляє місто за ID та оновлює список міст
   */
  deleteCity(cityId: number): void {
    const params = new HttpParams().set('city_id', cityId);

    this.http.delete<boolean>(`${this.baseUrl}/delete-city-id/`, { params }).subscribe({
      next: (success) => {
        if (success) {
          console.log(`Місто з ID ${cityId} видалено`);
          // Оновлюємо список міст на фронтенді
          this.getAllCities();

          // Якщо видалили місто, погоду якого зараз показували — скидаємо її
          const currentWeather = this.weatherSubject$.value;
          // Тут можна за бажанням додати перевірку, чи збігається id міста
          this.weatherSubject$.next(null);
        }
      },
      error: (err) => console.error('Помилка видалення міста:', err)
    });
  }
}
