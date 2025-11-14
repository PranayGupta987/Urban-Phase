import { Layers, Wind, MapPin } from "lucide-react";

interface SidebarProps {
  activeLayer: "traffic" | "aqi";
  onLayerChange: (layer: "traffic" | "aqi") => void;
}

function Sidebar({ activeLayer, onLayerChange }: SidebarProps) {
  return (
    <div className="w-72 bg-[#0f172a] text-white flex flex-col p-6 h-full">
      <div className="mb-8">
        <div className="text-xl font-bold tracking-tight">UrbanPulse</div>
        <p className="text-xs text-slate-400 mt-1">
          AI-powered sustainable city twin
        </p>
      </div>

      <div className="mb-6">
        <div className="flex items-center gap-2 mb-2">
          <Layers size={20} className="text-primary-400" />
          <h2 className="text-lg font-semibold">Map Layers</h2>
        </div>
        <p className="text-xs text-slate-400">Toggle data visualization</p>
      </div>

      <div className="space-y-3">
        <button
          onClick={() => onLayerChange("traffic")}
          className={`w-full flex items-center gap-3 p-4 rounded-lg transition-colors ${
            activeLayer === "traffic"
              ? "bg-primary-600 shadow-lg"
              : "bg-slate-800 hover:bg-slate-700"
          }`}
        >
          <MapPin size={20} />
          <div className="text-left flex-1">
            <div className="font-medium">Traffic Flow</div>
            <div className="text-xs text-slate-300">Real-time congestion</div>
          </div>
        </button>

        <button
          onClick={() => onLayerChange("aqi")}
          className={`w-full flex items-center gap-3 p-4 rounded-lg transition-colors ${
            activeLayer === "aqi"
              ? "bg-primary-600 shadow-lg"
              : "bg-slate-800 hover:bg-slate-700"
          }`}
        >
          <Wind size={20} />
          <div className="text-left flex-1">
            <div className="font-medium">Air Quality</div>
            <div className="text-xs text-slate-300">AQI monitoring</div>
          </div>
        </button>
      </div>

      <div className="mt-8 p-4 bg-slate-900 rounded-lg border border-slate-700">
        <h3 className="font-semibold mb-3 text-sm">Legend</h3>

        <div className="space-y-2 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-green-500 rounded" />
            <span className="text-slate-300">Low congestion</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-yellow-400 rounded" />
            <span className="text-slate-300">Moderate</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-1 bg-red-500 rounded" />
            <span className="text-slate-300">High congestion</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;
