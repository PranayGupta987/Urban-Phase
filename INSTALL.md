# UrbanPulse Installation & Run Instructions

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Required packages:
- fastapi==0.109.0
- uvicorn[standard]==0.27.0
- pydantic==2.5.3
- python-dotenv==1.0.0
- requests==2.31.0
- pandas==2.1.4
- numpy==1.26.2
- scikit-learn==1.3.2
- scipy==1.11.4
- lightgbm==4.1.0
- joblib==1.3.2

### 2. Set Environment Variables

Create `backend/.env` file:

```
LTA_API_KEY=your_lta_key_here
WAQI_TOKEN=c5c8204b44d6579b0def08c45059faca2430308f
DATA_GOV_SG_ENDPOINT=https://api.data.gov.sg/v1
```

### 3. Run Backend

```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: http://127.0.0.1:8000

## Frontend Setup

### 1. Install Node Dependencies

```bash
cd frontend
npm install
```

Required packages:
- maplibre-gl
- axios
- react-toastify
- zustand
- lucide-react
- react
- react-dom

### 2. Run Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

## API Endpoints

### Backend Routes

- GET `/status` - API status
- GET `/data/traffic` - Traffic GeoJSON
- GET `/data/aqi` - AQI GeoJSON
- GET `/data/weather` - Weather JSON
- POST `/simulate` - Run simulation
  - Body: `{ "vehicle_reduction": 30 }` (0-100)

### Frontend API Service

- `api.getTrafficData()` - GET /data/traffic
- `api.getAQIData()` - GET /data/aqi
- `api.getWeatherData()` - GET /data/weather
- `api.runSimulation({ vehicle_reduction: number })` - POST /simulate

## Verification

1. Backend starts without errors
2. Frontend loads map with Singapore center
3. Traffic lines appear on map
4. AQI circles appear on map
5. Simulation button updates map
6. No console errors
7. No white screen

