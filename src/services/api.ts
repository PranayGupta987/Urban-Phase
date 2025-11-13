import { TrafficData, AQIData, WeatherData, SimulationMetrics } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  async getTrafficData(): Promise<TrafficData> {
    const response = await fetch(`${API_URL}/data/traffic`);
    if (!response.ok) throw new Error('Failed to fetch traffic data');
    return response.json();
  },

  async getAQIData(): Promise<AQIData> {
    const response = await fetch(`${API_URL}/data/aqi`);
    if (!response.ok) throw new Error('Failed to fetch AQI data');
    return response.json();
  },

  async getWeatherData(): Promise<WeatherData> {
    const response = await fetch(`${API_URL}/data/weather`);
    if (!response.ok) throw new Error('Failed to fetch weather data');
    return response.json();
  },

  async runSimulation(
    trafficReduction: number,
    applyGreenZones: boolean
  ): Promise<SimulationMetrics> {
    const response = await fetch(`${API_URL}/simulate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        traffic_reduction: trafficReduction,
        apply_green_zones: applyGreenZones,
      }),
    });
    if (!response.ok) throw new Error('Failed to run simulation');
    return response.json();
  },

  async predictAQI(features: {
    hour: number;
    day_of_week: number;
    temperature: number;
    humidity: number;
    is_rush_hour?: number;
    is_weekend?: number;
  }) {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(features),
    });
    if (!response.ok) throw new Error('Failed to predict AQI');
    return response.json();
  },
};
