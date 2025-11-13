import { Activity, Wind, TrendingDown, Gauge } from 'lucide-react';
import { SimulationResponse } from '../types';

interface MetricsPanelProps {
  simulationData: SimulationResponse | null;
}

function MetricsPanel({ simulationData }: MetricsPanelProps) {
  if (!simulationData) return null;

  const { metrics } = simulationData;

  return (
    <div className="bg-white rounded-xl shadow-2xl p-6 max-w-2xl">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Simulation Results</h2>

      <div className="grid grid-cols-2 gap-4">
        <MetricCard
          icon={<Gauge size={20} />}
          label="Avg Speed"
          before={metrics.before.avg_speed}
          after={metrics.after.avg_speed}
          unit="km/h"
          improve={metrics.after.avg_speed > metrics.before.avg_speed}
        />

        <MetricCard
          icon={<Activity size={20} />}
          label="Congestion Index"
          before={metrics.before.congestion_index}
          after={metrics.after.congestion_index}
          unit=""
          improve={metrics.after.congestion_index < metrics.before.congestion_index}
        />

        <MetricCard
          icon={<TrendingDown size={20} />}
          label="CO₂ Reduction"
          before={0}
          after={metrics.after.co2_reduction}
          unit="%"
          improve={true}
          showDelta={false}
        />

        <MetricCard
          icon={<Wind size={20} />}
          label="AQI Improvement"
          before={0}
          after={metrics.after.aqi_improvement}
          unit="%"
          improve={true}
          showDelta={false}
        />
      </div>
    </div>
  );
}

interface MetricCardProps {
  icon: React.ReactNode;
  label: string;
  before: number;
  after: number;
  unit: string;
  improve: boolean;
  showDelta?: boolean;
}

function MetricCard({ icon, label, before, after, unit, improve, showDelta = true }: MetricCardProps) {
  const delta = after - before;
  const percentChange = before !== 0 ? ((delta / before) * 100) : 0;

  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <div className="flex items-center gap-2 mb-2 text-gray-600">
        {icon}
        <span className="text-sm font-medium">{label}</span>
      </div>

      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-bold text-gray-800">
          {after.toFixed(1)}{unit}
        </span>
        {showDelta && (
          <span className={`text-sm font-medium ${improve ? 'text-green-600' : 'text-red-600'}`}>
            {improve ? '↑' : '↓'} {Math.abs(percentChange).toFixed(1)}%
          </span>
        )}
      </div>

      {showDelta && (
        <div className="text-xs text-gray-500 mt-1">
          From {before.toFixed(1)}{unit}
        </div>
      )}
    </div>
  );
}

export default MetricsPanel;
