# UrbanPulse Quick Start Guide

Get UrbanPulse running in 5 minutes!

## 🚀 Fastest Way: Docker

```bash
# Start everything with one command
docker-compose up --build

# Access the app
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

That's it! The app is now running.

## 🛠️ Development Mode (Without Docker)

### Terminal 1: Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at: http://localhost:8000

### Terminal 2: Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

## 🎮 Using the App

1. **View Data Layers**
   - Click "Traffic Flow" to see traffic congestion
   - Click "Air Quality" to see AQI sensors
   - Click on AQI markers for detailed info

2. **Run Simulations**
   - Adjust the "Vehicle Reduction" slider (0-100%)
   - Click "Run Simulation"
   - View metrics showing improvements

3. **Understand the Colors**

   **Traffic:**
   - Green = Low congestion
   - Yellow = Moderate congestion
   - Red = High congestion

   **Air Quality:**
   - Green = Good (0-50)
   - Yellow = Moderate (51-100)
   - Orange = Unhealthy (101-150)

## 📡 Test the API

```bash
# Check status
curl http://localhost:8000/status

# Get traffic data
curl http://localhost:8000/data/traffic

# Get AQI data
curl http://localhost:8000/data/aqi

# Run simulation
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{"vehicle_reduction": 30}'
```

## 🔧 Troubleshooting

**Port already in use?**
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Find process using port 3000
lsof -ti:3000 | xargs kill -9
```

**Module not found errors?**
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && rm -rf node_modules && npm install
```

**Docker issues?**
```bash
# Clean up and rebuild
docker-compose down -v
docker-compose up --build
```

## 📚 Next Steps

- Read the full [README.md](README.md)
- Explore the API docs at http://localhost:8000/docs
- Customize the mock data in `backend/data/`
- Add your own ML models in `backend/ml/`

Happy hacking! 🎉
