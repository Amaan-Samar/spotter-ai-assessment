Here's a comprehensive README file for your project:

---

# Spotter AI - FMCSA HOS Trip Planner

## 📋 Overview

Spotter AI is a **Full Stack Trip Planning Application** for commercial truck drivers that helps plan routes compliant with FMCSA Hours of Service (HOS) regulations. The app calculates trip duration, fuel stops, daily driving limits, and generates ELD (Electronic Logging Device) log sheets based on the **70-hour/8-day rule** for property-carrying drivers.

This project was built as a technical assessment for a Full Stack Developer position.

---

## 🎯 Features

### ✅ Implemented Features

| Feature | Description |
|---------|-------------|
| **Trip Planning** | Users can enter trip details (current, pickup, dropoff locations, cycle used) |
| **Route Visualization** | Interactive map showing route, pickup/dropoff markers, and fuel stops |
| **HOS Compliance Engine** | Automatically calculates driving limits based on FMCSA 70hr/8day rule |
| **ELD Log Generation** | Generates daily log sheets with 24-hour grids showing duty status |
| **Cycle Tracking** | Tracks driver's 70-hour rolling cycle with visual progress bar |
| **Trip Summary** | Shows total miles, driving hours, on-duty hours, and trip duration |
| **Fuel Stop Calculation** | Automatically adds fuel stops every 1,000 miles |
| **Database Storage** | Saves all trips to SQLite database for future reference |
| **Responsive Design** | macOS-inspired UI with glassmorphic design |

### 🚧 Limitations / Not Implemented

| Limitation | Explanation |
|------------|-------------|
| **Real Routing API** | Currently uses mock distance data; integrates with OSRM/Nominatim planned |
| **Real-time GPS Tracking** | Not required by assessment; focuses on trip planning |
| **User Authentication** | No login system; single user demo |
| **Mobile App** | Web-only application |
| **Offline Support** | Requires internet connection for maps |
| **Multi-carrier Support** | Single carrier implementation |
| **PDF Export** | ELD logs displayed on screen only |
| **Email Reports** | No report distribution feature |

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 5.1.6 | Web framework |
| Django REST Framework | 3.17.1 | API development |
| SQLite | 3.x | Database (development) |
| Gunicorn | 23.0.0 | Production WSGI server |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.x | UI framework |
| Vite | 5.x | Build tool |
| Tailwind CSS | 3.x | Styling |
| Leaflet | 1.9.x | Interactive maps |
| React Leaflet | 4.x | React map integration |
| Axios | 1.x | HTTP client |

---

## 📁 Project Structure

```
spotter-ai-assessment/
├── backend/
│   ├── backend/
│   │   ├── settings.py      # Django configuration
│   │   ├── urls.py          # Main URL routes
│   │   └── wsgi.py
│   ├── api/
│   │   ├── models.py        # Database models (Trip, TripDay)
│   │   ├── views.py         # API endpoints (plan-trip, list-trips)
│   │   ├── urls.py          # API routes
│   │   ├── serializers.py   # DRF serializers
│   │   └── services/
│   │       ├── routing.py   # OSRM/Nominatim integration
│   │       └── hos_engine.py # HOS calculation engine
│   ├── manage.py
│   ├── requirements.txt
│   └── venv/                 # Virtual environment
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── TripForm.jsx      # Input form
    │   │   ├── MapView.jsx       # Leaflet map component
    │   │   ├── ELDLog.jsx        # Canvas-based ELD grid
    │   │   ├── TripSummary.jsx   # Trip statistics
    │   │   └── CycleTracker.jsx  # 70-hour progress bar
    │   ├── services/
    │   │   └── api.js            # Axios API client
    │   ├── App.jsx               # Main application
    │   └── index.css             # Tailwind + custom styles
    ├── package.json
    └── vite.config.js
```

---

## 🚀 Installation & Setup

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.12+ |
| Node.js | 18+ |
| npm | 9+ |
| Git | (optional) |

### Step 1: Clone the Repository

```bash
git clone https://github.com/Amaan-Samar/spotter-ai-assessment.git
cd spotter-ai-assessment
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start backend server
python manage.py runserver
```

Backend runs at: `http://localhost:8000`

### Step 3: Frontend Setup

```bash
# Open a new terminal window
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:5173`

