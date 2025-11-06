# Streamlit Frontend with Live Satellite Tracking

A Python-based web interface for tracking satellites in real-time on 2D maps and 3D globes. This application demonstrates client-server architecture with REST API consumption and interactive data visualization.

## Features

- **🗺️ 2D Map**: Live satellite positions on an interactive map using PyDeck
- **🌍 3D Globe**: Orbital visualization on a rotating Earth using Plotly
- **📋 Satellite Management**: View, add, and delete satellites with TLE data
- **📍 Real-Time Tracking**: SGP4 propagation for accurate position calculations
- **🔄 Auto-Refresh**: Automatic position updates
- **🛰️ Celestrak Integration**: Fetch current TLE data by NORAD ID

## Prerequisites

**Start the tracking backend first!**

```bash
cd ../backend_tracking
fastapi dev main.py
```

Backend should be running at http://localhost:8000

## Setup

### Option 1: Using Conda (Recommended)

```bash
conda env create -f environment.yml
conda activate satellite-tracking-frontend
```

### Option 2: Using pip

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run main.py
```

Opens at http://localhost:8501

## Usage Guide

### 1. 2D Map View

The 2D map tab displays real-time satellite positions:

- **Red dots** represent satellites
- **Hover** over a satellite to see details
- Click **🔄 Refresh Positions** to update
- Position updates show latitude, longitude, and altitude

**Technology**: PyDeck (Uber's geospatial visualization framework)

### 2. 3D Globe View

The 3D globe shows satellites on an interactive rotating Earth:

- **Red markers** show satellite positions
- **Rotate** by dragging
- **Zoom** with scroll wheel
- **Hover** for satellite details

**Technology**: Plotly (interactive graphing library)

### 3. Satellites Tab

View all satellites in the database:

- Expandable cards for each satellite
- TLE data display
- **Get Current Position** button for individual satellites
- Last TLE update timestamp

### 4. Add Satellite

Two methods for adding satellites:

#### Method 1: Fetch from Celestrak (Recommended)

1. Enter a NORAD Catalog ID
2. Click **Fetch TLE Data**
3. Enter a name for the satellite
4. Click **Create Satellite**

**Popular NORAD IDs:**
- ISS: 25544
- Hubble: 20580
- Starlink-1007: 44713
- NOAA 18: 28654

#### Method 2: Manual TLE Entry

1. Switch to "Manual TLE Entry"
2. Enter satellite name and NORAD ID
3. Paste TLE Line 1 (69 characters)
4. Paste TLE Line 2 (69 characters)
5. Click **Create Satellite**

### 5. Delete Satellite

1. Select a satellite from the dropdown
2. Click **🗑️ Delete Satellite**

## Architecture

```
┌──────────────────────┐
│  Streamlit Frontend  │
│  (localhost:8501)    │
└──────────┬───────────┘
           │ HTTP/JSON
           ▼
┌──────────────────────┐      ┌─────────────┐
│   FastAPI Backend    │─────▶│  SQLite DB  │
│   (localhost:8000)   │      │  (TLE Data) │
└──────────┬───────────┘      └─────────────┘
           │
           ▼
┌──────────────────────┐
│  Skyfield Library    │
│  (SGP4 Propagator)   │
└──────────────────────┘
```

## Technology Stack

### Core Framework
- **Streamlit**: Python web framework for data applications
- **requests**: HTTP library for API communication

### Visualization
- **PyDeck**: WebGL-powered geospatial visualizations
- **Plotly**: Interactive 3D graphics
- **Pandas**: Data manipulation for map layers

### Data Processing
- **Pydantic** (via backend): Data validation
- **Skyfield** (via backend): Satellite position calculations

## API Integration

The frontend communicates with the backend via these endpoints:

| API Call | Purpose |
|----------|---------|
| `GET /satellites/` | Load all satellites |
| `GET /satellites/{id}/position` | Get single satellite position |
| `GET /satellites/positions` | Get all current positions |
| `POST /satellites/` | Create new satellite |
| `DELETE /satellites/{id}` | Delete satellite |
| `GET /satellites/fetch-tle/{norad_id}` | Fetch TLE from Celestrak |

## Code Structure

```python
# API Helper Functions
get_all_satellites()      # Fetch satellite list
get_satellite_position()  # Get single position
get_all_positions()       # Get all positions
create_satellite()        # Add new satellite
delete_satellite()        # Remove satellite
fetch_tle_from_api()      # Fetch from Celestrak

