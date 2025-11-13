export interface TrafficFeature {
  type: 'Feature';
  geometry: {
    type: 'LineString';
    coordinates: number[][];
  };
  properties: {
    name?: string;
    speed: number;
    congestion: string;
    volume: number;
    capacity?: number;
  };
}

export interface AQIFeature {
  type: 'Feature';
  geometry: {
    type: 'Point';
    coordinates: number[];
  };
  properties: {
    aqi: number;
    category: string;
    pm25: number;
    pm10: number;
    no2?: number;
    o3?: number;
    station: string;
    color?: string;
  };
}

export interface GeoJSONCollection {
  type: 'FeatureCollection';
  features: (TrafficFeature | AQIFeature)[];
}

export interface Metrics {
  avg_speed: number;
  congestion_index: number;
  co2_reduction: number;
  aqi_improvement: number;
}

export interface SimulationResponse {
  before: GeoJSONCollection;
  after: GeoJSONCollection;
  metrics: {
    before: Metrics;
    after: Metrics;
  };
}

export interface SimulationRequest {
  vehicle_reduction: number;
}
