"""
FastAPI Backend with Satellite Tracking

This backend extends the basic satellite CRUD operations with real-time
position tracking using Two-Line Element (TLE) orbital data and the
Skyfield astronomical library.

TLE Data Sources:
- Celestrak: https://celestrak.org/NORAD/elements/
- Space-Track: https://www.space-track.org/ (requires free account)
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone

import aiosqlite
import requests
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from skyfield.api import EarthSatellite, load, wgs84


# ============================================
# Pydantic Models
# ============================================


class SatelliteCreate(BaseModel):
    """Model for creating a new satellite with TLE data."""

    name: str = Field(..., description="Satellite name or acronym")
    norad_id: int = Field(..., description="NORAD catalog ID", gt=0)
    tle_line1: str = Field(..., description="TLE Line 1", min_length=69, max_length=69)
    tle_line2: str = Field(..., description="TLE Line 2", min_length=69, max_length=69)


class SatelliteRead(BaseModel):
    """Model for reading satellite data."""

    id: int
    name: str
    norad_id: int
    tle_line1: str
    tle_line2: str
    tle_updated: str


class SatellitePosition(BaseModel):
    """Model for satellite position at a specific time."""

    satellite_id: int
    name: str
    norad_id: int
    latitude: float = Field(..., description="Latitude in degrees (-90 to 90)")
    longitude: float = Field(..., description="Longitude in degrees (-180 to 180)")
    altitude_km: float = Field(..., description="Altitude above Earth in kilometers")
    timestamp: str = Field(..., description="ISO 8601 timestamp")


class TLEUpdate(BaseModel):
    """Model for updating TLE data."""

    tle_line1: str = Field(..., min_length=69, max_length=69)
    tle_line2: str = Field(..., min_length=69, max_length=69)


# ============================================
# Database Setup
# ============================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
    async with aiosqlite.connect("satellites.db") as con:
        await con.execute(
            """
            CREATE TABLE IF NOT EXISTS Satellites (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                NORAD_ID INTEGER UNIQUE NOT NULL,
                TLE_Line1 TEXT NOT NULL,
                TLE_Line2 TEXT NOT NULL,
                TLE_Updated TEXT NOT NULL
            );
        """
        )
        await con.commit()
    yield


app = FastAPI(
    title="Satellite Tracking API",
    description="FastAPI backend for satellite management with real-time position tracking",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Skyfield timescale (used for time calculations)
ts = load.timescale()


async def connect():
    """Database connection dependency."""
    con = await aiosqlite.connect("satellites.db")
    try:
        yield con
    finally:
        await con.close()


# ============================================
# Helper Functions
# ============================================


def calculate_position(
    tle_line1: str, tle_line2: str, satellite_name: str, time: datetime = None
) -> tuple[float, float, float]:
    """
    Calculate satellite position using TLE data and SGP4 propagator.

    Args:
        tle_line1: First line of TLE data
        tle_line2: Second line of TLE data
        satellite_name: Name for the satellite object
        time: Optional datetime (UTC). Defaults to current time.

    Returns:
        Tuple of (latitude, longitude, altitude_km)
    """
    if time is None:
        time = datetime.now(timezone.utc)

    # Create satellite object from TLE
    satellite = EarthSatellite(tle_line1, tle_line2, satellite_name, ts)

    # Convert datetime to Skyfield time
    t = ts.from_datetime(time)

    # Calculate geocentric position
    geocentric = satellite.at(t)

    # Get geographic coordinates (subpoint on Earth)
    subpoint = wgs84.subpoint(geocentric)

    return (
        subpoint.latitude.degrees,
        subpoint.longitude.degrees,
        subpoint.elevation.km,
    )


def fetch_tle_from_celestrak(norad_id: int) -> tuple[str, str] | None:
    """
    Fetch TLE data from Celestrak by NORAD ID.

    Args:
        norad_id: NORAD catalog ID

    Returns:
        Tuple of (tle_line1, tle_line2) or None if not found
    """
    try:
        # Celestrak GP (General Perturbations) endpoint
        url = f"https://celestrak.org/NORAD/elements/gp.php?CATNR={norad_id}&FORMAT=TLE"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        lines = response.text.strip().split("\n")
        if len(lines) >= 3:
            # Format: Line 0 (name), Line 1 (TLE), Line 2 (TLE)
            return (lines[1].strip(), lines[2].strip())

        return None
    except Exception:
        return None


# ============================================
# API Endpoints
# ============================================


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Satellite Tracking API",
        "docs": "/docs",
        "endpoints": {
            "satellites": "/satellites/",
            "positions": "/satellites/positions",
        },
    }


@app.post("/satellites/", response_model=SatelliteRead, status_code=201)
async def create_satellite(
    sat: SatelliteCreate, con: aiosqlite.Connection = Depends(connect)
) -> SatelliteRead:
    """
    Create a new satellite with TLE orbital data.

    The TLE (Two-Line Element) format is a standard for distributing
    satellite orbital elements. Each line must be exactly 69 characters.
    """
    tle_updated = datetime.now(timezone.utc).isoformat()

    try:
        cur = await con.execute(
            """
            INSERT INTO Satellites (Name, NORAD_ID, TLE_Line1, TLE_Line2, TLE_Updated)
            VALUES (?, ?, ?, ?, ?)
            """,
            (sat.name, sat.norad_id, sat.tle_line1, sat.tle_line2, tle_updated),
        )
        await con.commit()

        return SatelliteRead(
            id=cur.lastrowid,
            name=sat.name,
            norad_id=sat.norad_id,
            tle_line1=sat.tle_line1,
            tle_line2=sat.tle_line2,
            tle_updated=tle_updated,
        )
    except aiosqlite.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"Satellite with NORAD ID {sat.norad_id} already exists",
        )


@app.get("/satellites/", response_model=list[SatelliteRead])
async def read_satellites(
    con: aiosqlite.Connection = Depends(connect),
) -> list[SatelliteRead]:
    """Get all satellites."""
    cur = await con.execute("SELECT * FROM Satellites")
    results = await cur.fetchall()

    return [
        SatelliteRead(
            id=row[0],
            name=row[1],
            norad_id=row[2],
            tle_line1=row[3],
            tle_line2=row[4],
            tle_updated=row[5],
        )
        for row in results
    ]


@app.get("/satellites/positions", response_model=list[SatellitePosition])
async def get_all_positions(
    con: aiosqlite.Connection = Depends(connect),
) -> list[SatellitePosition]:
    """
    Get current positions of all satellites.

    This endpoint calculates positions for all satellites in the database
    at the current time.
    """
    cur = await con.execute("SELECT * FROM Satellites")
    results = await cur.fetchall()

    positions = []
    current_time = datetime.now(timezone.utc)

    for row in results:
        satellite_id, name, norad_id, tle_line1, tle_line2, _ = row

        try:
            lat, lon, alt = calculate_position(tle_line1, tle_line2, name, current_time)

            positions.append(
                SatellitePosition(
                    satellite_id=satellite_id,
                    name=name,
                    norad_id=norad_id,
                    latitude=lat,
                    longitude=lon,
                    altitude_km=alt,
                    timestamp=current_time.isoformat(),
                )
            )
        except Exception:
            # Skip satellites with invalid TLE data
            continue

    return positions


@app.get("/satellites/{id}", response_model=SatelliteRead)
async def read_satellite(
    id: int, con: aiosqlite.Connection = Depends(connect)
) -> SatelliteRead:
    """Get a specific satellite by ID."""
    cur = await con.execute("SELECT * FROM Satellites WHERE ID=? LIMIT 1", (id,))
    result = await cur.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail=f"Satellite {id} not found")

    return SatelliteRead(
        id=result[0],
        name=result[1],
        norad_id=result[2],
        tle_line1=result[3],
        tle_line2=result[4],
        tle_updated=result[5],
    )


@app.get("/satellites/{id}/position", response_model=SatellitePosition)
async def get_satellite_position(
    id: int, con: aiosqlite.Connection = Depends(connect)
) -> SatellitePosition:
    """
    Calculate the current position of a satellite.

    Returns latitude, longitude, and altitude based on the satellite's
    TLE data and current time using the SGP4 orbital propagator.
    """
    # Fetch satellite from database
    cur = await con.execute("SELECT * FROM Satellites WHERE ID=? LIMIT 1", (id,))
    result = await cur.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail=f"Satellite {id} not found")

    satellite_id, name, norad_id, tle_line1, tle_line2, _ = result

    # Calculate position
    try:
        lat, lon, alt = calculate_position(tle_line1, tle_line2, name)

        return SatellitePosition(
            satellite_id=satellite_id,
            name=name,
            norad_id=norad_id,
            latitude=lat,
            longitude=lon,
            altitude_km=alt,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to calculate position: {str(e)}"
        )


@app.put("/satellites/{id}/tle", response_model=SatelliteRead)
async def update_tle(
    id: int, tle: TLEUpdate, con: aiosqlite.Connection = Depends(connect)
) -> SatelliteRead:
    """
    Update the TLE data for a satellite.

    TLE data becomes outdated over time due to atmospheric drag and other
    perturbations. This endpoint allows refreshing with current TLE data.
    """
    tle_updated = datetime.now(timezone.utc).isoformat()

    cur = await con.execute(
        """
        UPDATE Satellites
        SET TLE_Line1=?, TLE_Line2=?, TLE_Updated=?
        WHERE ID=?
        """,
        (tle.tle_line1, tle.tle_line2, tle_updated, id),
    )

    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Satellite {id} not found")

    await con.commit()

    # Fetch updated satellite
    cur = await con.execute("SELECT * FROM Satellites WHERE ID=? LIMIT 1", (id,))
    result = await cur.fetchone()

    return SatelliteRead(
        id=result[0],
        name=result[1],
        norad_id=result[2],
        tle_line1=result[3],
        tle_line2=result[4],
        tle_updated=result[5],
    )


@app.delete("/satellites/{id}", status_code=204)
async def delete_satellite(id: int, con: aiosqlite.Connection = Depends(connect)):
    """Delete a satellite."""
    cur = await con.execute("DELETE FROM Satellites WHERE ID=?", (id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Satellite {id} not found")
    await con.commit()


@app.get("/satellites/fetch-tle/{norad_id}")
async def fetch_tle(norad_id: int):
    """
    Fetch TLE data from Celestrak for a given NORAD ID.

    This is a utility endpoint for getting current TLE data from
    Celestrak's public database.
    """
    tle_data = fetch_tle_from_celestrak(norad_id)

    if tle_data is None:
        raise HTTPException(
            status_code=404, detail=f"TLE data not found for NORAD ID {norad_id}"
        )

    return {"norad_id": norad_id, "tle_line1": tle_data[0], "tle_line2": tle_data[1]}
