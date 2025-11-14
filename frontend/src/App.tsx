import { useState } from "react";
import MapView from "./components/MapView";
import Sidebar from "./components/Sidebar";
import MetricsPanel from "./components/MetricsPanel";
import SimulationPanel from "./components/SimulationPanel";
import { SimulationResponse } from "./types";

function App() {
  const [simulationData, setSimulationData] = useState<SimulationResponse | null>(null);
  const [activeLayer, setActiveLayer] = useState<"traffic" | "aqi">("traffic");
  const [showResults, setShowResults] = useState(false);

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      <Sidebar activeLayer={activeLayer} onLayerChange={setActiveLayer} />

      <div className="flex-1 relative bg-slate-900">
        <MapView activeLayer={activeLayer} simulationData={simulationData} />

        <SimulationPanel
          setSimulationData={setSimulationData}
          setShowResults={setShowResults}
        />

        {showResults && <MetricsPanel simulationData={simulationData} />}
      </div>
    </div>
  );
}

export default App;
