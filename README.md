# UrbanPulse – AI-Powered Sustainable City Twin

A full-stack application for visualizing, simulating, and optimizing urban environments using real-time data and AI-powered predictions.

## Features

- **Real-Time Monitoring**: Track traffic patterns, air quality index (AQI), and weather conditions
- **Interactive Visualization**: Mapbox + Deck.gl powered maps with heatmaps and layered data
- **AI-Powered Predictions**: LightGBM models for AQI forecasting
- **Smart Simulations**: Test traffic reduction scenarios and green zone impacts
- **Data-Driven Insights**: Comprehensive environmental analytics and metrics

## Architecture

### Backend (FastAPI)
- FastAPI REST API with async support
- Redis caching for performance optimization
- LightGBM ML models for predictions
- Demo mode with fallback to local JSON data
- Extensible API client architecture

### Frontend (React + Vite)
- Modern React with TypeScript
- Mapbox GL JS for base maps
- Deck.gl for data visualization layers
- Tailwind CSS for styling
- Responsive design with mobile support

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── routes/         # API endpoints
│   │   ├── clients.py      # API client stubs
│   │   ├── cache.py        # Redis caching
│   │   ├── config.py       # Configuration
│   │   └── main.py         # FastAPI application
│   ├── ml/
│   │   ├── model.py        # ML model loader
│   │   ├── train.py        # Model training
│   │   └── synthetic_data.py
│   ├── demo/               # Demo JSON data
│   ├── Dockerfile
│   └── requirements.txt
├── src/
│   ├── components/         # React components
│   ├── pages/              # Page components
│   ├── services/           # API service
│   ├── types/              # TypeScript types
│   └── App.tsx
├── docker-compose.yml
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- OR Node.js 20+ and Python 3.11+ (for local development)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd urbanpulse

# Copy environment files
cp .env.example .env
cp backend/.env.example backend/.env

# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Train ML models (optional)
python -m ml.train

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
# From project root
npm install

# Copy environment file
cp .env.example .env

# Update VITE_API_URL in .env
echo "VITE_API_URL=http://localhost:8000" >> .env

# Run development server
npm run dev
```

## Configuration

### Backend Environment Variables

```bash
# Redis (optional, uses in-memory cache if not available)
REDIS_URL=redis://localhost:6379

# Demo mode (uses local JSON files instead of real APIs)
DEMO_MODE=true

# API Keys (only needed when DEMO_MODE=false)
TRAFFIC_API_KEY=your_traffic_api_key
AQI_API_KEY=your_aqi_api_key
WEATHER_API_KEY=your_weather_api_key

# City Configuration
CITY_LAT=40.7128
CITY_LON=-74.0060
CITY_NAME=NewYork
```

### Frontend Environment Variables

```bash
# Backend API URL
VITE_API_URL=http://localhost:8000

# Mapbox Token (required for maps)
VITE_MAPBOX_TOKEN=your_mapbox_token
```

**Note**: To use the map visualization, you need a Mapbox access token. Get one free at [mapbox.com](https://account.mapbox.com/access-tokens/).

## API Endpoints

### Data Endpoints
- `GET /data/traffic` - Get traffic data (GeoJSON)
- `GET /data/aqi` - Get air quality index data (GeoJSON)
- `GET /data/weather` - Get weather data

### Prediction Endpoint
- `POST /predict` - Predict AQI based on environmental features

### Simulation Endpoint
- `POST /simulate` - Run traffic reduction simulation

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Demo Mode

The application includes demo mode with synthetic data:
- Pre-generated traffic patterns for New York City
- Sample AQI measurements
- Mock weather data
- No external API keys required

Demo data files are located in `backend/demo/`:
- `traffic.json` - Traffic data in GeoJSON format
- `aqi.json` - Air quality measurements
- `weather.json` - Weather conditions

## ML Model Training

Train the AQI prediction model:

```bash
cd backend
python -m ml.train
```

This generates a LightGBM model saved to `backend/ml/models/aqi_model.pkl`.

The model uses synthetic data by default. For production, replace the training data in `ml/synthetic_data.py` with real historical data.

## Usage

1. **Launch the Application**: Navigate to home page
2. **Click "Launch City Twin"**: Opens the interactive map view
3. **View Real-Time Data**: See current traffic and AQI on the map
4. **Switch Layers**: Toggle between Traffic Heatmap and AQI visualization
5. **Run Simulations**:
   - Adjust traffic reduction slider (0-100%)
   - Optionally enable green zones
   - Click "Run Simulation"
   - View predicted improvements in metrics
6. **Analyze Results**: Compare original vs simulated metrics

## Technology Stack

### Backend
- FastAPI - Modern Python web framework
- LightGBM - Gradient boosting for ML predictions
- Redis - Caching layer
- httpx - Async HTTP client
- Uvicorn - ASGI server

### Frontend
- React 18 - UI framework
- TypeScript - Type safety
- Vite - Build tool
- Mapbox GL JS - Map rendering
- Deck.gl - WebGL-powered visualization
- Tailwind CSS - Utility-first CSS
- Lucide React - Icon library

### Infrastructure
- Docker - Containerization
- Docker Compose - Multi-container orchestration
- Nginx - Frontend web server

## Development

### Backend Development

```bash
cd backend

# Run tests
pytest tests/

# Format code
black app/ ml/

# Lint
flake8 app/ ml/
```

### Frontend Development

```bash
# Type checking
npm run typecheck

# Linting
npm run lint

# Build for production
npm run build
```

## Production Deployment

1. Set `DEMO_MODE=false` in backend/.env
2. Add real API keys for traffic, AQI, and weather services
3. Configure Redis instance
4. Add Mapbox token to frontend .env
5. Build and deploy using Docker:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Extending the Application

### Adding New Data Sources

1. Create a new client in `backend/app/clients.py`
2. Add demo data to `backend/demo/`
3. Create new route in `backend/app/routes/`
4. Update frontend types in `src/types/`
5. Add API call in `src/services/api.ts`

### Adding New Visualizations

1. Create new Deck.gl layer in `src/components/CityMap.tsx`
2. Add layer controls to `src/components/ControlPanel.tsx`
3. Update layer type in `src/types/index.ts`

## Troubleshooting

**Maps not loading**: Ensure VITE_MAPBOX_TOKEN is set in .env

**Backend connection error**: Check VITE_API_URL matches backend port

**Redis connection failed**: Application works without Redis (uses in-memory cache)

**Missing ML model**: Run `python -m ml.train` in backend directory

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.
