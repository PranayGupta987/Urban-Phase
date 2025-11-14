import { Activity, Wind, TrendingDown, Gauge } from 'lucide-react';
import { SimulationResponse } from '../types';
import styles from './MetricsPanel.module.css';

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
    <div className={styles.panelRoot}>
      <div className={styles.header}>
        <h2 className={styles.title}>Simulation Results</h2>
      </div>

      <div className={styles.grid}>
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
  icon: React.ReactNode;
  label: string;
  value: number;
  unit: string;
}

function MetricCard({ icon, label, value, unit }: MetricCardProps) {
  return (
    <div className={styles.card}>
      <div className={styles.cardHeader}>
        {icon}
        <span className={styles.label}>{label}</span>
      </div>

      <div className={styles.valueRow}>
        <span className={styles.value}>{value.toFixed(1)}</span>
        {unit && <span className={styles.unit}>{unit}</span>}
      </div>
    </div>
  );
}

export default MetricsPanel;
