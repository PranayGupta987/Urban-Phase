import { useEffect, useRef, useState } from 'react';
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
  const [trafficData, setTrafficData] = useState<GeoJSONCollection | null>(null);
  const [aqiData, setAqiData] = useState<GeoJSONCollection | null>(null);

  useEffect(() => {
    if (!mapContainer.current) return;

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
      center: [-0.1278, 51.5074],
      zoom: 13,
    });

    map.current.on('load', () => {
      setTimeout(() => {
        loadTrafficData();
        loadAQIData();
      }, 50);
    });

    // Trigger map resize after mount to fix layout issues
    setTimeout(() => {
      map.current?.resize();
    }, 200);

    return () => {
      map.current?.remove();
    };
  }, []);

  const loadTrafficData = async () => {
    if (!map.current || !map.current.isStyleLoaded()) return;

    const data = await api.getTrafficData();
    setTrafficData(data);

    if (!map.current || !map.current.isStyleLoaded()) return;
    if (map.current.getSource('traffic')) return;

    try {
      map.current.addSource('traffic', {
        type: 'geojson',
        data: data as GeoJSON.FeatureCollection,
      });

      if (!map.current.isStyleLoaded()) return;

      map.current.addLayer({
        id: 'traffic-lines',
        type: 'line',
        source: 'traffic',
        paint: {
          'line-color': [
            'match',
            ['get', 'congestion'],
            'low', '#22c55e',
            'moderate', '#eab308',
            'high', '#ef4444',
            '#6b7280'
          ],
          'line-width': 4,
          'line-opacity': 0.8,
        },
      });
    } catch (error) {
      console.error('Error loading traffic data:', error);
    }
  };

  const loadAQIData = async () => {
    if (!map.current || !map.current.isStyleLoaded()) return;

    const data = await api.getAQIData();
    setAqiData(data);

    if (!map.current || !map.current.isStyleLoaded()) return;
    if (map.current.getSource('aqi')) return;

    try {
      map.current.addSource('aqi', {
        type: 'geojson',
        data: data as GeoJSON.FeatureCollection,
      });

      if (!map.current.isStyleLoaded()) return;

      map.current.addLayer({
        id: 'aqi-circles',
        type: 'circle',
        source: 'aqi',
        paint: {
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['get', 'aqi'],
            0, 10,
            100, 20,
            200, 30
          ],
          'circle-color': [
            'interpolate',
            ['linear'],
            ['get', 'aqi'],
            0, '#00e400',
            50, '#ffff00',
            100, '#ff7e00',
            150, '#ff0000',
            200, '#8f3f97'
          ],
          'circle-opacity': 0.6,
          'circle-stroke-width': 2,
          'circle-stroke-color': '#ffffff',
        },
      });

      if (!map.current.isStyleLoaded()) return;

      map.current.on('click', 'aqi-circles', (e) => {
        if (!map.current || !map.current.isStyleLoaded()) return;
        if (!e.features || !e.features[0]) return;

        const properties = e.features[0].properties;
        const coordinates = (e.features[0].geometry as GeoJSON.Point).coordinates.slice();

        new maplibregl.Popup()
          .setLngLat([coordinates[0], coordinates[1]])
          .setHTML(`
            <div class="p-2">
              <h3 class="font-bold text-lg mb-2">${properties?.station}</h3>
              <p class="text-sm"><strong>AQI:</strong> ${properties?.aqi} (${properties?.category})</p>
              <p class="text-sm"><strong>PM2.5:</strong> ${properties?.pm25} µg/m³</p>
              <p class="text-sm"><strong>PM10:</strong> ${properties?.pm10} µg/m³</p>
            </div>
          `)
          .addTo(map.current);
      });

      map.current.on('mouseenter', 'aqi-circles', () => {
        if (map.current && map.current.isStyleLoaded()) {
          map.current.getCanvas().style.cursor = 'pointer';
        }
      });

      map.current.on('mouseleave', 'aqi-circles', () => {
        if (map.current && map.current.isStyleLoaded()) {
          map.current.getCanvas().style.cursor = '';
        }
      });
    } catch (error) {
      console.error('Error loading AQI data:', error);
    }
  };

  useEffect(() => {
    if (!map.current || !map.current.isStyleLoaded()) return;

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
  }, [activeLayer]);

  useEffect(() => {
    if (!map.current || !map.current.isStyleLoaded() || !simulationData) return;

    const source = map.current.getSource('traffic') as maplibregl.GeoJSONSource;
    if (source) {
      try {
        source.setData(simulationData.after as GeoJSON.FeatureCollection);
      } catch (error) {
        console.error('Error updating simulation data:', error);
      }
    }
  }, [simulationData]);

  return (
    <div
      ref={mapContainer}
      className="absolute inset-0 w-full h-full"
      style={{ zIndex: 0 }}
    />
  );
}

export default MapView;
