export interface WeatherGet {
    id: number;
    temperature: number;
    temp_feels_like: number;
    temp_min: number;
    temp_max: number;
    visibility: number;
    dt: string;
    country: string;
    sunrise: string;
    sunset: string;
    humidity: number;
    timezone: string;
    name: string;
    rain: number;
    clouds: number;
    description: string;
}
