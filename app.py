import streamlit as st
import folium, json
from streamlit_folium import st_folium

st.set_page_config(page_title="Utilities Reliability Map", layout="wide")

# --- PASSWORD ---
PASSWORD = st.secrets["APP_PASSWORD"]   # set this in Streamlit Secrets
entered = st.text_input("Enter password:", type="password")
if entered != PASSWORD:
    st.stop()

# --- LOAD GEOJSON ---
with open("utilities_state_level_reliability_flag.geojson", "r") as f:
    geojson_data = json.load(f)

# --- MAKE MAP ---
m = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles="cartodbpositron")

def style_fn(feat):
    flag = feat["properties"].get("ReportFlag", "No")
    return {
        "fillColor": "green" if flag == "Yes" else "red",
        "color": "black",
        "weight": 0.3,
        "fillOpacity": 0.6,
    }

folium.GeoJson(
    geojson_data,
    style_function=style_fn,
    tooltip=folium.GeoJsonTooltip(
        fields=["UTILITY_ID","NAME","STATE","ReportFlag"],
        aliases=["Utility ID","Name","State","Reported?"]
    ),
).add_to(m)

st_folium(m, width=None, height=600)


