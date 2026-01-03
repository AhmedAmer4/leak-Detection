import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(page_title="تسربات الدمام", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("water_leakage_data.csv")
    with open("dammam.json", "r", encoding="utf-8") as f:
        geo_data = json.load(f)
    return df, geo_data

try:
    df, geo_data = load_data()
    st.title("🚰 لوحة تحكم تسربات المياه - الدمام")
    
    # KPIs
    st.metric("إجمالي البلاغات", len(df))

    # الرسم البياني
    fig = px.pie(df, names='house_connection_TYPE', title="أنواع التوصيلات")
    st.plotly_chart(fig, use_container_width=True)

    # الخريطة
    st.subheader("مواقع التسربات")
    m = folium.Map(location=[26.4207, 50.0888], zoom_start=11)
    folium.GeoJson(geo_data, name="الأحياء").add_to(m)
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3, color='red', fill=True
        ).add_to(m)
    st_folium(m, width=1200, height=500)

except Exception as e:
    st.error(f"⚠️ تأكد من رفع الملفات بأسماء: water_leakage_data.csv و dammam.json")
    st.write(e)
