# HTML/JavaScript Frontend with Live Satellite Tracking

A single-page web application for tracking satellites in real-time using vanilla HTML, CSS, JavaScript, and the Leaflet.js mapping library. Demonstrates client-server architecture with REST API consumption and interactive visualization.

## Features

- **🗺️ Live Interactive Map**: Real-time satellite positions on OpenStreetMap
- **🔄 Auto-Refresh**: Positions update every 5 seconds
- **📋 Position Table**: Tabular view of all satellite coordinates
- **🛰️ Satellite Database**: Browse all satellites with TLE data
- **➕ Add Satellites**: Fetch TLE from Celestrak or enter manually
- **📍 Markers with Popups**: Click satellites for detailed information
- **Zero Dependencies**: No npm, no build step, runs directly in browser

## Prerequisites

**Start the tracking backend first!**

```bash
cd ../backend_tracking
fastapi dev main.py
```

Backend should be running at http://localhost:8000

## Setup

**No installation required!** This is a static HTML application.

## Running the Application

### Method 1: Python HTTP Server (Recommended)

```bash
python -m http.server 8080
```

Then open: http://localhost:8080

### Method 2: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

### Method 3: Direct File Access

```bash
# macOS
open index.html

# Linux
xdg-open index.html

# Windows
start index.html
```

**Note**: Using an HTTP server (Method 1 or 2) is recommended to avoid CORS restrictions.

## Usage Guide

### Live Map Tab

**Features:**
- Real-time satellite positions displayed as markers
- Auto-refresh every 5 seconds (with countdown)
- Manual refresh button
- Center map button (fits all satellites in view)
- Statistics: satellite count and last update time

**Interaction:**
- **Pan**: Click and drag the map
- **Zoom**: Mouse wheel or zoom controls
- **Click Marker**: View satellite details (name, NORAD ID, coordinates, altitude)

**Map Provider**: OpenStreetMap (free, no API key required)

### Positions Tab

Displays all satellite positions in a sortable table:

| Name | NORAD ID | Latitude | Longitude | Altitude |
|------|----------|----------|-----------|----------|

Click **🔄 Refresh Positions** to update.

### Satellites Tab

Browse all satellites in the database:

- Each satellite displayed in an expandable card
- Shows database ID, NORAD ID, and TLE update time
- Full TLE data displayed in monospace font
- Easy to copy TLE for verification

### Add Satellite Tab

**Step 1: Fetch TLE from Celestrak**
1. Enter NORAD Catalog ID (e.g., 25544 for ISS)
2. Click **Fetch TLE Data**
3. TLE automatically populated

**Step 2: Create Satellite**
1. Enter satellite name
2. Review fetched TLE data (read-only fields)
3. Click **Create Satellite**

**Popular NORAD IDs:**
- ISS: 25544
- Hubble: 20580
- Starlink-1007: 44713
- NOAA 18: 28654

## Architecture

```
┌──────────────────────┐
│   Browser (HTML/JS)  │
│   (localhost:8080)   │
└──────────┬───────────┘
           │ Fetch API
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

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox, gradients
- **Vanilla JavaScript**: No frameworks, ES6+ features
- **Leaflet.js**: Interactive maps (CDN)
- **Fetch API**: Asynchronous HTTP requests

### Backend (Not included in this directory)
- **FastAPI**: Position calculation
- **Skyfield**: SGP4 propagator
- **SQLite**: TLE data storage

## Code Structure

### HTML Structure
```html
<!-- Header -->
<header>Title, connection status</header>

<!-- Tabs -->
<div class="tabs">Tab buttons</div>

<!-- Tab Contents -->
<div id="map-tab">Live map with Leaflet</div>
<div id="positions-tab">Position table</div>
<div id="satellites-tab">Satellite cards</div>
<div id="add-tab">Create forms</div>
```

### JavaScript Functions

```javascript
// Map Functions
initMap()           // Initialize Leaflet map
updateMap()         // Update satellite markers
centerMap()         // Fit map to satellites

// API Functions
loadPositions()     // GET /satellites/positions
loadSatellites()    // GET /satellites/
fetchTLE()          // GET /satellites/fetch-tle/{norad_id}
createSatellite()   // POST /satellites/

// UI Functions
showTab()           // Tab navigation
showMessage()       // Display notifications
checkConnection()   // Verify backend connection

// Auto-Refresh
startAutoRefresh()  // Start 5-second timer
stopAutoRefresh()   // Stop timer
```

## Auto-Refresh Feature

Positions automatically update every 5 seconds:

- **Checkbox**: Enable/disable auto-refresh
- **Countdown**: Shows seconds until next refresh
- **Manual Override**: Click refresh button anytime

Implementation uses `setInterval()`:

```javascript
autoRefreshInterval = setInterval(() => {
    loadPositions();
}, 5000);
```

## Map Markers

Each satellite is represented by a marker:

```javascript
L.marker([latitude, longitude])
    .addTo(map)
    .bindPopup(`
        <strong>${name}</strong><br>
        NORAD: ${norad_id}<br>
        Lat: ${latitude}°<br>
        Lon: ${longitude}°<br>
        Alt: ${altitude_km} km
    `);
