import { Play, RotateCcw, Layers } from 'lucide-react';
import { LayerType } from '../types';

interface ControlPanelProps {
  trafficReduction: number;
  onTrafficReductionChange: (value: number) => void;
  greenZones: boolean;
  onGreenZonesChange: (value: boolean) => void;
  onRunSimulation: () => void;
  onReset: () => void;
  activeLayer: LayerType;
  onLayerChange: (layer: LayerType) => void;
  isSimulating: boolean;
}

export function ControlPanel({
  trafficReduction,
  onTrafficReductionChange,
  greenZones,
  onGreenZonesChange,
  onRunSimulation,
  onReset,
  activeLayer,
  onLayerChange,
  isSimulating,
}: ControlPanelProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-4">Simulation Controls</h2>

        <div className="space-y-4">
          <div>
            <label className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                Traffic Reduction
              </span>
              <span className="text-lg font-bold text-blue-600">
                {trafficReduction}%
              </span>
            </label>
            <input
              type="range"
              min="0"
              max="100"
              value={trafficReduction}
              onChange={(e) => onTrafficReductionChange(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>0%</span>
              <span>50%</span>
              <span>100%</span>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="greenZones"
              checked={greenZones}
              onChange={(e) => onGreenZonesChange(e.target.checked)}
              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label htmlFor="greenZones" className="text-sm font-medium text-gray-700">
              Apply Green Zones
            </label>
          </div>

          <div className="flex gap-2">
            <button
              onClick={onRunSimulation}
              disabled={isSimulating}
              className="flex-1 flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              <Play className="w-5 h-5" />
              {isSimulating ? 'Running...' : 'Run Simulation'}
            </button>
            <button
              onClick={onReset}
              className="flex items-center justify-center bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              <RotateCcw className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      <div className="border-t pt-4">
        <div className="flex items-center gap-2 mb-3">
          <Layers className="w-5 h-5 text-gray-700" />
          <h3 className="text-sm font-bold text-gray-900">Map Layers</h3>
        </div>
        <div className="space-y-2">
          <button
            onClick={() => onLayerChange('traffic')}
            className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
              activeLayer === 'traffic'
                ? 'bg-blue-100 text-blue-800 font-semibold'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Traffic Heatmap
          </button>
          <button
            onClick={() => onLayerChange('aqi')}
            className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
              activeLayer === 'aqi'
                ? 'bg-blue-100 text-blue-800 font-semibold'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Air Quality Index
          </button>
        </div>
      </div>
    </div>
  );
}
