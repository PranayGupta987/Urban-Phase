import {
  GeoJSONCollection,
  SimulationRequest,
  SimulationResponse,
} from "../types";

// Always derive base URL from VITE_API_URL, falling back to 127.0.0.1:8000
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
console.log("[API] Base URL:", API_BASE_URL);

export const api = {
  async getStatus() {
    try {
      const response = await fetch(`${API_BASE_URL}/status`);
      if (!response.ok) throw new Error("Failed to fetch status");
      const data = await response.json();
      console.log("[API] getStatus response:", data);
      return data;
    } catch (error) {
      console.error("API getStatus error:", error);
      throw error;
    }
  },

  async getTrafficData(): Promise<GeoJSONCollection> {
    try {
      const url = `${API_BASE_URL}/data/traffic`;
      console.log("[API] getTrafficData request:", url);
      const response = await fetch(url);
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `Failed to fetch traffic data: ${response.status} ${errorText}`
        );
      }
      const data = await response.json();
      if (!data || data.type !== "FeatureCollection") {
        throw new Error("Invalid traffic data format");
      }
      console.log(
        "[API] getTrafficData response: features=",
        Array.isArray(data.features) ? data.features.length : "N/A"
      );
      return data;
    } catch (error) {
      console.error("API getTrafficData error:", error);
      throw error;
    }
  },

  async getAQIData(): Promise<GeoJSONCollection> {
    try {
      const url = `${API_BASE_URL}/data/aqi`;
      console.log("[API] getAQIData request:", url);
      const response = await fetch(url);
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `Failed to fetch AQI data: ${response.status} ${errorText}`
        );
      }
      const data = await response.json();
      if (!data || data.type !== "FeatureCollection") {
        throw new Error("Invalid AQI data format");
      }
      console.log(
        "[API] getAQIData response: features=",
        Array.isArray(data.features) ? data.features.length : "N/A"
      );
      return data;
    } catch (error) {
      console.error("API getAQIData error:", error);
      throw error;
    }
  },

  async getWeatherData() {
    try {
      const url = `${API_BASE_URL}/data/weather`;
      console.log("[API] getWeatherData request:", url);
      const response = await fetch(url);
      if (!response.ok) throw new Error("Failed to fetch weather data");
      const data = await response.json();
      console.log("[API] getWeatherData response:", data);
      return data;
    } catch (error) {
      console.error("API getWeatherData error:", error);
      throw error;
    }
  },

  async runSimulation(request: SimulationRequest): Promise<SimulationResponse> {
    try {
      const url = `${API_BASE_URL}/simulate`;
      const payload = { vehicle_reduction: Number(request.vehicle_reduction) };
      console.log("[API] runSimulation request:", { url, payload });

      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch {
          errorData = {
            error: `HTTP ${response.status}: ${response.statusText}`,
          };
        }
        throw new Error(
          errorData.error || errorData.message || "Simulation failed"
        );
      }

      const data = (await response.json()) as SimulationResponse;
      console.log("[API] runSimulation response:", data);

      if (!data || !data.before || !data.after || !data.metrics) {
        throw new Error("Invalid simulation response format");
      }

      return data;
    } catch (error) {
      console.error("API runSimulation error:", error);
      throw error;
    }
  },
};
