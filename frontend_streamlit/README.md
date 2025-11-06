# Streamlit Frontend for Satellite Management

A modern Python-based web interface for managing satellite data through a FastAPI backend. This demonstrates client-server architecture where the frontend (Streamlit) consumes a REST API.

## Architecture

```
┌─────────────────────┐         HTTP Requests          ┌─────────────────────┐
│  Streamlit Frontend │  ────────────────────────────> │   FastAPI Backend   │
│   (This App)        │  <────────────────────────────  │   (localhost:8000)  │
│  localhost:8501     │         JSON Responses         │                     │
└─────────────────────┘                                └─────────────────────┘
```

## Features

- **View All Satellites**: Display all satellites in a sortable table (GET)
- **Create Satellite**: Add new satellites with validation (POST)
- **Update Satellite (PUT)**: Replace all fields of an existing satellite
- **Update Satellite (PATCH)**: Modify only specific fields
- **Delete Satellite**: Remove satellites from the database (DELETE)

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

### Option 1: Using Conda (Recommended)

1. Create the conda environment:
```bash
conda env create -f environment.yml
```

2. Activate the environment:
```bash
conda activate streamlit-frontend
```

### Option 2: Using pip

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
streamlit run main.py
```

The application will automatically open in your browser at http://localhost:8501

## Usage

### 1. View All Satellites
- Navigate to the **📋 View All** tab
- Click **🔄 Refresh Data** to reload the satellite list
- Data is displayed in an interactive table

### 2. Create a New Satellite
- Navigate to the **➕ Create** tab
- Fill in the form:
  - **Acronym**: Satellite name/acronym (e.g., "ISS")
  - **Mass**: Satellite mass in kilograms
  - **Power**: Power consumption in watts
- Click **Create Satellite**

### 3. Update a Satellite (Full Replacement)
- Navigate to the **✏️ Update (PUT)** tab
- Select a satellite from the dropdown
- Modify all fields (all fields must be provided)
- Click **Update Satellite**

**Note**: PUT replaces the entire resource. All fields must be specified.

### 4. Update a Satellite (Partial Update)
- Navigate to the **🔧 Update (PATCH)** tab
- Select a satellite from the dropdown
- Check the boxes for fields you want to update
- Modify only those fields
- Click **Patch Satellite**

**Note**: PATCH only updates the specified fields, leaving others unchanged.

### 5. Delete a Satellite
- Navigate to the **🗑️ Delete** tab
- Select a satellite from the dropdown
- Click **🗑️ Delete Satellite**

**Warning**: This action cannot be undone!

## HTTP Methods Used

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| Read All  | GET         | `/satellites/` | Retrieve all satellites |
| Read One  | GET         | `/satellites/{id}` | Retrieve specific satellite |
| Create    | POST        | `/satellites/` | Create new satellite |
| Update    | PUT         | `/satellites/{id}` | Replace satellite (all fields) |
| Patch     | PATCH       | `/satellites/{id}` | Update specific fields |
| Delete    | DELETE      | `/satellites/{id}` | Remove satellite |

## Technology Stack

- **Streamlit**: Python web framework for data applications
- **requests**: HTTP library for API communication
- **Python 3.11**: Programming language

## Pedagogical Notes

This example demonstrates:

1. **Client-Server Separation**: Frontend and backend run as separate processes
2. **REST API Consumption**: Using HTTP methods to interact with resources
3. **Stateless Communication**: Each request is independent
4. **Data Validation**: Both frontend (Streamlit widgets) and backend (Pydantic) validate data
5. **CRUD Operations**: Complete Create, Read, Update, Delete functionality
6. **PUT vs PATCH**: Difference between full replacement and partial updates

## Troubleshooting

### "Cannot connect to API" Error

- **Check backend is running**: Visit http://localhost:8000/docs
- **Check port**: Backend must be on port 8000
- **Restart backend**: Stop and restart the FastAPI application

### Port Already in Use

If Streamlit's default port (8501) is in use, specify a different port:

```bash
streamlit run main.py --server.port 8502
```

### Changes Not Appearing

- Click the **🔄 Refresh Data** button in the View All tab
- The app automatically refreshes after Create/Update/Delete operations

## Dependencies

- **streamlit**: Web application framework
- **requests**: HTTP client library

See `requirements.txt` for specific versions.
