export interface TrafficFeature {
  type: 'Feature';
  geometry: {
    type: 'Point';
    coordinates: [number, number];
  };
  properties: {
    traffic_volume: number;
    congestion_level: string;
    street: string;
    simulated?: boolean;
  };
}

export interface AQIFeature {
  type: 'Feature';
  geometry: {
    type: 'Point';
    coordinates: [number, number];
  };
  properties: {
    aqi: number;
    category: string;
    pollutants: {
      pm25: number;
      pm10: number;
      o3: number;
    };
  };
}

export interface TrafficData {
  type: 'FeatureCollection';
  features: TrafficFeature[];
}

export interface AQIData {
  type: 'FeatureCollection';
  features: AQIFeature[];
}

export interface WeatherData {
  location: {
    name: string;
    lat: number;
    lon: number;
  };
  current: {
    temperature: number;
    feels_like: number;
    humidity: number;
    pressure: number;
    wind_speed: number;
    wind_direction: number;
    conditions: string;
    visibility: number;
  };
}

export interface SimulationMetrics {
  original_metrics: {
    avg_traffic: number;
    avg_aqi: number;
  };
  simulated_metrics: {
    avg_traffic: number;
    avg_aqi: number;
  };
  improvements: {
    traffic_reduction: number;
    aqi_reduction: number;
  };
  geojson_layers: {
    traffic: TrafficData;
    aqi: AQIData;
  };
}

export type LayerType = 'traffic' | 'aqi';
