import { Layers, Wind, MapPin } from 'lucide-react';

interface SidebarProps {
  activeLayer: 'traffic' | 'aqi';
  onLayerChange: (layer: 'traffic' | 'aqi') => void;
}

function Sidebar({ activeLayer, onLayerChange }: SidebarProps) {
  return (
    <aside className="w-68 bg-slate-950/90 text-slate-100 px-6 py-6 border-r border-slate-800/80 shadow-xl shadow-black/50 backdrop-blur-2xl flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Layers size={20} className="text-primary-300" />
            <h2 className="text-sm font-semibold tracking-wide uppercase text-slate-300">Layers</h2>
          </div>
          <p className="text-[11px] text-slate-500">Switch between traffic and air quality views.</p>
        </div>
      </div>

      <div className="bg-slate-900/60 border border-slate-700/70 rounded-2xl p-2 flex items-center gap-1">
        <button
          onClick={() => onLayerChange('traffic')}
          className={`flex-1 flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium transition-all duration-150 ${
            activeLayer === 'traffic'
              ? 'bg-gradient-to-tr from-primary-600 to-primary-400 text-white shadow-md shadow-primary-900/60'
              : 'text-slate-400 hover:bg-slate-800/90'
          }`}
        >
          <MapPin size={16} className={activeLayer === 'traffic' ? 'text-white' : 'text-slate-500'} />
          <span>Traffic</span>
        </button>

        <button
          onClick={() => onLayerChange('aqi')}
          className={`flex-1 flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium transition-all duration-150 ${
            activeLayer === 'aqi'
              ? 'bg-gradient-to-tr from-primary-600 to-primary-400 text-white shadow-md shadow-primary-900/60'
              : 'text-slate-400 hover:bg-slate-800/90'
          }`}
        >
          <Wind size={16} className={activeLayer === 'aqi' ? 'text-white' : 'text-slate-500'} />
          <span>Air Quality</span>
        </button>
      </div>

      <div className="mt-2 p-4 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-inner shadow-black/40">
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
    </aside>
  );
}

export default Sidebar;
