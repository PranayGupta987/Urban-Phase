import { useState } from 'react';
import MapView from './components/MapView';
import Sidebar from './components/Sidebar';
import MetricsPanel from './components/MetricsPanel';
import SimulationPanel from './components/SimulationPanel';
import { SimulationResponse } from './types';

function App() {
  const [simulationData, setSimulationData] = useState<SimulationResponse | null>(null);
  const [activeLayer, setActiveLayer] = useState<'traffic' | 'aqi'>('traffic');

  return (
    <div className="h-screen w-screen flex overflow-hidden bg-gray-900">
      <Sidebar activeLayer={activeLayer} onLayerChange={setActiveLayer} />

      <div className="flex-1 flex flex-col">
        <header className="bg-gray-800 text-white px-6 py-4 shadow-lg border-b border-gray-700">
          <h1 className="text-2xl font-bold tracking-tight">
            UrbanPulse
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            AI-Powered Sustainable City Twin
          </p>
        </header>

        <div className="flex-1 relative">
          <MapView
            activeLayer={activeLayer}
            simulationData={simulationData}
          />
        </div>

        <div className="absolute bottom-6 left-80 right-6 flex gap-4 pointer-events-none">
          <div className="pointer-events-auto">
            <MetricsPanel simulationData={simulationData} />
          </div>
          <div className="pointer-events-auto ml-auto">
            <SimulationPanel onSimulate={setSimulationData} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
