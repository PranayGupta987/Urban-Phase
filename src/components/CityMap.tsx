import { useState } from 'react';
import Map, { NavigationControl } from 'react-map-gl';
import DeckGL from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';
import { HeatmapLayer } from '@deck.gl/aggregation-layers';
import { TrafficData, AQIData, LayerType } from '../types';
import 'mapbox-gl/dist/mapbox-gl.css';

interface CityMapProps {
  trafficData: TrafficData | null;
  aqiData: AQIData | null;
  activeLayer: LayerType;
}

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || '';

const INITIAL_VIEW_STATE = {
  longitude: -74.0060,
  latitude: 40.7128,
  zoom: 12,
  pitch: 45,
  bearing: 0,
};

export function CityMap({ trafficData, aqiData, activeLayer }: CityMapProps) {
  const [viewState, setViewState] = useState(INITIAL_VIEW_STATE);

  const layers = [];

  if (activeLayer === 'traffic' && trafficData) {
    const trafficPoints = trafficData.features.map((f) => ({
      position: [f.geometry.coordinates[0], f.geometry.coordinates[1]],
      weight: f.properties.traffic_volume,
    }));

    layers.push(
      new HeatmapLayer({
        id: 'traffic-heatmap',
        data: trafficPoints,
        getPosition: (d: any) => d.position,
        getWeight: (d: any) => d.weight,
        radiusPixels: 60,
        intensity: 1,
        threshold: 0.05,
        colorRange: [
          [0, 255, 0, 100],
          [255, 255, 0, 150],
          [255, 165, 0, 200],
          [255, 0, 0, 255],
        ],
      })
    );
  }

  if (activeLayer === 'aqi' && aqiData) {
    const aqiPoints = aqiData.features.map((f) => ({
      position: [f.geometry.coordinates[0], f.geometry.coordinates[1]],
      aqi: f.properties.aqi,
      category: f.properties.category,
    }));

    layers.push(
      new ScatterplotLayer({
        id: 'aqi-circles',
        data: aqiPoints,
        pickable: true,
        opacity: 0.6,
        stroked: true,
        filled: true,
        radiusScale: 100,
        radiusMinPixels: 20,
        radiusMaxPixels: 100,
        lineWidthMinPixels: 2,
        getPosition: (d: any) => d.position,
        getRadius: (d: any) => d.aqi / 5,
        getFillColor: (d: any) => {
          if (d.aqi <= 50) return [0, 255, 0, 180];
          if (d.aqi <= 100) return [255, 255, 0, 180];
          if (d.aqi <= 150) return [255, 165, 0, 180];
          if (d.aqi <= 200) return [255, 0, 0, 180];
          return [139, 0, 0, 180];
        },
        getLineColor: [255, 255, 255, 200],
      })
    );
  }

  return (
    <div className="relative w-full h-full rounded-lg overflow-hidden shadow-lg">
      <DeckGL
        viewState={viewState}
        onViewStateChange={({ viewState }: any) => setViewState(viewState)}
        controller={true}
        layers={layers}
      >
        <Map
          mapboxAccessToken={MAPBOX_TOKEN}
          mapStyle="mapbox://styles/mapbox/dark-v11"
          attributionControl={false}
        >
          <NavigationControl position="top-right" />
        </Map>
      </DeckGL>

      <div className="absolute bottom-4 left-4 bg-white bg-opacity-90 rounded-lg p-3 shadow-lg">
        <h3 className="text-sm font-bold text-gray-900 mb-2">
          {activeLayer === 'traffic' ? 'Traffic Intensity' : 'Air Quality Index'}
        </h3>
        <div className="space-y-1">
          {activeLayer === 'traffic' ? (
            <>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(0, 255, 0)' }}></div>
                <span className="text-xs text-gray-700">Low</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(255, 255, 0)' }}></div>
                <span className="text-xs text-gray-700">Moderate</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(255, 165, 0)' }}></div>
                <span className="text-xs text-gray-700">High</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(255, 0, 0)' }}></div>
                <span className="text-xs text-gray-700">Severe</span>
              </div>
            </>
          ) : (
            <>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(0, 255, 0)' }}></div>
                <span className="text-xs text-gray-700">Good (0-50)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(255, 255, 0)' }}></div>
                <span className="text-xs text-gray-700">Moderate (51-100)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(255, 165, 0)' }}></div>
                <span className="text-xs text-gray-700">Unhealthy (101-150)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded" style={{ backgroundColor: 'rgb(255, 0, 0)' }}></div>
                <span className="text-xs text-gray-700">Very Unhealthy (151+)</span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