### Step 4: Test the Application

1. Open `http://localhost:5173` in your browser
2. You should see the macOS-style interface
3. Look for "✓ Backend Connected" badge in top bar

---

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/test/` | Health check |
| POST | `/api/plan-trip/` | Calculate trip and generate logs |
| GET | `/api/trips/` | List all saved trips |
| GET | `/api/trips/{id}/` | Get specific trip details |

### Request Example: `POST /api/plan-trip/`

```json
{
  "current_location": "Chicago, IL",
  "pickup_location": "Indianapolis, IN",
  "dropoff_location": "Atlanta, GA",
  "cycle_used": 35
}
```

### Response Example

```json
{
  "trip_id": 1,
  "total_miles": 720.0,
  "total_driving_hours": 13.1,
  "total_days": 2,
  "fuel_stops": [],
  "days": [...],
  "cycle_tracking": {
    "started_with": 35,
    "trip_added": 15.1,
    "remaining": 19.9
  },
  "route_geometry": [[41.8781, -87.6298], ...]
}
```

---

## 🧪 Testing Different Scenarios

| Test Case | Input | Expected Output |
|-----------|-------|-----------------|
| Short Trip | Chicago → Indianapolis (35 cycle) | ~180 miles, 1 day, 0 fuel stops |
| Medium Trip | Chicago → Atlanta (35 cycle) | ~720 miles, 2 days, 0 fuel stops |
| Long Trip | NY → Los Angeles (20 cycle) | ~2800 miles, 5 days, 2 fuel stops |
| Cycle Violation | Chicago → LA (60 cycle) | Warning message about exceeding limit |

---

## 📊 HOS Rules Implemented

| Rule | Value | Implementation |
|------|-------|----------------|
| Daily Driving Limit | 11 hours max | Trip split into 11-hour segments |
| Daily Duty Window | 14 hours | Log entries respect 14-hour window |
| 30-min Break | After 8 hours driving | Added to log automatically |
| Weekly Cycle | 70 hours / 8 days | Tracked with progress bar |
| Off-duty Requirement | 10 consecutive hours | Midnight to 6am in logs |
| Fuel Stops | Every 1,000 miles | Auto-calculated and mapped |

---

## 🐛 Known Issues & Workarounds

| Issue | Workaround |
|-------|------------|
| **CORS errors** | Ensure `CORS_ALLOW_ALL_ORIGINS = True` in settings.py |
| **Map not loading** | Check internet connection for Leaflet CDN |
| **Routing API fails** | Mock distance data used as fallback |
| **Canvas not drawing** | Verify logEntries data structure in console |

---

## 🔧 Environment Variables

Create `backend/.env` file:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 🚢 Deployment

### Deploy Backend (Render)

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn backend.wsgi:application`

### Deploy Frontend (Vercel)

1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel --prod` in frontend directory
3. Follow prompts

---

## 📝 Assessment Requirements Met

| Requirement | Status |
|-------------|--------|
| Django + React Full-stack app | ✅ Complete |
| Trip details as inputs | ✅ Complete |
| Map showing route | ✅ Complete |
| ELD logs filled out | ✅ Complete |
| 70hr/8day cycle rule | ✅ Complete |
| Fuel stops every 1000 miles | ✅ Complete |
| 1 hour for pickup/dropoff | ✅ Complete |
| Multiple logs for longer trips | ✅ Complete |
| Hosted version | 🚧 Pending |
| Loom video | 🚧 Pending |
| GitHub code | ✅ Complete |

---

## 📄 License

This project was created for a technical assessment. All rights reserved.

---

## 👨‍💻 Author

Spotter AI Assessment Submission

---

## 🙏 Acknowledgments

- FMCSA for HOS regulations documentation
- Leaflet for open-source mapping
- OpenStreetMap for tile data
- Tailwind CSS for styling framework

---

## 📞 Support

For issues or questions regarding this assessment:
- Backend logs: Check terminal output
- Frontend errors: Open browser console (F12)
- API testing: Use curl or Postman

---

**Last Updated:** April 2026

---

Would you like me to also provide:
1. **Loom video script** - What to say in your 3-5 minute demo?
2. **Deployment instructions** - Step-by-step for Vercel + Render?
3. **API documentation** - More detailed for Postman testing?