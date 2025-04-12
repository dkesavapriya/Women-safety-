
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from utils.safest_route import get_safest_route_from_coords, get_color

st.set_page_config(page_title="Women Safety Analytics", layout="wide")
st.title("👩 Women Safety Analytics - Tamil Nadu")

crime_data = pd.read_csv("data/chennai_crime_data.csv")

st.subheader("📍 Crime Hotspots")
m = folium.Map(location=[13.0827, 80.2707], zoom_start=12)
for _, row in crime_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['crime_type']} on {row['date']}",
        icon=folium.Icon(color='green')
    ).add_to(m)
folium_static(m)

st.subheader("🛣️ Enter Source and Destination Coordinates to Find Safest Route")

col1, col2 = st.columns(2)
with col1:
    source_lat = st.text_input("Source Latitude", "13.0827")
    source_lon = st.text_input("Source Longitude", "80.2707")
with col2:
    dest_lat = st.text_input("Destination Latitude", "13.0600")
    dest_lon = st.text_input("Destination Longitude", "80.2400")

if st.button("Find Safest Route"):
    try:
        src_coords = (float(source_lon), float(source_lat))  # lon, lat
        dst_coords = (float(dest_lon), float(dest_lat))
        route_info = get_safest_route_from_coords(src_coords, dst_coords, crime_data)
        route_map = folium.Map(location=route_info["center"], zoom_start=14)
        folium.PolyLine(
            locations=route_info["route"],
            color=get_color(route_info["score"]),
            weight=6,
            tooltip=f"Safety Score: {route_info['score']}"
        ).add_to(route_map)
        folium_static(route_map)
    except Exception as e:
        st.error(f"Error calculating route: {e}")
