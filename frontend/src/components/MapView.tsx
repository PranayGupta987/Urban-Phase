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
      loadTrafficData();
      loadAQIData();
    });

    return () => {
      map.current?.remove();
    };
  }, []);

  const loadTrafficData = async () => {
    const data = await api.getTrafficData();
    setTrafficData(data);

    if (map.current && !map.current.getSource('traffic')) {
      map.current.addSource('traffic', {
        type: 'geojson',
        data: data as GeoJSON.FeatureCollection,
      });

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
    }
  };

  const loadAQIData = async () => {
    const data = await api.getAQIData();
    setAqiData(data);

    if (map.current && !map.current.getSource('aqi')) {
      map.current.addSource('aqi', {
        type: 'geojson',
        data: data as GeoJSON.FeatureCollection,
      });

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

      map.current.on('click', 'aqi-circles', (e) => {
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
          .addTo(map.current!);
      });

      map.current.on('mouseenter', 'aqi-circles', () => {
        if (map.current) map.current.getCanvas().style.cursor = 'pointer';
      });

      map.current.on('mouseleave', 'aqi-circles', () => {
        if (map.current) map.current.getCanvas().style.cursor = '';
      });
    }
  };

  useEffect(() => {
    if (!map.current) return;

    if (activeLayer === 'traffic') {
      map.current.setLayoutProperty('traffic-lines', 'visibility', 'visible');
      map.current.setLayoutProperty('aqi-circles', 'visibility', 'none');
    } else {
      map.current.setLayoutProperty('traffic-lines', 'visibility', 'none');
      map.current.setLayoutProperty('aqi-circles', 'visibility', 'visible');
    }
  }, [activeLayer]);

  useEffect(() => {
    if (!map.current || !simulationData) return;

    const source = map.current.getSource('traffic') as maplibregl.GeoJSONSource;
    if (source) {
      source.setData(simulationData.after as GeoJSON.FeatureCollection);
    }
  }, [simulationData]);

  return <div ref={mapContainer} className="absolute inset-0" />;
}

export default MapView;
