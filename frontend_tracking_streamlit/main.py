"""
Streamlit Frontend with Live Satellite Tracking

This application provides a web interface for managing satellites and
visualizing their real-time positions on a 2D map and 3D globe.

Make sure the FastAPI backend is running at http://localhost:8000
before starting this application.
"""

import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go
from datetime import datetime
from typing import Optional


# Configuration
API_BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{API_BASE_URL}/satellites/"


# ============================================
# API Helper Functions
# ============================================


def get_all_satellites() -> list[dict]:
    """Fetch all satellites from the API."""
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch satellites: {e}")
        return []


def get_satellite_position(satellite_id: int) -> Optional[dict]:
    """Fetch current position of a satellite."""
    try:
        response = requests.get(f"{API_ENDPOINT}{satellite_id}/position")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch position for satellite {satellite_id}: {e}")
        return None


def get_all_positions() -> list[dict]:
    """Fetch current positions of all satellites."""
    try:
        response = requests.get(f"{API_BASE_URL}/satellites/positions")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch positions: {e}")
        return []


def create_satellite(name: str, norad_id: int, tle_line1: str, tle_line2: str) -> bool:
    """Create a new satellite via the API."""
    try:
        response = requests.post(
            API_ENDPOINT,
            json={
                "name": name,
                "norad_id": norad_id,
                "tle_line1": tle_line1,
                "tle_line2": tle_line2,
            },
        )
        response.raise_for_status()
        result = response.json()
        st.success(f"Created satellite '{name}' with ID: {result['id']}")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to create satellite: {e}")
        return False


def delete_satellite(satellite_id: int) -> bool:
    """Delete a satellite from the API."""
    try:
        response = requests.delete(f"{API_ENDPOINT}{satellite_id}")
        response.raise_for_status()
        st.success(f"Deleted satellite {satellite_id}")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to delete satellite: {e}")
        return False


def fetch_tle_from_api(norad_id: int) -> Optional[dict]:
    """Fetch TLE data from Celestrak via the backend API."""
    try:
        response = requests.get(f"{API_BASE_URL}/satellites/fetch-tle/{norad_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch TLE data: {e}")
        return None


# ============================================
# Visualization Functions
# ============================================


def create_2d_map(positions: list[dict]):
    """Create a 2D map with satellite positions using PyDeck."""
    if not positions:
        st.info("No satellite positions to display.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(positions)
    df = df.rename(columns={"latitude": "lat", "longitude": "lon"})

    # Create PyDeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=[255, 0, 0, 200],
        get_radius=100000,  # 100 km radius
        pickable=True,
    )

    # Set view state (center on first satellite or default)
    view_state = pdk.ViewState(
        latitude=df["lat"].mean() if len(df) > 0 else 0,
        longitude=df["lon"].mean() if len(df) > 0 else 0,
        zoom=1,
        pitch=0,
    )

    # Create map (using Carto basemap - no API key required)
    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{name}\nLat: {lat:.2f}°\nLon: {lon:.2f}°\nAlt: {altitude_km:.0f} km"},
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        )
    )


def create_3d_globe(positions: list[dict]):
    """Create a 3D globe with satellite positions using Plotly."""
    if not positions:
        st.info("No satellite positions to display.")
        return

    df = pd.DataFrame(positions)

    # Create 3D scatter plot on globe
    fig = go.Figure()

    # Add satellite positions
    fig.add_trace(
        go.Scattergeo(
            lon=df["longitude"],
            lat=df["latitude"],
            text=df["name"],
            mode="markers+text",
            marker=dict(size=8, color="red", line=dict(width=1, color="white")),
            textposition="top center",
            textfont=dict(size=8, color="white"),
            hovertemplate="<b>%{text}</b><br>"
            + "Lat: %{lat:.2f}°<br>"
            + "Lon: %{lon:.2f}°<br>"
            + "Alt: %{customdata:.0f} km<extra></extra>",
            customdata=df["altitude_km"],
        )
    )

    # Update layout for globe view
    fig.update_geos(
        projection_type="orthographic",
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor="rgb(243, 243, 243)",
        coastlinecolor="rgb(204, 204, 204)",
        countrycolor="rgb(204, 204, 204)",
        bgcolor="rgb(10, 10, 10)",
    )

    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="rgb(10, 10, 10)",
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================
# Streamlit UI
# ============================================

