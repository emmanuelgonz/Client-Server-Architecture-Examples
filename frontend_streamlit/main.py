"""
Streamlit Frontend for Satellite Management System

This application provides a web interface for managing satellite data
through a FastAPI backend. It demonstrates client-server architecture
where the frontend (Streamlit) consumes a REST API (FastAPI).

Make sure the FastAPI backend is running at http://localhost:8000
before starting this application.
"""

import streamlit as st
import requests
from typing import Optional


# Configuration
API_BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{API_BASE_URL}/satellites/"


def get_all_satellites() -> list[dict]:
    """
    Fetch all satellites from the API.

    Returns:
        List of satellite dictionaries
    """
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch satellites: {e}")
        return []


def get_satellite(satellite_id: int) -> Optional[dict]:
    """
    Fetch a specific satellite by ID.

    Args:
        satellite_id: The ID of the satellite to fetch

    Returns:
        Satellite dictionary or None if not found
    """
    try:
        response = requests.get(f"{API_ENDPOINT}{satellite_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch satellite {satellite_id}: {e}")
        return None


def create_satellite(acronym: str, mass: float, power: float) -> bool:
    """
    Create a new satellite via the API.

    Args:
        acronym: Satellite acronym
        mass: Satellite mass in kg
        power: Satellite power in W

    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.post(
            API_ENDPOINT,
            json={"acronym": acronym, "mass": mass, "power": power}
        )
        response.raise_for_status()
        st.success(f"Created satellite with ID: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to create satellite: {e}")
        return False


def update_satellite(satellite_id: int, acronym: str, mass: float, power: float) -> bool:
    """
    Update an existing satellite (full update with PUT).

    Args:
        satellite_id: The ID of the satellite to update
        acronym: New satellite acronym
        mass: New satellite mass in kg
        power: New satellite power in W

    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.put(
            f"{API_ENDPOINT}{satellite_id}",
            json={"acronym": acronym, "mass": mass, "power": power}
        )
        response.raise_for_status()
        st.success(f"Updated satellite {satellite_id}")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to update satellite: {e}")
        return False


def patch_satellite(satellite_id: int, **kwargs) -> bool:
    """
    Partially update a satellite (PATCH).

    Args:
        satellite_id: The ID of the satellite to update
        **kwargs: Fields to update (acronym, mass, power)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Only send fields that are provided
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        response = requests.patch(
            f"{API_ENDPOINT}{satellite_id}",
            json=update_data
        )
        response.raise_for_status()
        st.success(f"Partially updated satellite {satellite_id}")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to patch satellite: {e}")
        return False


def delete_satellite(satellite_id: int) -> bool:
    """
    Delete a satellite from the API.

    Args:
        satellite_id: The ID of the satellite to delete

    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.delete(f"{API_ENDPOINT}{satellite_id}")
        response.raise_for_status()
        st.success(f"Deleted satellite {satellite_id}")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to delete satellite: {e}")
        return False


# ============================================
# Streamlit UI
# ============================================

st.set_page_config(
    page_title="Satellite Manager",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ Satellite Management System")
st.markdown("""
This application demonstrates a **client-server architecture** where:
- **Backend**: FastAPI REST API (http://localhost:8000)
- **Frontend**: Streamlit web interface (this application)
- **Communication**: HTTP requests (GET, POST, PUT, PATCH, DELETE)
""")

# Check if API is accessible
try:
    response = requests.get(f"{API_BASE_URL}/docs", timeout=2)
    st.success(f"✅ Connected to API at {API_BASE_URL}")
except requests.exceptions.RequestException:
    st.error(f"❌ Cannot connect to API at {API_BASE_URL}. Make sure the backend is running!")
    st.info("Start the backend with: `cd ../backend_sql && fastapi dev main.py`")
    st.stop()

# Create tabs for different operations
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 View All",
    "➕ Create",
    "✏️ Update (PUT)",
    "🔧 Update (PATCH)",
    "🗑️ Delete"
])

# Tab 1: View all satellites
with tab1:
    st.header("All Satellites")
    st.markdown("**HTTP Method**: `GET /satellites/`")

    if st.button("🔄 Refresh Data", key="refresh_all"):
        st.rerun()

    satellites = get_all_satellites()

    if satellites:
        st.dataframe(
            satellites,
            use_container_width=True,
            hide_index=True
        )
        st.caption(f"Total satellites: {len(satellites)}")
    else:
        st.info("No satellites found. Create one in the **Create** tab!")

# Tab 2: Create new satellite
with tab2:
    st.header("Create New Satellite")
    st.markdown("**HTTP Method**: `POST /satellites/`")

    with st.form("create_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            new_acronym = st.text_input(
                "Acronym",
                placeholder="e.g., ISS",
                help="Satellite acronym or name"
            )

        with col2:
            new_mass = st.number_input(
                "Mass (kg)",
                min_value=0.0,
                value=100.0,
                step=10.0,
                help="Satellite mass in kilograms"
            )

        with col3:
            new_power = st.number_input(
                "Power (W)",
                min_value=0.0,
                value=50.0,
                step=5.0,
                help="Satellite power consumption in watts"
            )

        submitted = st.form_submit_button("Create Satellite", type="primary")

        if submitted:
            if not new_acronym:
                st.error("Acronym is required!")
            else:
                if create_satellite(new_acronym, new_mass, new_power):
                    st.rerun()

