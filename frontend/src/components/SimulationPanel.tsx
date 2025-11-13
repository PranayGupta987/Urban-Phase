import { useState } from 'react';
import { Play, RotateCcw } from 'lucide-react';
import { api } from '../services/api';
import { SimulationResponse } from '../types';

interface SimulationPanelProps {
  onSimulate: (data: SimulationResponse | null) => void;
}

function SimulationPanel({ onSimulate }: SimulationPanelProps) {
  const [vehicleReduction, setVehicleReduction] = useState(30);
  const [loading, setLoading] = useState(false);

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const result = await api.runSimulation({ vehicle_reduction: vehicleReduction });
      onSimulate(result);
    } catch (error) {
      console.error('Simulation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    onSimulate(null);
    setVehicleReduction(30);
  };

  return (
    <div className="bg-white rounded-xl shadow-2xl p-6 w-96">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Scenario Simulation</h2>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Vehicle Reduction
        </label>
        <div className="flex items-center gap-4">
          <input
            type="range"
            min="0"
            max="100"
            value={vehicleReduction}
            onChange={(e) => setVehicleReduction(Number(e.target.value))}
            className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
          />
          <span className="text-2xl font-bold text-primary-600 w-16 text-right">
            {vehicleReduction}%
          </span>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Simulate reduction in vehicle traffic
        </p>
      </div>

      <div className="space-y-3">
        <button
          onClick={handleSimulate}
          disabled={loading}
          className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors"
        >
          <Play size={18} />
          {loading ? 'Running...' : 'Run Simulation'}
        </button>

        <button
          onClick={handleReset}
          className="w-full bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors"
        >
          <RotateCcw size={18} />
          Reset
        </button>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">About</h3>
        <p className="text-xs text-blue-800">
          This simulation predicts the impact of reduced vehicle traffic on congestion, emissions, and air quality using AI models.
        </p>
      </div>
    </div>
  );
}

export default SimulationPanel;
