# Client-Server Architecture Examples

Complete examples demonstrating client-server architecture for IEE 305 (Information Systems Engineering). Includes basic CRUD operations and advanced satellite tracking with real-time position visualization.

## Directory Structure

```
client_server/
├── backend_sql/                    # Basic FastAPI + SQLite
├── backend_orm/                    # FastAPI + SQLModel ORM
├── backend_tracking/               # FastAPI + Satellite Tracking ⭐ ADVANCED
├── frontend_streamlit/             # Basic Streamlit frontend
├── frontend_html/                  # Basic HTML/JS frontend
├── frontend_tracking_streamlit/    # Streamlit + Live Maps ⭐ ADVANCED
├── frontend_tracking_html/         # HTML/JS + Live Maps ⭐ ADVANCED
└── README.md                       # This file
```

## Example Sets

### Basic Examples: Simple Satellite CRUD

**Purpose**: Learn fundamental client-server architecture and REST APIs

**Backend Options:**
- `backend_sql/` - FastAPI with raw SQL (aiosqlite)
- `backend_orm/` - FastAPI with SQLModel ORM

**Frontend Options:**
- `frontend_streamlit/` - Python-based (Streamlit)
- `frontend_html/` - Browser-based (HTML/CSS/JavaScript)

**Data Model**: Simple satellite records (ID, acronym, mass, power)

**Operations**: Create, Read, Update (PUT & PATCH), Delete

**Best For**: Introduction to REST APIs, HTTP methods, CRUD operations

---

### Advanced Examples: Satellite Tracking with Live Positions ⭐

**Purpose**: Real-world application with orbital mechanics and data visualization

**Backend:**
- `backend_tracking/` - FastAPI + TLE data + SGP4 propagator

**Frontend Options:**
- `frontend_tracking_streamlit/` - 2D maps + 3D globe (Python)
- `frontend_tracking_html/` - Live interactive map (HTML/JS)

**Data Model**: Satellites with TLE (Two-Line Element) orbital data

**Operations**:
- Full CRUD operations
- Real-time position calculation
- TLE fetching from Celestrak
- Map visualization

**Best For**: Term projects, advanced coursework, external API integration

---

## Quick Start Guide

### Option 1: Basic Examples

**Step 1: Start a backend**

```bash
# SQL Backend
cd backend_sql
conda env create -f environment.yml
conda activate sqlite-backend
fastapi dev main.py

# ORM Backend
cd backend_orm
conda env create -f environment.yml
conda activate orm-backend
fastapi dev main.py
```

**Step 2: Start a frontend**

```bash
# Streamlit (Python)
cd ../frontend_streamlit
conda env create -f environment.yml
conda activate streamlit-frontend
streamlit run main.py --server.headless true

# OR HTML (Browser)
cd ../frontend_html
python3 -m http.server 8080
# Open http://localhost:8080
```

---

### Option 2: Satellite Tracking Examples ⭐

**Step 1: Start tracking backend**

```bash
cd backend_tracking
conda env create -f environment.yml
conda activate satellite-tracking
fastapi dev main.py
```

**Step 2: Seed database with sample satellites**

```bash
python3 seed_database.py
```

**Step 3: Start a frontend**

```bash
# Streamlit (Python)
cd ../frontend_tracking_streamlit
conda env create -f environment.yml
conda activate satellite-tracking-frontend
streamlit run main.py --server.headless true

# OR HTML (Browser)
cd ../frontend_tracking_html
python3 -m http.server 8080
# Open http://localhost:8080
```

---

## Comparison Matrix

### Backend Comparison

| Feature | backend_sql | backend_orm | backend_tracking |
|---------|-------------|-------------|------------------|
| **Framework** | FastAPI | FastAPI | FastAPI |
| **Database** | SQLite | SQLite | SQLite |
| **Data Layer** | Raw SQL | SQLModel ORM | Raw SQL + Skyfield |
| **Complexity** | Low | Medium | High |
| **Data Model** | Simple (4 fields) | Simple (4 fields) | Complex (TLE data) |
| **Position Calc** | ❌ | ❌ | ✅ SGP4 |
| **External API** | ❌ | ❌ | ✅ Celestrak |
| **Best For** | SQL learning | ORM introduction | Real applications |

### Frontend Comparison

| Feature | Streamlit (Basic) | HTML (Basic) | Streamlit (Tracking) | HTML (Tracking) |
|---------|-------------------|--------------|----------------------|-----------------|
| **Language** | Python | HTML/CSS/JS | Python | HTML/CSS/JS |
| **Setup** | pip/conda | None | pip/conda | None |
| **Dependencies** | streamlit, requests | None (CDN) | +pandas, pydeck, plotly | +Leaflet.js (CDN) |
| **CRUD Ops** | ✅ | ✅ | ✅ | ✅ |
| **Visualization** | Tables | Tables | 2D map + 3D globe | 2D map |
| **Auto-Refresh** | Manual | Manual | Manual | Auto (5s) |
| **Learning Curve** | Low | Medium | Medium | Medium |
| **Best For** | Python students | Web dev intro | Data viz | Real-time apps |

---

## Technology Stack

### Backend Technologies
- **FastAPI**: Modern async web framework
- **SQLite**: Lightweight database
- **aiosqlite**: Async SQLite driver
- **Pydantic**: Data validation
- **SQLModel** (ORM example): ORM combining SQLAlchemy + Pydantic
- **Skyfield** (tracking): Astronomical calculations
- **Requests** (tracking): HTTP client for Celestrak

### Frontend Technologies

