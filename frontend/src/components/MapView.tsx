import { useEffect, useRef, useState, useCallback } from 'react';
import maplibregl from 'maplibre-gl';
import { api } from '../services/api';
import { GeoJSONCollection, SimulationResponse } from '../types';

interface MapViewProps {
  activeLayer: 'traffic' | 'aqi';
  simulationData: SimulationResponse | null;
}

function MapView({ activeLayer, simulationData }: MapViewProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const [error, setError] = useState<string | null>(null);
  const isMountedRef = useRef(true);
  const [loadingTraffic, setLoadingTraffic] = useState(false);
  const [loadingAQI, setLoadingAQI] = useState(false);

  useEffect(() => {
    isMountedRef.current = true;
    console.log('[MapView] Mounted');
    return () => {
      isMountedRef.current = false;
      console.log('[MapView] Unmounted');
    };
  }, []);

  useEffect(() => {
    if (!mapContainer.current) return;

    try {
      console.log('[MapView] Initializing MapLibre map');
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: {
          version: 8,
          glyphs: 'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf',
          sources: {
            osm: {
              type: 'raster',
              tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
              tileSize: 256,
              attribution: '© OpenStreetMap contributors',
            },
          },
          layers: [
            {
              id: 'osm',
              type: 'raster',
              source: 'osm',
            },
          ],
        },
        center: [103.8198, 1.2966],
        zoom: 12,
      });

      map.current.on('load', () => {
        if (!isMountedRef.current) return;
        console.log('[MapView] Map load event fired');
        if (map.current?.isStyleLoaded()) {
          loadTrafficData();
          loadAQIData();
        }
      });

      map.current.on('error', (e) => {
        console.error('Map error:', e);
        setError('Map loading error');
      });

      setTimeout(() => {
        if (map.current && isMountedRef.current) {
          map.current.resize();
        }
      }, 300);

      return () => {
        if (map.current) {
          map.current.remove();
          map.current = null;
        }
      };
    } catch (err) {
      console.error('Error initializing map:', err);
      setError('Failed to initialize map');
    }
  }, []);

  const loadTrafficData = useCallback(async () => {
    if (!map.current || !map.current.isStyleLoaded() || !isMountedRef.current) {
      return;
    }

    console.log('[MapView] Loading traffic data...');
    setLoadingTraffic(true);

    try {
      const data = await api.getTrafficData();
      console.log('[MapView] Traffic data:', data);
      
      if (!isMountedRef.current || !map.current) return;
      
      if (!data || data.type !== 'FeatureCollection' || !Array.isArray(data.features)) {
        console.error('Invalid traffic data format:', data);
        setError('Invalid traffic data format');
        return;
      }

      const source = map.current.getSource('traffic') as maplibregl.GeoJSONSource;
      
      if (source) {
        try {
          source.setData(data as GeoJSON.FeatureCollection);
        } catch (err) {
          console.error('Error updating traffic source:', err);
        }
      } else {
        if (!map.current.isStyleLoaded()) {
          setTimeout(() => loadTrafficData(), 100);
          return;
        }

        try {
          console.log('[MapView] Adding traffic source and layer');
          map.current.addSource('traffic', {
            type: 'geojson',
            data: data as GeoJSON.FeatureCollection,
          });

          if (!map.current.isStyleLoaded()) return;

          if (!map.current.getLayer('traffic-lines')) {
            map.current.addLayer({
              id: 'traffic-lines',
              type: 'line',
              source: 'traffic',
              paint: {
                'line-color': [
                  'case',
                  ['has', 'congestion_level'],
                  [
                    'case',
                    ['<', ['get', 'congestion_level'], 0.4],
                    '#22c55e',
                    ['<', ['get', 'congestion_level'], 0.7],
                    '#eab308',
                    '#ef4444',
                  ],
                  [
                    'match',
                    ['get', 'congestion'],
                    'low',
                    '#22c55e',
                    'moderate',
                    '#eab308',
                    'high',
                    '#ef4444',
                    '#6b7280',
                  ],
                ],
                'line-width': 4,
                'line-opacity': 0.8,
              },
            });
          }
        } catch (err) {
          console.error('Error adding traffic layer:', err);
        }
      }
    } catch (err) {
      console.error('Error loading traffic data:', err);
      setError('Failed to load traffic data');
    } finally {
      setLoadingTraffic(false);
    }
  }, []);

  const loadAQIData = useCallback(async () => {
    if (!map.current || !map.current.isStyleLoaded() || !isMountedRef.current) {
      return;
    }

    console.log('[MapView] Loading AQI data...');
    setLoadingAQI(true);

    try {
      const data = await api.getAQIData();
      console.log('[MapView] AQI data:', data);
      
      if (!isMountedRef.current || !map.current) return;
      
      if (!data || data.type !== 'FeatureCollection' || !Array.isArray(data.features)) {
        console.error('Invalid AQI data format:', data);
        setError('Invalid AQI data format');
        return;
      }

      const source = map.current.getSource('aqi') as maplibregl.GeoJSONSource;
      
      if (source) {
        try {
          source.setData(data as GeoJSON.FeatureCollection);
        } catch (err) {
          console.error('Error updating AQI source:', err);
        }
      } else {
        if (!map.current.isStyleLoaded()) {
          setTimeout(() => loadAQIData(), 100);
          return;
        }

        try {
          console.log('[MapView] Adding AQI source and layer');
          map.current.addSource('aqi', {
            type: 'geojson',
            data: data as GeoJSON.FeatureCollection,
          });

          if (!map.current.isStyleLoaded()) return;

          if (!map.current.getLayer('aqi-circles')) {
            map.current.addLayer({
              id: 'aqi-circles',
              type: 'circle',
              source: 'aqi',
              paint: {
                'circle-radius': [
                  'interpolate',
                  ['linear'],
                  ['get', 'aqi'],
                  0,
                  10,
                  100,
                  20,
                  200,
                  30,
                ],
                'circle-color': [
                  'interpolate',
                  ['linear'],
                  ['get', 'aqi'],
                  0,
                  '#00e400',
                  50,
                  '#ffff00',
                  100,
                  '#ff7e00',
                  150,
                  '#ff0000',
                  200,
                  '#8f3f97',
                ],
                'circle-opacity': 0.6,
                'circle-stroke-width': 2,
                'circle-stroke-color': '#ffffff',
              },
            });
          }

          if (!map.current.isStyleLoaded()) return;

          map.current.on('click', 'aqi-circles', (e) => {
            if (!map.current || !map.current.isStyleLoaded() || !isMountedRef.current) return;
            if (!e.features || !e.features[0]) return;

            const feature = e.features[0] as any;
            const properties = feature.properties || {};
            const geometry = feature.geometry as GeoJSON.Point;
            const coordinates = geometry.coordinates.slice();

            new maplibregl.Popup()
              .setLngLat([coordinates[0], coordinates[1]])
              .setHTML(`
                <div class="p-2">
                  <h3 class="font-bold text-lg mb-2">${properties?.station || 'AQI Station'}</h3>
                  <p class="text-sm"><strong>AQI:</strong> ${properties?.aqi || 'N/A'} (${properties?.category || 'Unknown'})</p>
                  <p class="text-sm"><strong>PM2.5:</strong> ${properties?.pm25 || 'N/A'} µg/m³</p>
                  ${properties?.pm10 ? `<p class="text-sm"><strong>PM10:</strong> ${properties?.pm10} µg/m³</p>` : ''}
                </div>
              `)
              .addTo(map.current);
          });

          map.current.on('mouseenter', 'aqi-circles', () => {
            if (map.current && map.current.isStyleLoaded() && isMountedRef.current) {
              map.current.getCanvas().style.cursor = 'pointer';
            }
          });

          map.current.on('mouseleave', 'aqi-circles', () => {
            if (map.current && map.current.isStyleLoaded() && isMountedRef.current) {
              map.current.getCanvas().style.cursor = '';
            }
          });
        } catch (err) {
          console.error('Error adding AQI layer:', err);
        }
      }
    } catch (err) {
      console.error('Error loading AQI data:', err);
      setError('Failed to load AQI data');
    } finally {
      setLoadingAQI(false);
    }
  }, []);

  useEffect(() => {
    if (!map.current || !map.current.isStyleLoaded() || !isMountedRef.current) return;

    console.log('[MapView] Active layer changed:', activeLayer);

    try {
      if (activeLayer === 'traffic') {
        if (map.current.getLayer('traffic-lines')) {
          map.current.setLayoutProperty('traffic-lines', 'visibility', 'visible');
        }
        if (map.current.getLayer('aqi-circles')) {
          map.current.setLayoutProperty('aqi-circles', 'visibility', 'none');
        }
      } else {
        if (map.current.getLayer('traffic-lines')) {
          map.current.setLayoutProperty('traffic-lines', 'visibility', 'none');
        }
        if (map.current.getLayer('aqi-circles')) {
          map.current.setLayoutProperty('aqi-circles', 'visibility', 'visible');
        }
      }
    } catch (err) {
      console.error('Error changing layer visibility:', err);
    }
  }, [activeLayer]);

  useEffect(() => {
    if (!map.current || !map.current.isStyleLoaded() || !simulationData || !isMountedRef.current) return;

    try {
      console.log('[MapView] simulationData changed:', simulationData);
      const source = map.current.getSource('traffic') as maplibregl.GeoJSONSource;
      if (source && simulationData.after) {
        if (simulationData.after.type === 'FeatureCollection' && Array.isArray(simulationData.after.features)) {
          console.log('[MapView] Applying simulation AFTER data, features=', simulationData.after.features.length);
          source.setData(simulationData.after as GeoJSON.FeatureCollection);
        } else {
          console.error('Invalid simulation data format:', simulationData.after);
        }
      }
    } catch (err) {
      console.error('Error updating simulation data:', err);
    }
  }, [simulationData]);

  return (
    <>
      {(loadingTraffic || loadingAQI) && (
        <div className="absolute top-4 left-4 z-50 bg-black bg-opacity-60 text-white px-3 py-1 rounded">
          Loading {loadingTraffic ? 'traffic ' : ''}
          {loadingAQI ? 'AQI ' : ''}
          data...
        </div>
      )}
      {error && (
        <div className="absolute top-4 left-1/2 transform -translate-x-1/2 z-50 bg-red-500 text-white px-4 py-2 rounded shadow-lg">
          {error}
        </div>
      )}
      <div
        ref={mapContainer}
        className="absolute inset-0 w-full h-full"
        style={{ zIndex: 0 }}
      />
    </>
  );
}

export default MapView;
