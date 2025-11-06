# Satellite Tracking Backend

A FastAPI application with real-time satellite position tracking using Two-Line Element (TLE) orbital data and the SGP4 propagator from the Skyfield library.

## Overview

This backend extends basic satellite CRUD operations with:
- **TLE Storage**: Store Two-Line Element orbital data for each satellite
- **Position Calculation**: Real-time position calculation using SGP4 propagator
- **Celestrak Integration**: Fetch current TLE data from Celestrak's public API
- **RESTful API**: Standard HTTP endpoints for satellite management and tracking

## Architecture

```
┌────────────────────┐
│  Frontend Client   │
└────────┬───────────┘
         │ HTTP/JSON
         ▼
┌────────────────────┐      ┌─────────────┐
│  FastAPI Backend   │─────▶│  SQLite DB  │
│                    │      └─────────────┘
│  - CRUD Operations │
│  - TLE Management  │
│  - SGP4 Propagator │      ┌─────────────┐
│  - Skyfield Lib    │─────▶│  Celestrak  │
└────────────────────┘      │  (TLE API)  │
                            └─────────────┘
```

## What is TLE (Two-Line Element)?

TLE is a standardized format for distributing satellite orbital elements:

```
ISS (ZARYA)
1 25544U 98067A   24310.51118287  .00013207  00000+0  23527-3 0  9992
2 25544  51.6406 308.8287 0005935 102.5703  63.9156 15.50327891478902
```

- **Line 0**: Satellite name
- **Line 1**: Epoch, drag, ephemeris type (69 characters)
- **Line 2**: Orbital elements (inclination, RAAN, eccentricity, etc.) (69 characters)

The **SGP4 (Simplified General Perturbations)** propagator uses TLE data to calculate satellite positions at any given time.

## Setup

### Option 1: Using Conda (Recommended)

```bash
conda env create -f environment.yml
conda activate satellite-tracking
```

### Option 2: Using pip

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

```bash
fastapi dev main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## Database Schema

```sql
CREATE TABLE Satellites (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    NORAD_ID INTEGER UNIQUE NOT NULL,
    TLE_Line1 TEXT NOT NULL,
    TLE_Line2 TEXT NOT NULL,
    TLE_Updated TEXT NOT NULL
);
```

## API Endpoints

### Satellite Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/satellites/` | Create a new satellite with TLE data |
| GET | `/satellites/` | Get all satellites |
| GET | `/satellites/{id}` | Get a specific satellite |
| PUT | `/satellites/{id}/tle` | Update TLE data for a satellite |
| DELETE | `/satellites/{id}` | Delete a satellite |

### Position Tracking

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/satellites/{id}/position` | Get current position of a satellite |
| GET | `/satellites/positions` | Get current positions of all satellites |

### Utilities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/satellites/fetch-tle/{norad_id}` | Fetch TLE from Celestrak by NORAD ID |

## Example Usage

### 1. Create a Satellite

```bash
curl -X POST "http://localhost:8000/satellites/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ISS (ZARYA)",
    "norad_id": 25544,
    "tle_line1": "1 25544U 98067A   24310.51118287  .00013207  00000+0  23527-3 0  9992",
    "tle_line2": "2 25544  51.6406 308.8287 0005935 102.5703  63.9156 15.50327891478902"
  }'
```

### 2. Get Current Position

```bash
curl "http://localhost:8000/satellites/1/position"
```

**Response:**
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

### 3. Get All Positions

```bash
curl "http://localhost:8000/satellites/positions"
```

### 4. Fetch TLE from Celestrak

```bash
curl "http://localhost:8000/satellites/fetch-tle/25544"
```

## Seeding the Database

Use the provided script to seed the database with sample satellites:

```bash
python seed_database.py
```

This adds 5 sample satellites:
1. ISS (ZARYA) - International Space Station
2. HUBBLE SPACE TELESCOPE
3. STARLINK-1007
4. NOAA 18 - Weather satellite
5. GPS BIIA-21 - Navigation satellite

## Technologies

- **FastAPI**: Modern async web framework
- **aiosqlite**: Async SQLite driver
- **Skyfield**: Astronomical calculations library
- **SGP4**: Satellite propagation algorithm
- **Pydantic**: Data validation
- **Requests**: HTTP client for Celestrak integration

## How Position Calculation Works

1. **Fetch TLE data** from database (or Celestrak)
2. **Create satellite object** using Skyfield's `EarthSatellite`
3. **Propagate** to current time using SGP4 algorithm
4. **Calculate subpoint** (point on Earth directly below satellite)
5. **Return** latitude, longitude, and altitude

```python
from skyfield.api import EarthSatellite, load, wgs84

ts = load.timescale()
satellite = EarthSatellite(tle_line1, tle_line2, name, ts)

t = ts.now()
geocentric = satellite.at(t)
subpoint = wgs84.subpoint(geocentric)

latitude = subpoint.latitude.degrees
longitude = subpoint.longitude.degrees
altitude = subpoint.elevation.km
```

## TLE Data Sources

### Celestrak (Free, No Account)
- **URL**: https://celestrak.org/
- **API**: https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE
- **Usage**: Integrated in this backend

### Space-Track (Free Account Required)
- **URL**: https://www.space-track.org/
- **Features**: More comprehensive database, historical TLE data
- **Usage**: Requires authentication (not implemented in this example)

## Common NORAD IDs

| Satellite | NORAD ID |
|-----------|----------|
| ISS | 25544 |
| Hubble Space Telescope | 20580 |
| Tiangong Space Station | 48274 |
| NOAA 18 | 28654 |
| GPS BIIA-21 | 24876 |
| Starlink satellites | 44713+ |

## Pedagogical Notes

This example demonstrates:

1. **External API Integration**: Fetching data from Celestrak
2. **Scientific Computing**: Using astronomical libraries (Skyfield)
3. **Data Validation**: TLE format validation (exactly 69 characters per line)
4. **Real-time Calculations**: Position updates based on current time
5. **Unique Constraints**: NORAD ID uniqueness in database
6. **RESTful Design**: Separate endpoints for management vs. calculations

## Troubleshooting

### TLE Not Found Error
- Verify NORAD ID is correct
- Check Celestrak is accessible: https://celestrak.org/
- Some satellites may not be in Celestrak's database

### Position Calculation Errors
- Ensure TLE data is valid (exactly 69 characters per line)
- TLE data becomes outdated over time (update via `/satellites/{id}/tle`)
- Check that Skyfield data files are downloaded (happens automatically on first run)

### Database Errors
- Delete `satellites.db` to reset the database
- Check file permissions for write access

## Dependencies

- **fastapi**: Web framework
- **aiosqlite**: Async SQLite driver
- **uvicorn**: ASGI server
- **pydantic**: Data validation
- **skyfield**: Astronomical calculations
- **requests**: HTTP client

See `requirements.txt` for specific versions.

## Further Enhancements

Potential extensions for advanced students:

1. **Orbital Paths**: Calculate and display satellite ground tracks
2. **Pass Predictions**: Calculate when satellites are visible from specific locations
3. **TLE Auto-Update**: Background task to refresh TLE data periodically
4. **Multiple Time Points**: Historical and future position predictions
5. **Collision Detection**: Calculate close approaches between satellites
6. **Coverage Analysis**: Calculate ground station visibility windows

## References

- [Celestrak TLE Documentation](https://celestrak.org/NORAD/documentation/)
- [Skyfield Documentation](https://rhodesmill.org/skyfield/)
- [SGP4 Theory](https://en.wikipedia.org/wiki/Simplified_perturbations_models)
- [TLE Format Specification](https://celestrak.org/columns/v04n03/)
