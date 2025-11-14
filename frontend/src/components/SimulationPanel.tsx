import { useState } from 'react';
import { Play, RotateCcw, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import { SimulationResponse } from '../types';

interface SimulationPanelProps {
  setSimulationData: (data: SimulationResponse | null) => void;
  setShowResults: (value: boolean) => void;
}

function SimulationPanel({ setSimulationData, setShowResults }: SimulationPanelProps) {
  const [vehicleReduction, setVehicleReduction] = useState(30);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSimulate = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('[SimulationPanel] Calling runSimulation with:', {
        vehicle_reduction: vehicleReduction,
      });
      const result = await api.runSimulation({
        vehicle_reduction: vehicleReduction,
      });
      console.log('[SimulationPanel] Simulation response:', result);
      setSimulationData(result);
      setShowResults(true);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Simulation failed';
      setError(errorMessage);
      console.error('[SimulationPanel] Simulation failed:', err);
      setShowResults(false);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    console.log('[SimulationPanel] Resetting simulation');
    setSimulationData(null);
    setShowResults(false);
    setVehicleReduction(30);
    setError(null);
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
            disabled={loading}
          />
          <span className="text-2xl font-bold text-primary-600 w-16 text-right">
            {vehicleReduction}%
          </span>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Simulate reduction in vehicle traffic
        </p>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <div className="space-y-3">
        <button
          onClick={handleSimulate}
          disabled={loading}
          className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors"
        >
          {loading ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              Running...
            </>
          ) : (
            <>
              <Play size={18} />
              Run Simulation
            </>
          )}
        </button>

        <button
          onClick={handleReset}
          disabled={loading}
          className="w-full bg-gray-200 hover:bg-gray-300 disabled:bg-gray-100 text-gray-700 font-medium py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors"
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
