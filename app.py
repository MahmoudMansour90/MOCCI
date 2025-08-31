import os, json, requests, streamlit as st

DATA_PATH = "utilities_state_level_reliability_flag.geojson"
DATA_URL  = st.secrets.get("DATA_URL")

def load_geojson():
    if os.path.exists(DATA_PATH):
        st.info("Loading local GeoJSON...")
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    if DATA_URL:
        st.info(f"Fetching from DATA_URL...")
        r = requests.get(DATA_URL, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=True, timeout=60)
        st.write(f"HTTP {r.status_code} | Content-Type: {r.headers.get('Content-Type','')}")
        r.raise_for_status()
        ct = r.headers.get("Content-Type","").lower()
        text = r.text[:200].strip()  # peek at start
        if "html" in ct or text.startswith("<!DOCTYPE html"):
            st.error("DATA_URL returned HTML (likely a login/download page). Use a direct-download link (Dropbox ?dl=1 or Google Drive uc?export=download&id=...).")
            st.stop()
        try:
            return r.json()
        except Exception:
            return json.loads(r.content.decode("utf-8"))

    st.error("No data found. Add the GeoJSON to the repo or set DATA_URL in Secrets.")
    st.stop()