st.set_page_config(
    page_title="Satellite Tracker", page_icon="🛰️", layout="wide"
)

st.title("🛰️ Live Satellite Tracking System")
st.markdown("""
Track satellites in real-time using Two-Line Element (TLE) orbital data.
Positions are calculated using the **SGP4 propagator** from the Skyfield library.
""")

# Check API connection
try:
    response = requests.get(f"{API_BASE_URL}/", timeout=2)
    st.success(f"✅ Connected to API at {API_BASE_URL}")
except requests.exceptions.RequestException:
    st.error(f"❌ Cannot connect to API at {API_BASE_URL}. Make sure the backend is running!")
    st.info("Start the backend with: `cd ../backend_tracking && fastapi dev main.py`")
    st.stop()

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🗺️ 2D Map", "🌍 3D Globe", "📋 Satellites", "➕ Add Satellite", "🗑️ Delete"]
)

# Tab 1: 2D Map
with tab1:
    st.header("Live Satellite Positions (2D Map)")
    st.markdown("**Real-time positions** calculated from TLE orbital elements.")

    col1, col2 = st.columns([1, 4])

    with col1:
        if st.button("🔄 Refresh Positions", key="refresh_2d"):
            st.rerun()

        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

    with col2:
        positions = get_all_positions()
        if positions:
            st.info(f"Tracking {len(positions)} satellites")

    create_2d_map(positions)

    # Show position data table
    if positions:
        st.subheader("Position Data")
        df = pd.DataFrame(positions)
        df = df[["name", "norad_id", "latitude", "longitude", "altitude_km"]]
        df["latitude"] = df["latitude"].round(2)
        df["longitude"] = df["longitude"].round(2)
        df["altitude_km"] = df["altitude_km"].round(0)
        st.dataframe(df, use_container_width=True, hide_index=True)

# Tab 2: 3D Globe
with tab2:
    st.header("Live Satellite Positions (3D Globe)")
    st.markdown("**Interactive 3D visualization** showing satellites on Earth.")

    col1, col2 = st.columns([1, 4])

    with col1:
        if st.button("🔄 Refresh Positions", key="refresh_3d"):
            st.rerun()

        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

    with col2:
        positions = get_all_positions()
        if positions:
            st.info(f"Tracking {len(positions)} satellites")

    create_3d_globe(positions)

