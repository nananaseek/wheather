import { WeatherGet } from "./weather-get";

export interface CityGet {
    id: number;
    name: string;
    weather: WeatherGet
}
