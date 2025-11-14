export interface GeoJSONFeatureProperties {
  [key: string]: any;
}

export interface GeoJSONFeature {
  type: 'Feature';
  geometry:
    | {
        type: 'LineString';
        coordinates: [number, number][];
      }
    | {
        type: 'Point';
        coordinates: [number, number];
      };
  properties: GeoJSONFeatureProperties;
}

export interface GeoJSONCollection {
  type: 'FeatureCollection';
  features: GeoJSONFeature[];
}

export interface SimulationRequest {
  vehicle_reduction: number; // 0–100
  segment_ids?: number[] | null;
}

export interface SimulationMetrics {
  avg_congestion_before: number;
  avg_congestion_after: number;
  avg_speed_before: number;
  avg_speed_after: number;
  aqi_before: number;
  aqi_after: number;
}

export interface SimulationResponse {
  before: GeoJSONCollection;
  after: GeoJSONCollection;
  metrics: SimulationMetrics;
  error?: string | null;
}
