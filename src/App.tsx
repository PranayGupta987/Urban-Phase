import { useState } from 'react';
import { Home } from './pages/Home';
import { MapView } from './pages/MapView';

type Page = 'home' | 'map';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home');

  return (
    <>
      {currentPage === 'home' && (
        <Home onNavigateToMap={() => setCurrentPage('map')} />
      )}
      {currentPage === 'map' && (
        <MapView onNavigateHome={() => setCurrentPage('home')} />
      )}
    </>
  );
}

export default App;
