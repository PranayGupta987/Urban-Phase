import { apiGet } from "./client";

export const getTraffic = () => apiGet("/data/traffic");
export const getAQI = () => apiGet("/data/aqi");
export const getWeather = () => apiGet("/data/weather");