```

## API Integration

The frontend makes these HTTP requests:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Check backend connection |
| GET | `/satellites/positions` | Fetch all current positions |
| GET | `/satellites/` | List all satellites |
| GET | `/satellites/fetch-tle/{norad_id}` | Fetch TLE from Celestrak |
| POST | `/satellites/` | Create new satellite |

## Pedagogical Notes

This example demonstrates:

1. **Separation of Concerns**: Backend calculates positions, frontend displays
2. **Asynchronous JavaScript**: `async/await` with Fetch API
3. **DOM Manipulation**: Dynamically updating HTML
4. **Event Handling**: Click, submit, checkbox events
5. **Third-Party Libraries**: Integrating Leaflet.js via CDN
6. **Real-Time Updates**: Using timers for auto-refresh
7. **Error Handling**: Try/catch with user-friendly messages
8. **REST API Consumption**: Standard HTTP methods

## CSS Styling Highlights

- **Gradient Background**: Linear gradient for modern look
- **Tab Navigation**: Active tab highlighting
- **Responsive Design**: Flexbox layout
- **Card Layout**: Satellite information cards
- **Status Indicators**: Color-coded connection status
- **Loading States**: Placeholders while data loads

## Comparison with Streamlit Frontend

| Feature | HTML/JS Frontend | Streamlit Frontend |
|---------|------------------|-------------------|
| **Language** | HTML/CSS/JavaScript | Python only |
| **Setup** | None (static files) | pip/conda install |
| **Dependencies** | Leaflet.js (CDN) | streamlit, pydeck, plotly |
| **Visualization** | 2D map (Leaflet) | 2D map + 3D globe |
| **Learning Curve** | Higher (3 languages) | Lower (Python) |
| **Customization** | Full control | Limited to widgets |
| **Best For** | Web dev fundamentals | Data science apps |

## Browser Compatibility

Works with all modern browsers:
- Chrome/Edge (Chromium)
- Firefox
- Safari
- Opera

Requires JavaScript enabled.

## Troubleshooting

### CORS Errors

If you see `Cross-Origin Request Blocked`:

1. **Use HTTP server** (Method 1 or 2) instead of `file://`
2. Backend has CORS enabled (already configured)

### Map Not Loading

- Check internet connection (Leaflet tiles from OpenStreetMap)
- Clear browser cache
- Check browser console (F12) for errors

### Auto-Refresh Not Working

- Ensure checkbox is checked
- Check backend is responding (`/satellites/positions`)
- Look for JavaScript errors in console

### Backend Connection Failed

- Verify backend running at http://localhost:8000
- Test: http://localhost:8000/docs
- Check firewall for port 8000

### Markers Not Appearing

- Verify satellites exist in database
- Check positions API returns data
- Look for JavaScript errors in console

## Performance Considerations

- **Lightweight**: No frontend build process
- **CDN**: Leaflet loaded from CDN (cached)
- **Efficient**: Only updates changed markers
- **Scalable**: Handles ~50 satellites smoothly

## Security Notes

For production deployment:

1. **HTTPS**: Use HTTPS for both frontend and backend
2. **CORS**: Restrict CORS to specific origins
3. **Rate Limiting**: Add rate limiting to backend
4. **Input Validation**: Backend validates all inputs (already implemented)

## Customization Ideas

For advanced students:

1. **Satellite Paths**: Draw ground tracks on map
2. **Custom Icons**: Different icons for satellite types
3. **Color Coding**: Color by altitude or orbit type
4. **Search Filter**: Filter satellites by name
5. **Map Styles**: Add dark mode map style
6. **Clustering**: Group nearby satellites
7. **Pass Predictions**: Show when satellites are overhead

## File Structure

```
frontend_tracking_html/
├── index.html          # Complete application
└── README.md          # This file
```

**Single File Design**: All HTML, CSS, and JavaScript in one file for simplicity.

## Testing Locally

1. Start backend: `cd ../backend_tracking && fastapi dev main.py`
2. Seed database: `python seed_database.py` (in backend directory)
3. Start frontend: `python -m http.server 8080`
4. Open: http://localhost:8080
5. Click **Fetch TLE** and add ISS (NORAD ID: 25544)
6. Watch it appear on the map!

## Keyboard Shortcuts

- **F5**: Refresh page
- **F12**: Open developer tools
- **Ctrl/Cmd + Shift + I**: Inspect element

## Debugging Tips

Use browser developer tools (F12):

```javascript
// Console commands for debugging
console.log(positions);  // View position data
console.table(positions); // Tabular view
console.dir(map);        // Inspect map object
```

## Further Reading

- [Leaflet Documentation](https://leafletjs.com/reference.html)
- [Fetch API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [OpenStreetMap](https://www.openstreetmap.org/)
- [TLE Format](https://celestrak.org/columns/v04n03/)
- [SGP4 Propagator](https://en.wikipedia.org/wiki/Simplified_perturbations_models)

## Related Examples

- **Basic HTML Frontend**: `../frontend_html/` (simple CRUD without tracking)
- **Streamlit Frontend**: `../frontend_tracking_streamlit/` (Python alternative)
- **Backend**: `../backend_tracking/` (FastAPI with position calculation)