# Visualization Functions
create_2d_map()          # PyDeck 2D map
create_3d_globe()        # Plotly 3D globe

# Streamlit UI
st.tabs()                # Tab navigation
st.form()                # Form handling
st.rerun()               # Force refresh
```

## Pedagogical Notes

This example demonstrates:

1. **REST API Consumption**: Making HTTP requests to backend
2. **Data Visualization**: Multiple visualization libraries (PyDeck, Plotly)
3. **Real-Time Updates**: Handling time-dependent data
4. **External API Integration**: Fetching TLE from Celestrak via backend
5. **State Management**: Using Streamlit session state
6. **Error Handling**: Try/except with user-friendly messages
7. **Form Validation**: Input validation before API calls

## Comparison: 2D Map vs 3D Globe

| Feature | 2D Map (PyDeck) | 3D Globe (Plotly) |
|---------|-----------------|-------------------|
| View | Flat map projection | Spherical Earth |
| Interaction | Pan & zoom | Rotate & zoom |
| Performance | Very fast | Good |
| Best For | Tracking many satellites | Understanding orbital geometry |
| Customization | Advanced (layers) | Moderate |

## Troubleshooting

### "Cannot connect to API" Error

1. Check backend is running at http://localhost:8000
2. Visit http://localhost:8000/docs to verify
3. Check firewall settings for port 8000

### Map Not Displaying

- PyDeck requires modern browser (Chrome, Firefox, Edge)
- Check JavaScript is enabled
- Clear browser cache

### Position Data Not Updating

- Click **🔄 Refresh Positions**
- Verify TLE data is valid in backend
- Check satellite is in database

### Celestrak Fetch Fails

- Verify NORAD ID is correct
- Check internet connection
- Celestrak may be temporarily unavailable

### Performance Issues

- Limit to ~20 satellites for smooth map performance
- Use 3D globe for fewer satellites (<10 recommended)
- Close other browser tabs

## Keyboard Shortcuts

Streamlit provides built-in shortcuts:

- **R**: Rerun the app
- **C**: Clear cache
- **?**: Show keyboard shortcuts

## Customization Ideas

For advanced students:

1. **Orbital Paths**: Add satellite ground tracks to the map
2. **Time Travel**: Add time slider to see past/future positions
3. **Pass Predictions**: Calculate when satellites are visible from your location
4. **Filters**: Filter satellites by type (LEO, MEO, GEO)
5. **Heatmaps**: Show satellite density over time
6. **Comparison Mode**: Track specific satellites with detailed info

## Dependencies

```
streamlit>=1.39.0   # Web framework
requests>=2.32.0    # HTTP client
pandas>=2.2.0       # Data manipulation
pydeck>=0.9.0       # 2D maps
plotly>=5.24.0      # 3D globe
```

See `requirements.txt` for exact versions.

## Known Limitations

1. **TLE Accuracy**: TLE data degrades over time (days to weeks)
2. **Refresh Rate**: Manual refresh (auto-refresh could be added)
3. **Historical Data**: No historical position tracking (backend limitation)
4. **Time Zones**: All times in UTC (no local time conversion)

## Further Reading

- [Streamlit Documentation](https://docs.streamlit.io/)
- [PyDeck Documentation](https://deckgl.readthedocs.io/en/latest/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [TLE Format](https://celestrak.org/columns/v04n03/)
- [SGP4 Algorithm](https://en.wikipedia.org/wiki/Simplified_perturbations_models)

## Related Examples

- **Basic Streamlit Frontend**: `../frontend_streamlit/` (simple CRUD without tracking)
- **HTML Frontend**: `../frontend_tracking_html/` (JavaScript-based alternative)
- **Backend**: `../backend_tracking/` (FastAPI with position calculation)
