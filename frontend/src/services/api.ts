import { GeoJSONCollection, SimulationRequest, SimulationResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  async getStatus() {
    const response = await fetch(`${API_BASE_URL}/status`);
    return response.json();
  },

  async getTrafficData(): Promise<GeoJSONCollection> {
    const response = await fetch(`${API_BASE_URL}/data/traffic`);
    return response.json();
  },

  async getAQIData(): Promise<GeoJSONCollection> {
    const response = await fetch(`${API_BASE_URL}/data/aqi`);
    return response.json();
  },

  async runSimulation(request: SimulationRequest): Promise<SimulationResponse> {
    const response = await fetch(`${API_BASE_URL}/simulate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    return response.json();
  },
};
