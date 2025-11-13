import { Building2, Map, TrendingDown, CloudRain } from 'lucide-react';

interface HomeProps {
  onNavigateToMap: () => void;
}

export function Home({ onNavigateToMap }: HomeProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Building2 className="w-12 h-12 text-blue-600" />
            <h1 className="text-5xl font-bold text-gray-900">UrbanPulse</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-Powered Sustainable City Twin
          </p>
          <p className="text-lg text-gray-500 mt-2 max-w-3xl mx-auto">
            Visualize, simulate, and optimize urban environments for a sustainable future
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-center w-14 h-14 bg-blue-100 rounded-lg mb-4">
              <Map className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Real-Time Monitoring</h3>
            <p className="text-gray-600">
              Track traffic patterns, air quality, and weather conditions in real-time with
              interactive visualizations
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-center w-14 h-14 bg-green-100 rounded-lg mb-4">
              <TrendingDown className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Smart Simulations</h3>
            <p className="text-gray-600">
              Run AI-powered scenarios to predict the impact of traffic reduction and
              green zone initiatives
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-center w-14 h-14 bg-teal-100 rounded-lg mb-4">
              <CloudRain className="w-8 h-8 text-teal-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Data-Driven Insights</h3>
            <p className="text-gray-600">
              Make informed decisions with ML-powered predictions and comprehensive
              environmental analytics
            </p>
          </div>
        </div>

        <div className="text-center">
          <button
            onClick={onNavigateToMap}
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold text-lg py-4 px-8 rounded-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          >
            Launch City Twin
          </button>
        </div>

        <div className="mt-16 bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            How It Works
          </h2>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
                1
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Load Data</h4>
              <p className="text-sm text-gray-600">
                Real-time traffic, AQI, and weather data
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
                2
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Visualize</h4>
              <p className="text-sm text-gray-600">
                Interactive maps with heatmaps and layers
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
                3
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Simulate</h4>
              <p className="text-sm text-gray-600">
                Test sustainability interventions
              </p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-3">
                4
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Optimize</h4>
              <p className="text-sm text-gray-600">
                Make data-driven policy decisions
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
