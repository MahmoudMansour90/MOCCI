import os, json, requests
import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Utilities Reliability Map", layout="wide")

# ---- PASSWORD (tolerant) ----
PASSWORD = st.secrets.get("APP_PASSWORD")
entered = st.text_input("Enter password:", type="password")
if PASSWORD and entered != PASSWORD:
    st.stop()

# ---- DATA SOURCE ----
DATA_PATH = "utilities_state_level_reliability_flag.geojson"  # local (optional)
DATA_URL  = st.secrets.get("DATA_URL")  # OneDrive/Drive direct link

def load_geojson():
    # 1) Try local file
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    # 2) Try remote URL
    if DATA_URL:
        try:
            r = requests.get(DATA_URL, timeout=60)
            r.raise_for_status()
            # Try JSON parse
            try:
                return r.json()
            except Exception:
                # Some hosts serve as text; try manual parse
                return json.loads(r.content.decode("utf-8"))
        except Exception as e:
            st.error(f"Could not fetch data from DATA_URL. Details: {e}")
            st.stop()
    # 3) Nothing found
    st.error("No data file found. Add the GeoJSON to the repo OR set DATA_URL in Secrets.")
    st.stop()

geojson_data = load_geojson()

# ---- MAP ----
st.title("Utilities Reliability Map (EIA-861, State-Level)")
st.caption("Green = reported reliability; Red = did not report")

m = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles="cartodbpositron")

def style_fn(ft):
    flag = str(ft["properties"].get("ReportFlag", "No")).lower()
    return {
        "fillColor": "green" if flag == "yes" else "red",
        "color": "black",
        "weight": 0.3,
        "fillOpacity": 0.6,
    }

folium.GeoJson(
    geojson_data,
    style_function=style_fn,
    tooltip=folium.GeoJsonTooltip(
        fields=["UTILITY_ID","NAME","STATE","ReportFlag"],
        aliases=["Utility ID","Name","State","Reported?"],
    ),
    name="Utilities",
).add_to(m)

folium.LayerControl().add_to(m)
st_folium(m, width=None, height=640)
