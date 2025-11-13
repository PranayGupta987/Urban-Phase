# UrbanPulse – AI-Powered Sustainable City Twin

UrbanPulse is an interactive digital twin platform that simulates urban sustainability scenarios using real-time traffic and air quality data. Built for hackathons and rapid prototyping, it demonstrates how AI can help cities optimize for reduced emissions and improved livability.

## 🎯 Project Goal

Create an intelligent city simulation platform that:
- Visualizes real-time traffic flow and air quality data
- Simulates the impact of sustainability interventions
- Provides actionable insights for urban planners
- Demonstrates AI's potential in smart city development

## 🚀 Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **MapLibre GL JS** for interactive map visualization
- **TailwindCSS** for modern, responsive design
- **Lucide React** for beautiful icons

### Backend
- **FastAPI** (Python) for high-performance API
- **Pydantic** for data validation
- **Uvicorn** ASGI server
- Modular architecture with services, routers, and models

### Infrastructure
- **Docker** & **Docker Compose** for containerization
- **Nginx** for frontend serving in production

## 📁 Project Structure

```
UrbanPulse/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── MapView.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── MetricsPanel.tsx
│   │   │   └── SimulationPanel.tsx
│   │   ├── services/        # API integration
│   │   │   └── api.ts
│   │   ├── types/           # TypeScript definitions
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── backend/                  # FastAPI backend application
│   ├── routers/             # API route handlers
│   │   ├── status.py
│   │   ├── data.py
│   │   └── simulate.py
│   ├── services/            # Business logic
│   │   ├── traffic_service.py
│   │   ├── aqi_service.py
│   │   └── simulation_service.py
│   ├── models/              # Data models
│   │   └── schemas.py
│   ├── ml/                  # Machine learning models
│   │   ├── placeholder_model.py
│   │   └── README.md
│   ├── utils/               # Utilities
│   │   └── cache.py
│   ├── data/                # Mock data
│   │   ├── traffic.geojson
│   │   └── aqi.geojson
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

## 🏃 Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone and navigate to the project**
   ```bash
   cd UrbanPulse
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Verify it's running**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000

## 📡 API Endpoints

### Status Endpoint
```
GET /status
```
Returns the health status of the API.

**Response:**
```json
{
  "status": "ok"
}
```

### Traffic Data
```
GET /data/traffic
```
Returns real-time traffic flow data as GeoJSON.

**Response:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "LineString",
        "coordinates": [...]
      },
      "properties": {
        "speed": 25,
        "congestion": "moderate",
        "volume": 1200
      }
    }
  ]
}
```

### Air Quality Data
```
GET /data/aqi
```
Returns air quality index (AQI) data from monitoring stations.

**Response:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-0.1278, 51.5074]
      },
      "properties": {
        "aqi": 65,
        "category": "Moderate",
        "pm25": 22.5,
        "pm10": 35.2,
        "station": "Central Station"
      }
    }
  ]
}
```

### Run Simulation
```
POST /simulate
```
Simulates the impact of vehicle reduction on traffic and air quality.

**Request Body:**
```json
{
  "vehicle_reduction": 30
}
```

**Response:**
```json
{
  "before": { /* GeoJSON data */ },
  "after": { /* GeoJSON data */ },
  "metrics": {
    "before": {
      "avg_speed": 25.0,
      "congestion_index": 0.65,
      "co2_reduction": 0.0,
      "aqi_improvement": 0.0
    },
    "after": {
      "avg_speed": 31.0,
      "congestion_index": 0.46,
      "co2_reduction": 10.56,
      "aqi_improvement": 4.65
    }
  }
}
```

## 🎨 Features

### Interactive Map
- Real-time visualization of traffic flow and air quality
- Toggle between different data layers
- Click on AQI sensors for detailed information
- Color-coded traffic congestion levels

### Scenario Simulation
- Adjust vehicle reduction percentage (0-100%)
- Run AI-powered simulations
- View before/after comparisons
- Real-time metrics dashboard

### Metrics Dashboard
- Average traffic speed
- Congestion index
- CO₂ emission reduction
- Air quality improvement

## 🔧 Development

### Backend Development

The backend follows a modular architecture:

- **Routers**: Handle HTTP requests and responses
- **Services**: Contain business logic
- **Models**: Define data structures with Pydantic
- **ML**: Placeholder for machine learning models
- **Utils**: Shared utilities like caching

### Frontend Development

The frontend is built with React and TypeScript:

- **Components**: Reusable UI components
- **Services**: API integration layer
- **Types**: TypeScript type definitions
- **Hooks**: Custom React hooks (can be added)

### Adding New Features

1. **Backend**: Add new routers in `backend/routers/`
2. **Frontend**: Add new components in `frontend/src/components/`
3. **Data Models**: Update `backend/models/schemas.py`
4. **API Integration**: Update `frontend/src/services/api.ts`

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
npm run test
```

### Linting
```bash
# Frontend
cd frontend
npm run lint

# Backend
cd backend
flake8 .
```

## 🚀 Deployment

### Production Build

**Frontend:**
```bash
cd frontend
npm run build
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Production
```bash
docker-compose up -d
```

## 🌟 Future Enhancements

### Machine Learning
- Train LSTM models on historical traffic data
- Implement Graph Neural Networks for road networks
- Real-time prediction with streaming data

### Data Integration
- Connect to real city traffic APIs
- Integrate weather data
- Connect to government AQI sensors

### Features
- User authentication and saved scenarios
- Historical data analysis
- Multi-city support
- Export reports and visualizations
- 3D building visualization

### Infrastructure
- PostgreSQL/PostGIS for spatial data
- Redis for caching
- Kubernetes deployment
- CI/CD pipeline

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MapLibre GL JS](https://maplibre.org/)
- [TailwindCSS](https://tailwindcss.com/)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👥 Team

Built for hackathons and sustainable city development.

---

**Happy Hacking!** 🚀🌍
