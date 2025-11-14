import type { ReactNode } from "react";
import { Activity, Wind, Gauge } from "lucide-react";
import { SimulationResponse } from "../types";

interface MetricsPanelProps {
  simulationData: SimulationResponse | null;
}

function MetricsPanel({ simulationData }: MetricsPanelProps) {
  if (!simulationData || !simulationData.metrics) {
    return null;
  }

  const m = simulationData.metrics;

  const avgSpeedBefore = m?.avg_speed_before ?? 0;
  const avgSpeedAfter = m?.avg_speed_after ?? 0;
  const congestionBefore = m?.avg_congestion_before ?? 0;
  const congestionAfter = m?.avg_congestion_after ?? 0;
  const aqiBefore = m?.aqi_before ?? 0;
  const aqiAfter = m?.aqi_after ?? 0;

  return (
    <div className="absolute right-8 top-[260px] w-[360px] rounded-2xl shadow-lg bg-white p-6">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Simulation Results</h2>

      <div className="grid grid-cols-2 gap-4">
        <MetricCard
          icon={<Gauge size={20} />}
          label="Before Avg Speed"
          value={avgSpeedBefore}
          unit="km/h"
        />
        <MetricCard
          icon={<Gauge size={20} />}
          label="After Avg Speed"
          value={avgSpeedAfter}
          unit="km/h"
        />

        <MetricCard
          icon={<Activity size={20} />}
          label="Before Congestion"
          value={congestionBefore}
          unit=""
        />
        <MetricCard
          icon={<Activity size={20} />}
          label="After Congestion"
          value={congestionAfter}
          unit=""
        />

        <MetricCard
          icon={<Wind size={20} />}
          label="Before AQI"
          value={aqiBefore}
          unit=""
        />
        <MetricCard
          icon={<Wind size={20} />}
          label="After AQI"
          value={aqiAfter}
          unit=""
        />
      </div>
    </div>
  );
}

interface MetricCardProps {
  icon: ReactNode;
  label: string;
  value: number;
  unit: string;
}

function MetricCard({ icon, label, value, unit }: MetricCardProps) {
  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <div className="flex items-center gap-2 mb-2 text-gray-600">
        {icon}
        <span className="text-sm font-medium">{label}</span>
      </div>

      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-bold text-gray-800">
          {value.toFixed(1)}
        </span>
        {unit && <span className="text-xs text-gray-500">{unit}</span>}
      </div>
    </div>
  );
}

export default MetricsPanel;