# Tab 3: View All Satellites
with tab3:
    st.header("All Satellites in Database")
    st.markdown("**Satellite catalog** with TLE orbital data.")

    if st.button("🔄 Refresh", key="refresh_list"):
        st.rerun()

    satellites = get_all_satellites()

    if satellites:
        # Show summary
        st.metric("Total Satellites", len(satellites))

        # Show detailed table
        st.subheader("Satellite Details")
        for sat in satellites:
            with st.expander(f"{sat['name']} (NORAD ID: {sat['norad_id']})"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Database ID:**", sat["id"])
                    st.write("**NORAD ID:**", sat["norad_id"])
                    st.write("**Last TLE Update:**", sat["tle_updated"])

                with col2:
                    st.write("**TLE Line 1:**")
                    st.code(sat["tle_line1"], language=None)
                    st.write("**TLE Line 2:**")
                    st.code(sat["tle_line2"], language=None)

                # Get current position
                if st.button(f"📍 Get Current Position", key=f"pos_{sat['id']}"):
                    pos = get_satellite_position(sat["id"])
                    if pos:
                        st.write(f"**Latitude:** {pos['latitude']:.4f}°")
                        st.write(f"**Longitude:** {pos['longitude']:.4f}°")
                        st.write(f"**Altitude:** {pos['altitude_km']:.2f} km")
                        st.write(f"**Timestamp:** {pos['timestamp']}")
    else:
        st.info("No satellites in database. Add one in the **Add Satellite** tab!")

# Tab 4: Add Satellite
with tab4:
    st.header("Add New Satellite")
    st.markdown("Add a satellite using **TLE (Two-Line Element)** orbital data.")

    # Method selection
    method = st.radio(
        "Input Method",
        ["Fetch from Celestrak (by NORAD ID)", "Manual TLE Entry"],
        horizontal=True,
    )

    if method == "Fetch from Celestrak (by NORAD ID)":
        st.subheader("Fetch TLE from Celestrak")
        st.markdown(
            """
        Enter a NORAD Catalog ID to automatically fetch current TLE data.

        **Popular Satellites:**
        - ISS: 25544
        - Hubble: 20580
        - Starlink-1007: 44713
        - NOAA 18: 28654
        """
        )

        with st.form("fetch_tle_form"):
            norad_id = st.number_input(
                "NORAD Catalog ID", min_value=1, value=25544, step=1
            )

            fetch_submitted = st.form_submit_button("Fetch TLE Data", type="primary")

            if fetch_submitted:
                with st.spinner("Fetching TLE from Celestrak..."):
                    tle_data = fetch_tle_from_api(norad_id)

                    if tle_data:
                        st.success("TLE data fetched successfully!")
                        st.session_state["fetched_norad_id"] = norad_id
                        st.session_state["fetched_tle1"] = tle_data["tle_line1"]
                        st.session_state["fetched_tle2"] = tle_data["tle_line2"]
                        st.rerun()

        # If TLE was fetched, show creation form
        if "fetched_tle1" in st.session_state:
            st.success("TLE data loaded! Now enter a name for the satellite.")

            with st.form("create_from_fetch"):
                name = st.text_input("Satellite Name", placeholder="e.g., ISS (ZARYA)")

                st.text("TLE Line 1:")
                st.code(st.session_state["fetched_tle1"], language=None)

                st.text("TLE Line 2:")
                st.code(st.session_state["fetched_tle2"], language=None)

                create_submitted = st.form_submit_button("Create Satellite", type="primary")

                if create_submitted and name:
                    if create_satellite(
                        name,
                        st.session_state["fetched_norad_id"],
                        st.session_state["fetched_tle1"],
                        st.session_state["fetched_tle2"],
                    ):
                        # Clear session state
                        del st.session_state["fetched_norad_id"]
                        del st.session_state["fetched_tle1"]
                        del st.session_state["fetched_tle2"]
                        st.rerun()

    else:  # Manual TLE Entry
        st.subheader("Manual TLE Entry")
        st.markdown(
            """
        Enter TLE data manually. Each line must be exactly **69 characters**.

        Find TLE data at:
        - [Celestrak](https://celestrak.org/NORAD/elements/)
        - [Space-Track](https://www.space-track.org/) (requires free account)
        """
        )

        with st.form("manual_tle_form"):
            name = st.text_input("Satellite Name", placeholder="e.g., ISS (ZARYA)")

            norad_id = st.number_input(
                "NORAD Catalog ID", min_value=1, value=25544, step=1
            )

            tle_line1 = st.text_input(
                "TLE Line 1 (69 characters)",
                max_chars=69,
                placeholder="1 25544U 98067A   24310.51118287  .00013207...",
            )

            tle_line2 = st.text_input(
                "TLE Line 2 (69 characters)",
                max_chars=69,
                placeholder="2 25544  51.6406 308.8287 0005935...",
            )

            submitted = st.form_submit_button("Create Satellite", type="primary")

            if submitted:
                # Validate
                if not name:
                    st.error("Satellite name is required!")
                elif len(tle_line1) != 69:
                    st.error(f"TLE Line 1 must be exactly 69 characters (currently {len(tle_line1)})")
                elif len(tle_line2) != 69:
                    st.error(f"TLE Line 2 must be exactly 69 characters (currently {len(tle_line2)})")
                else:
                    if create_satellite(name, norad_id, tle_line1, tle_line2):
                        st.rerun()

# Tab 5: Delete Satellite
with tab5:
    st.header("Delete Satellite")
    st.warning("⚠️ This action cannot be undone!")

    satellites = get_all_satellites()

    if satellites:
        satellite_options = {f"{s['name']} (ID: {s['id']})": s["id"] for s in satellites}

        selected_sat = st.selectbox(
            "Select Satellite to Delete", options=satellite_options.keys()
        )

        if selected_sat:
            satellite_id = satellite_options[selected_sat]

            col1, col2 = st.columns([1, 3])

            with col1:
                if st.button("🗑️ Delete Satellite", type="primary"):
                    if delete_satellite(satellite_id):
                        st.rerun()
    else:
        st.info("No satellites available to delete.")

# Footer
st.markdown("---")
st.caption(
    "IEE 305 - Information Systems Engineering | Real-Time Satellite Tracking with TLE Data"
)
