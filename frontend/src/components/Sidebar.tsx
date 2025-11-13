import { Layers, Wind, MapPin } from 'lucide-react';

interface SidebarProps {
  activeLayer: 'traffic' | 'aqi';
  onLayerChange: (layer: 'traffic' | 'aqi') => void;
}

function Sidebar({ activeLayer, onLayerChange }: SidebarProps) {
  return (
    <div className="w-64 bg-gray-800 text-white p-4 shadow-xl border-r border-gray-700 flex flex-col">
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <Layers size={20} className="text-primary-400" />
          <h2 className="text-lg font-semibold">Map Layers</h2>
        </div>
        <p className="text-xs text-gray-400">Toggle data visualization</p>
      </div>

      <div className="space-y-3">
        <button
          onClick={() => onLayerChange('traffic')}
          className={`w-full flex items-center gap-3 p-4 rounded-lg transition-all ${
            activeLayer === 'traffic'
              ? 'bg-primary-600 shadow-lg'
              : 'bg-gray-700 hover:bg-gray-600'
          }`}
        >
          <MapPin size={20} />
          <div className="text-left flex-1">
            <div className="font-medium">Traffic Flow</div>
            <div className="text-xs text-gray-300">Real-time congestion</div>
          </div>
        </button>

        <button
          onClick={() => onLayerChange('aqi')}
          className={`w-full flex items-center gap-3 p-4 rounded-lg transition-all ${
            activeLayer === 'aqi'
              ? 'bg-primary-600 shadow-lg'
              : 'bg-gray-700 hover:bg-gray-600'
          }`}
        >
          <Wind size={20} />
          <div className="text-left flex-1">
            <div className="font-medium">Air Quality</div>
            <div className="text-xs text-gray-300">AQI monitoring</div>
          </div>
        </button>
      </div>

      <div className="mt-8 p-4 bg-gray-900 rounded-lg">
        <h3 className="font-semibold mb-3 text-sm">Legend</h3>
        {activeLayer === 'traffic' ? (
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-4 h-1 bg-green-500 rounded"></div>
              <span className="text-gray-300">Low congestion</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-1 bg-yellow-500 rounded"></div>
              <span className="text-gray-300">Moderate</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-1 bg-red-500 rounded"></div>
              <span className="text-gray-300">High congestion</span>
            </div>
          </div>
        ) : (
          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-gray-300">Good (0-50)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
              <span className="text-gray-300">Moderate (51-100)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
              <span className="text-gray-300">Unhealthy (101-150)</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Sidebar;
