from contextlib import asynccontextmanager

import aiosqlite
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class SatelliteCreate(BaseModel):
    acronym: str
    mass: float
    power: float


class SatelliteRead(BaseModel):
    id: int
    acronym: str
    mass: float
    power: float


class SatelliteUpdate(BaseModel):
    acronym: str | None = None
    mass: float | None = None
    power: float | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with aiosqlite.connect("satellites.db") as con:
        await con.execute(
            """
            CREATE TABLE IF NOT EXISTS Satellites (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Acronym TEXT,
                Mass REAL,
                Power REAL
            );
        """
        )
    yield


app = FastAPI(lifespan=lifespan, docs_url="/")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def connect():
    con = await aiosqlite.connect("satellites.db")
    try:
        yield con
    finally:
        await con.close()


@app.post("/satellites/")
async def create_satellite(
    sat: SatelliteCreate, con: aiosqlite.Connection = Depends(connect)
) -> int:
    cur = await con.execute(
        "INSERT INTO Satellites (Acronym, Mass, Power) VALUES (?, ?, ?)",
        (sat.acronym, sat.mass, sat.power),
    )
    await con.commit()
    return cur.lastrowid


@app.get("/satellites/{id}", response_model=SatelliteRead)
async def read_satellite(
    id: int, con: aiosqlite.Connection = Depends(connect)
) -> SatelliteRead:
    cur = await con.execute("SELECT * FROM Satellites WHERE ID=? LIMIT 1", (id,))
    result = await cur.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail=f"Satellite {id} not found")
    return SatelliteRead(
        id=result[0], acronym=result[1], mass=result[2], power=result[3]
    )


@app.get("/satellites/", response_model=list[SatelliteRead])
async def read_satellites(
    con: aiosqlite.Connection = Depends(connect),
) -> list[SatelliteRead]:
    cur = await con.execute("SELECT * FROM Satellites")
    results = await cur.fetchall()
    return [
        SatelliteRead(id=result[0], acronym=result[1], mass=result[2], power=result[3])
        for result in results
    ]


@app.put("/satellites/{id}")
async def update_satellite(
    id: int, sat: SatelliteCreate, con: aiosqlite.Connection = Depends(connect)
):
    cur = await con.execute(
        """
        UPDATE Satellites
        SET Acronym=?, Mass=?, Power=?
        WHERE ID=?
        """,
        (sat.acronym, sat.mass, sat.power, id),
    )
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Satellite {id} not found")
    await con.commit()


@app.patch("/satellites/{id}")
async def update_satellite_partial(
    id: int, sat: SatelliteUpdate, con: aiosqlite.Connection = Depends(connect)
):
    updated = False

    if sat.acronym is not None:
        cur = await con.execute(
            "UPDATE Satellites SET Acronym=? WHERE ID=?", (sat.acronym, id)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Satellite {id} not found")
        updated = True

    if sat.mass is not None:
        cur = await con.execute(
            "UPDATE Satellites SET Mass=? WHERE ID=?", (sat.mass, id)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Satellite {id} not found")
        updated = True

    if sat.power is not None:
        cur = await con.execute(
            "UPDATE Satellites SET Power=? WHERE ID=?", (sat.power, id)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Satellite {id} not found")
        updated = True

    if updated:
        await con.commit()


@app.delete("/satellites/{id}")
async def delete_satellite(id: int, con: aiosqlite.Connection = Depends(connect)):
    cur = await con.execute("DELETE FROM Satellites WHERE ID=?", (id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"Satellite {id} not found")
    await con.commit()
