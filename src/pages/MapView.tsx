import { useEffect, useState } from 'react';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import { CityMap } from '../components/CityMap';
import { ControlPanel } from '../components/ControlPanel';
import { MetricCards } from '../components/MetricCards';
import { api } from '../services/api';
import { TrafficData, AQIData, WeatherData, LayerType, SimulationMetrics } from '../types';

interface MapViewProps {
  onNavigateHome: () => void;
}

export function MapView({ onNavigateHome }: MapViewProps) {
  const [trafficData, setTrafficData] = useState<TrafficData | null>(null);
  const [aqiData, setAQIData] = useState<AQIData | null>(null);
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [originalTrafficData, setOriginalTrafficData] = useState<TrafficData | null>(null);
  const [originalAQIData, setOriginalAQIData] = useState<AQIData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const [trafficReduction, setTrafficReduction] = useState(30);
  const [greenZones, setGreenZones] = useState(false);
  const [activeLayer, setActiveLayer] = useState<LayerType>('traffic');

  const [simulationResults, setSimulationResults] = useState<SimulationMetrics | null>(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [traffic, aqi, weather] = await Promise.all([
        api.getTrafficData(),
        api.getAQIData(),
        api.getWeatherData(),
      ]);

      setTrafficData(traffic);
      setAQIData(aqi);
      setWeatherData(weather);
      setOriginalTrafficData(traffic);
      setOriginalAQIData(aqi);
    } catch (err) {
      setError('Failed to load city data. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunSimulation = async () => {
    setIsSimulating(true);
    setError(null);
    try {
      const results = await api.runSimulation(trafficReduction, greenZones);
      setSimulationResults(results);
      setTrafficData(results.geojson_layers.traffic);
      setAQIData(results.geojson_layers.aqi);
    } catch (err) {
      setError('Simulation failed. Please try again.');
      console.error(err);
    } finally {
      setIsSimulating(false);
    }
  };

  const handleReset = () => {
    setTrafficData(originalTrafficData);
    setAQIData(originalAQIData);
    setSimulationResults(null);
    setTrafficReduction(30);
    setGreenZones(false);
  };

  const calculateAvgTraffic = (data: TrafficData | null) => {
    if (!data || !data.features.length) return 0;
    const sum = data.features.reduce(
      (acc, f) => acc + f.properties.traffic_volume,
      0
    );
    return sum / data.features.length;
  };

  const calculateAvgAQI = (data: AQIData | null) => {
    if (!data || !data.features.length) return 0;
    const sum = data.features.reduce((acc, f) => acc + f.properties.aqi, 0);
    return sum / data.features.length;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
          <p className="text-lg text-gray-600">Loading city data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={onNavigateHome}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-6 h-6 text-gray-700" />
            </button>
            <h1 className="text-2xl font-bold text-gray-900">UrbanPulse City Twin</h1>
          </div>
          <div className="text-sm text-gray-600">
            {weatherData?.location.name || 'New York'}
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5" />
            {error}
          </div>
        )}

        <MetricCards
          weather={weatherData?.current || null}
          avgTraffic={calculateAvgTraffic(trafficData)}
          avgAQI={calculateAvgAQI(aqiData)}
        />

        {simulationResults && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
            <h3 className="font-bold text-blue-900 mb-2">Simulation Results</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-blue-700">Traffic Reduced:</span>
                <p className="font-bold text-blue-900">
                  {simulationResults.improvements.traffic_reduction.toFixed(1)}%
                </p>
              </div>
              <div>
                <span className="text-blue-700">AQI Improved:</span>
                <p className="font-bold text-blue-900">
                  -{simulationResults.improvements.aqi_reduction.toFixed(1)}
                </p>
              </div>
              <div>
                <span className="text-blue-700">New Avg Traffic:</span>
                <p className="font-bold text-blue-900">
                  {simulationResults.simulated_metrics.avg_traffic.toFixed(1)}
                </p>
              </div>
              <div>
                <span className="text-blue-700">New Avg AQI:</span>
                <p className="font-bold text-blue-900">
                  {simulationResults.simulated_metrics.avg_aqi.toFixed(0)}
                </p>
              </div>
            </div>
          </div>
        )}

        <div className="grid lg:grid-cols-4 gap-6">
          <div className="lg:col-span-3 h-[600px]">
            <CityMap
              trafficData={trafficData}
              aqiData={aqiData}
              activeLayer={activeLayer}
            />
          </div>
          <div className="lg:col-span-1">
            <ControlPanel
              trafficReduction={trafficReduction}
              onTrafficReductionChange={setTrafficReduction}
              greenZones={greenZones}
              onGreenZonesChange={setGreenZones}
              onRunSimulation={handleRunSimulation}
              onReset={handleReset}
              activeLayer={activeLayer}
              onLayerChange={setActiveLayer}
              isSimulating={isSimulating}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
