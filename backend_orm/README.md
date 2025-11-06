# SQLite Backend API

A FastAPI application with SQLite database for managing satellite data.

## Setup

### Option 1: Using Conda (Recommended)

1. Create the conda environment:
```bash
conda env create -f environment.yml
```

2. Activate the environment:
```bash
conda activate sqlite-backend
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
fastapi dev main.py
```

The API will be available at http://localhost:8000 with interactive documentation.

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **aiosqlite**: Async SQLite driver
- **uvicorn**: ASGI server for running FastAPI applications
- **pydantic**: Data validation library (included with FastAPI)
