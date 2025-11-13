import { Cloud, Wind, Droplets, Thermometer } from 'lucide-react';

interface MetricCardsProps {
  weather: {
    temperature: number;
    humidity: number;
    wind_speed: number;
    conditions: string;
  } | null;
  avgTraffic: number;
  avgAQI: number;
}

export function MetricCards({ weather, avgTraffic, avgAQI }: MetricCardsProps) {
  const getAQIColor = (aqi: number) => {
    if (aqi <= 50) return 'bg-green-100 text-green-800';
    if (aqi <= 100) return 'bg-yellow-100 text-yellow-800';
    if (aqi <= 150) return 'bg-orange-100 text-orange-800';
    return 'bg-red-100 text-red-800';
  };

  const getTrafficColor = (traffic: number) => {
    if (traffic <= 40) return 'bg-green-100 text-green-800';
    if (traffic <= 70) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center gap-2 mb-2">
          <Thermometer className="w-5 h-5 text-blue-600" />
          <span className="text-sm text-gray-600">Temperature</span>
        </div>
        <div className="text-2xl font-bold text-gray-900">
          {weather?.temperature.toFixed(1) || '--'}°C
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center gap-2 mb-2">
          <Droplets className="w-5 h-5 text-blue-600" />
          <span className="text-sm text-gray-600">Humidity</span>
        </div>
        <div className="text-2xl font-bold text-gray-900">
          {weather?.humidity.toFixed(0) || '--'}%
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center gap-2 mb-2">
          <Wind className="w-5 h-5 text-blue-600" />
          <span className="text-sm text-gray-600">Avg Traffic</span>
        </div>
        <div className={`text-2xl font-bold rounded px-2 ${getTrafficColor(avgTraffic)}`}>
          {avgTraffic.toFixed(1)}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center gap-2 mb-2">
          <Cloud className="w-5 h-5 text-blue-600" />
          <span className="text-sm text-gray-600">Avg AQI</span>
        </div>
        <div className={`text-2xl font-bold rounded px-2 ${getAQIColor(avgAQI)}`}>
          {avgAQI.toFixed(0)}
        </div>
      </div>
    </div>
  );
}