# Tab 3: Update satellite (PUT - full replacement)
with tab3:
    st.header("Update Satellite (Full Replacement)")
    st.markdown("**HTTP Method**: `PUT /satellites/{id}`")
    st.info("PUT replaces **all** fields of the satellite with new values.")

    satellites = get_all_satellites()

    if satellites:
        satellite_options = {
            f"ID {s['id']}: {s['acronym']}": s['id']
            for s in satellites
        }

        selected_sat = st.selectbox(
            "Select Satellite to Update",
            options=satellite_options.keys(),
            key="put_select"
        )

        if selected_sat:
            satellite_id = satellite_options[selected_sat]
            current_sat = next(s for s in satellites if s['id'] == satellite_id)

            with st.form("update_form"):
                st.caption(f"Current values for ID {satellite_id}:")

                col1, col2, col3 = st.columns(3)

                with col1:
                    update_acronym = st.text_input(
                        "New Acronym",
                        value=current_sat['acronym']
                    )

                with col2:
                    update_mass = st.number_input(
                        "New Mass (kg)",
                        value=float(current_sat['mass']),
                        step=10.0
                    )

                with col3:
                    update_power = st.number_input(
                        "New Power (W)",
                        value=float(current_sat['power']),
                        step=5.0
                    )

                submitted = st.form_submit_button("Update Satellite", type="primary")

                if submitted:
                    if update_satellite(satellite_id, update_acronym, update_mass, update_power):
                        st.rerun()
    else:
        st.info("No satellites available to update.")

# Tab 4: Patch satellite (PATCH - partial update)
with tab4:
    st.header("Update Satellite (Partial Update)")
    st.markdown("**HTTP Method**: `PATCH /satellites/{id}`")
    st.info("PATCH updates **only** the fields you specify, leaving others unchanged.")

    satellites = get_all_satellites()

    if satellites:
        satellite_options = {
            f"ID {s['id']}: {s['acronym']}": s['id']
            for s in satellites
        }

        selected_sat = st.selectbox(
            "Select Satellite to Patch",
            options=satellite_options.keys(),
            key="patch_select"
        )

        if selected_sat:
            satellite_id = satellite_options[selected_sat]
            current_sat = next(s for s in satellites if s['id'] == satellite_id)

            with st.form("patch_form"):
                st.caption(f"Current values for ID {satellite_id}:")
                st.json(current_sat)

                st.markdown("**Update only the fields you want to change:**")

                col1, col2, col3 = st.columns(3)

                with col1:
                    patch_acronym_enable = st.checkbox("Update Acronym")
                    patch_acronym = st.text_input(
                        "New Acronym",
                        value=current_sat['acronym'],
                        disabled=not patch_acronym_enable
                    ) if patch_acronym_enable else None

                with col2:
                    patch_mass_enable = st.checkbox("Update Mass")
                    patch_mass = st.number_input(
                        "New Mass (kg)",
                        value=float(current_sat['mass']),
                        step=10.0,
                        disabled=not patch_mass_enable
                    ) if patch_mass_enable else None

                with col3:
                    patch_power_enable = st.checkbox("Update Power")
                    patch_power = st.number_input(
                        "New Power (W)",
                        value=float(current_sat['power']),
                        step=5.0,
                        disabled=not patch_power_enable
                    ) if patch_power_enable else None

                submitted = st.form_submit_button("Patch Satellite", type="primary")

                if submitted:
                    if not any([patch_acronym, patch_mass is not None, patch_power is not None]):
                        st.warning("Select at least one field to update!")
                    else:
                        kwargs = {}
                        if patch_acronym:
                            kwargs['acronym'] = patch_acronym
                        if patch_mass is not None:
                            kwargs['mass'] = patch_mass
                        if patch_power is not None:
                            kwargs['power'] = patch_power

                        if patch_satellite(satellite_id, **kwargs):
                            st.rerun()
    else:
        st.info("No satellites available to patch.")

# Tab 5: Delete satellite
with tab5:
    st.header("Delete Satellite")
    st.markdown("**HTTP Method**: `DELETE /satellites/{id}`")
    st.warning("⚠️ This action cannot be undone!")

    satellites = get_all_satellites()

    if satellites:
        satellite_options = {
            f"ID {s['id']}: {s['acronym']} (Mass: {s['mass']}kg, Power: {s['power']}W)": s['id']
            for s in satellites
        }

        selected_sat = st.selectbox(
            "Select Satellite to Delete",
            options=satellite_options.keys(),
            key="delete_select"
        )

        if selected_sat:
            satellite_id = satellite_options[selected_sat]

            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                if st.button("🗑️ Delete Satellite", type="primary"):
                    if delete_satellite(satellite_id):
                        st.rerun()

            with col2:
                st.button("Cancel", disabled=True)
    else:
        st.info("No satellites available to delete.")

# Footer
st.markdown("---")
st.caption("IEE 305 - Information Systems Engineering | Client-Server Architecture Demo")
