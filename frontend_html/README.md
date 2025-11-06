# HTML/JavaScript Frontend for Satellite Management

A simple, single-page web application for managing satellite data through a FastAPI backend. This demonstrates client-server architecture using vanilla HTML, CSS, and JavaScript with the Fetch API.

## Architecture

```
┌─────────────────────┐         HTTP Requests          ┌─────────────────────┐
│   HTML Frontend     │  ────────────────────────────> │   FastAPI Backend   │
│   (index.html)      │  <────────────────────────────  │   (localhost:8000)  │
│   Browser-based     │         JSON Responses         │                     │
└─────────────────────┘                                └─────────────────────┘
```

## Features

- **View All Satellites**: Display all satellites in a table (GET)
- **Create Satellite**: Add new satellites with form validation (POST)
- **Update Satellite (PUT)**: Replace all fields of an existing satellite
- **Update Satellite (PATCH)**: Modify only specific fields with checkboxes
- **Delete Satellite**: Remove satellites with confirmation (DELETE)
- **Responsive Design**: Clean, modern UI with tab navigation
- **Real-time Connection Status**: Visual indicator for API connectivity

## Prerequisites

**You must have the FastAPI backend running first!**

Start either backend from the parent directory:

```bash
# Option 1: SQL backend
cd ../backend_sql
fastapi dev main.py

# Option 2: ORM backend
cd ../backend_orm
fastapi dev main.py
```

The backend should be accessible at http://localhost:8000

## Setup

No installation required! This is a static HTML application that runs directly in your browser.

## Running the Application

### Method 1: Simple HTTP Server (Recommended)

Using Python's built-in HTTP server:

```bash
# Python 3
python -m http.server 8080

# Then open: http://localhost:8080
```

### Method 2: Live Server (VS Code Extension)

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Method 3: Direct File Access

Simply open `index.html` in your web browser:

```bash
# On macOS
open index.html

# On Linux
xdg-open index.html

# On Windows
start index.html
```

**Note**: Some browsers may restrict fetch requests when opening files directly (file:// protocol). Using an HTTP server (Method 1 or 2) is recommended.

## Usage

### 1. Connection Status

The top of the page shows the connection status to the API:
- ✅ Green = Connected to backend
- ❌ Red = Cannot reach backend (start the FastAPI server)

### 2. View All Satellites

Navigate to the **📋 View All** tab:
- Displays all satellites in a sortable table
- Click **🔄 Refresh Data** to reload the list
- Shows ID, acronym, mass, and power for each satellite

### 3. Create a New Satellite

Navigate to the **➕ Create** tab:
- Fill in the form fields:
  - **Acronym**: Satellite name (required)
  - **Mass**: Satellite mass in kg (required)
  - **Power**: Power consumption in watts (required)
- Click **Create Satellite**
- Success/error message will appear at the top

### 4. Update a Satellite (Full Replacement)

Navigate to the **✏️ Update (PUT)** tab:
- Select a satellite from the dropdown
- Form auto-populates with current values
- Modify any or all fields
- Click **Update Satellite**

**Important**: PUT requires all fields to be specified (full replacement).

### 5. Update a Satellite (Partial Update)

Navigate to the **🔧 Update (PATCH)** tab:
- Select a satellite from the dropdown
- View current values in the JSON display
- Check the boxes for fields you want to update
- Only checked fields will be sent to the API
- Click **Patch Satellite**

**Important**: PATCH only updates the fields you check, leaving others unchanged.

### 6. Delete a Satellite

Navigate to the **🗑️ Delete** tab:
- Select a satellite from the dropdown
- Review the confirmation details
- Click **🗑️ Delete Satellite** to confirm
- Click **Cancel** to abort

**Warning**: Deletion cannot be undone!

## HTTP Methods Used

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| Read All  | GET         | `/satellites/` | Retrieve all satellites |
| Create    | POST        | `/satellites/` | Create new satellite |
| Update    | PUT         | `/satellites/{id}` | Replace satellite (all fields) |
| Patch     | PATCH       | `/satellites/{id}` | Update specific fields |
| Delete    | DELETE      | `/satellites/{id}` | Remove satellite |

## Technology Stack

- **HTML5**: Semantic markup and structure
- **CSS3**: Modern styling with flexbox and gradients
- **Vanilla JavaScript**: No frameworks or libraries required
- **Fetch API**: Modern HTTP client for API communication
- **JSON**: Data interchange format

## Code Structure

The application is contained in a single `index.html` file with three main sections:

### 1. HTML Structure
- Tab navigation system
- Forms for each CRUD operation
- Table for displaying satellites
- Message display area

### 2. CSS Styling
- Responsive layout
- Tab-based interface
- Form styling with validation states
- HTTP method badges (color-coded)
- Message styling (success/error/info)

### 3. JavaScript Logic
- `loadSatellites()`: Fetch and display all satellites
- `createSatellite()`: POST new satellite
- `updateSatellite()`: PUT full replacement
- `patchSatellite()`: PATCH partial update
- `deleteSatellite()`: DELETE satellite
- `showTab()`: Tab navigation handler
- `checkConnection()`: Verify API accessibility

## Pedagogical Notes

This example demonstrates:

1. **Client-Server Architecture**: Clear separation between frontend (browser) and backend (API)
2. **REST API Consumption**: Using standard HTTP methods for CRUD operations
3. **Asynchronous JavaScript**: `async/await` with Fetch API
4. **Event Handling**: Form submissions, button clicks, dropdown changes
5. **DOM Manipulation**: Dynamically updating page content
6. **Error Handling**: Try/catch blocks with user-friendly messages
7. **PUT vs PATCH**: Different approaches to updating resources
8. **Form Validation**: HTML5 validation with JavaScript checks

## Troubleshooting

### CORS Errors

If you see CORS (Cross-Origin Resource Sharing) errors in the browser console:

1. **Solution 1**: Use an HTTP server (Method 1 or 2 above) instead of opening the file directly
2. **Solution 2**: Ensure the FastAPI backend is running with CORS enabled (already configured in the example backends)

### "Cannot connect to API" Message

- Verify the backend is running at http://localhost:8000
- Check the backend URL in the browser: http://localhost:8000/docs
- Ensure no firewall is blocking port 8000

### Changes Not Appearing

- Click the **🔄 Refresh Data** button in the View All tab
- Check the browser console (F12) for JavaScript errors
- Verify the backend received the request (check backend terminal output)

### Fetch Requests Blocked

If using the `file://` protocol (opening HTML directly):
- Use Method 1 or 2 to run with an HTTP server
- Modern browsers restrict fetch from file:// for security

## Comparison with Streamlit Frontend

| Feature | HTML Frontend | Streamlit Frontend |
|---------|--------------|-------------------|
| Language | HTML/CSS/JavaScript | Python |
| Setup | No installation | pip/conda install |
| Learning Curve | Higher (3 languages) | Lower (Python only) |
| Customization | Full control | Limited to Streamlit widgets |
| Deployment | Static file server | Python server |
| Best For | Web development learning | Rapid prototyping, data apps |

## Files

- **index.html**: Complete application (HTML, CSS, JavaScript)
- **README.md**: This documentation file

## Browser Compatibility

Works with all modern browsers:
- Chrome/Edge (Chromium-based)
- Firefox
- Safari
- Opera

Requires JavaScript enabled.