**Streamlit:**
- **streamlit**: Python web framework
- **requests**: HTTP client
- **pandas**: Data manipulation
- **pydeck**: 2D maps (WebGL)
- **plotly**: 3D visualizations

**HTML/JavaScript:**
- **Vanilla JS**: No frameworks
- **Fetch API**: HTTP requests
- **Leaflet.js**: Interactive maps
- **OpenStreetMap**: Map tiles

---

## API Endpoints Reference

### Basic CRUD Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/satellites/` | List all satellites |
| GET | `/satellites/{id}` | Get one satellite |
| POST | `/satellites/` | Create satellite |
| PUT | `/satellites/{id}` | Update all fields |
| PATCH | `/satellites/{id}` | Update some fields |
| DELETE | `/satellites/{id}` | Delete satellite |

### Tracking-Specific Endpoints ⭐

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/satellites/{id}/position` | Current position of one satellite |
| GET | `/satellites/positions` | Current positions of all satellites |
| GET | `/satellites/fetch-tle/{norad_id}` | Fetch TLE from Celestrak |
| PUT | `/satellites/{id}/tle` | Update TLE data |

---

## Sample Data

### Basic Examples

```json
{
  "acronym": "ISS",
  "mass": 419700.0,
  "power": 120000.0
}
```

### Tracking Examples (TLE Format)

```json
{
  "name": "ISS (ZARYA)",
  "norad_id": 25544,
  "tle_line1": "1 25544U 98067A   24310.51118287  .00013207  00000+0  23527-3 0  9992",
  "tle_line2": "2 25544  51.6406 308.8287 0005935 102.5703  63.9156 15.50327891478902"
}
```

**Position Response:**
```json
{
  "satellite_id": 1,
  "name": "ISS (ZARYA)",
  "norad_id": 25544,
  "latitude": 23.4567,
  "longitude": -45.1234,
  "altitude_km": 418.23,
  "timestamp": "2024-11-05T12:34:56.789Z"
}
```

---

## Common NORAD IDs for Testing

| Satellite | NORAD ID | Type |
|-----------|----------|------|
| ISS (ZARYA) | 25544 | Space Station |
| Hubble Space Telescope | 20580 | Observatory |
| Tiangong Space Station | 48274 | Space Station |
| NOAA 18 | 28654 | Weather |
| GPS BIIA-21 (PRN 09) | 24876 | Navigation |
| Starlink-1007 | 44713 | Communications |

---

## Architecture Diagrams

### Basic Architecture

```
┌─────────────┐         HTTP/JSON          ┌─────────────┐
│   Frontend  │ ─────────────────────────> │   Backend   │
│  (Streamlit │ <───────────────────────── │  (FastAPI)  │
│   or HTML)  │                            └──────┬──────┘
└─────────────┘                                   │
                                                  ▼
                                            ┌─────────────┐
                                            │  SQLite DB  │
                                            └─────────────┘
```

### Tracking Architecture

```
┌─────────────┐         HTTP/JSON          ┌─────────────┐
│   Frontend  │ ─────────────────────────> │   Backend   │
│  (Maps +    │ <───────────────────────── │  (FastAPI)  │
│   Forms)    │                            └──────┬──────┘
└─────────────┘                                   │
                                          ┌───────┼───────┐
                                          ▼       ▼       ▼
                                    ┌──────┐ ┌────────┐ ┌──────────┐
                                    │SQLite│ │Skyfield│ │Celestrak │
                                    │  DB  │ │ (SGP4) │ │ (TLE API)│
                                    └──────┘ └────────┘ └──────────┘
```

---

## Learning Objectives

### Basic Examples (Lectures 18-20)

Students will be able to:
1. ✅ Design RESTful API endpoints
2. ✅ Implement CRUD operations with FastAPI
3. ✅ Consume REST APIs from frontend
4. ✅ Handle HTTP requests/responses
5. ✅ Validate data with Pydantic
6. ✅ Understand PUT vs PATCH

### Advanced Examples (Term Project)

Students will be able to:
1. ✅ Integrate external APIs (Celestrak)
2. ✅ Work with domain-specific data formats (TLE)
3. ✅ Implement real-time calculations (SGP4)
4. ✅ Visualize geographic data on maps
5. ✅ Design auto-refresh patterns
6. ✅ Handle time-dependent data

---

## Troubleshooting

### Backend Won't Start

```bash
# Check port 8000 is available
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Can't Connect

1. **Verify backend running**: Visit http://localhost:8000/docs
2. **Check CORS**: Already configured in backends
3. **Check firewall**: Allow ports 8000, 8501, 8080

### Position Calculation Errors (Tracking)

1. **TLE format**: Must be exactly 69 characters per line
2. **TLE age**: Update old TLE data (degrades over weeks)
3. **Skyfield data**: First run downloads ephemeris files (~10MB)

---

## References

### Course Materials
- IEE 305 Syllabus
- Lecture 18: Client-Server APIs
- Lecture 19: Backend Implementation
- Lecture 20: Frontend Development

### External Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Skyfield Documentation](https://rhodesmill.org/skyfield/)
- [Celestrak](https://celestrak.org/)
- [TLE Format Specification](https://celestrak.org/columns/v04n03/)

---

## Credits

**Course**: IEE 305 - Information Systems Engineering
**Institution**: Arizona State University
**Semester**: Fall 2025

**Technologies**: FastAPI, Streamlit, SQLite, SQLModel, Skyfield, Leaflet.js

**Data Sources**: Celestrak (TLE data), OpenStreetMap (map tiles)
