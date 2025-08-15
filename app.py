import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import os

# Initialize session state for data storage
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['Date', 'Rainfall_mm', 'Condition', 'Landslide_Risk', 'PM2.5', 'PM10', 'AQI', 'Air_Quality', 'Vegetation_Air_Risk', 'pH', 'pH_Level', 'Vegetation_pH_Risk'])

# File to store data
DATA_FILE = 'dolomiti_atmosphere_data.csv'

# Load existing data if available
if os.path.exists(DATA_FILE):
    st.session_state.data = pd.read_csv(DATA_FILE)

# Title and Intro
st.title("🌄 Dolomiti Park Atmosphere Monitor")
st.markdown("Monitoring rainfall, air quality, and rain analysis to assess landslide risk and vegetation health in the Dolomiti Park.")
today = date.today()
st.write(f"📅 Today's Date: {today}")

# Layout with columns for inputs
col1, col2, col3 = st.columns(3)

# Rainfall Input
with col1:
    st.subheader("🌧️ Rainfall")
    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        max_value=1000.0,
        step=0.1,
        value=0.0,
        help="Enter daily rainfall in millimeters."
    )
    # Rainfall Condition and Landslide Risk
    condition = "Dry" if rainfall < 5 else "Normal" if rainfall < 20 else "Wet"
    landslide_risk = "High" if rainfall > 50 else "Moderate" if rainfall > 20 else "Low"
    landslide_color = "red" if landslide_risk == "High" else "orange" if landslide_risk == "Moderate" else "green"

# Air Quality Input
with col2:
    st.subheader("🌬️ Air Quality")
    pm25 = st.number_input("PM2.5 (µg/m³)", min_value=0.0, step=1.0, value=0.0)
    pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0, step=1.0, value=0.0)
    aqi = st.number_input("AQI", min_value=0, max_value=500, step=1, value=0)
    # Air Quality Rating
    if aqi <= 50:
        air_quality = "Good"
        air_color = "green"
        vegetation_air_risk = "Low"
    elif aqi <= 100:
        air_quality = "Moderate"
        air_color = "yellow"
        vegetation_air_risk = "Low"
    elif aqi <= 150:
        air_quality = "Unhealthy for Sensitive Groups"
        air_color = "orange"
        vegetation_air_risk = "Moderate"
    else:
        air_quality = "Unhealthy"
        air_color = "red"
        vegetation_air_risk = "High"

# Rain Analysis Input
with col3:
    st.subheader("💧 Rain Analysis")
    ph = st.number_input("Rainwater pH", min_value=0.0, max_value=14.0, step=0.1, value=7.0)
    # pH Level and Vegetation Risk
    if ph < 5.6:
        ph_level = "Acidic"
        ph_color = "red"
        vegetation_ph_risk = "High"
    elif ph <= 7.0:
        ph_level = "Neutral"
        ph_color = "blue"
        vegetation_ph_risk = "Low"
    else:
        ph_level = "Alkaline"
        ph_color = "purple"
        vegetation_ph_risk = "Moderate"

# Submit Data
if st.button("Submit Data"):
    # Create new data entry
    new_data = pd.DataFrame({
        'Date': [today],
        'Rainfall_mm': [rainfall],
        'Condition': [condition],
        'Landslide_Risk': [landslide_risk],
        'PM2.5': [pm25],
        'PM10': [pm10],
        'AQI': [aqi],
        'Air_Quality': [air_quality],
        'Vegetation_Air_Risk': [vegetation_air_risk],
        'pH': [ph],
        'pH_Level': [ph_level],
        'Vegetation_pH_Risk': [vegetation_ph_risk]
    })
    # Append to session state
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
    # Save to CSV
    st.session_state.data.to_csv(DATA_FILE, index=False)
    st.success("Data submitted successfully!")

# Dashboard
st.subheader("📊 Dolomiti Environmental Dashboard")

# Alerts for Landslide and Vegetation
if landslide_risk == "High":
    st.error("⚠️ **High Landslide Risk**: Heavy rainfall detected (>50 mm). Monitor slopes and drainage systems.")
if vegetation_air_risk == "High" or vegetation_ph_risk == "High":
    st.warning("🌱 **Vegetation Risk**: Poor air quality (AQI > 150) or acidic rain (pH < 5.6) may harm Dolomiti vegetation.")

# Display Current Metrics
st.markdown(f"**Rainfall**: {rainfall} mm (<span style='color:{'red' if condition == 'Dry' else 'blue' if condition == 'Normal' else 'green'}'>{condition}</span>, Landslide Risk: <span style='color:{landslide_color}'>{landslide_risk}</span>)", unsafe_allow_html=True)
st.markdown(f"**Air Quality**: AQI {aqi} (<span style='color:{air_color}'>{air_quality}</span>, Vegetation Risk: <span style='color:{'red' if vegetation_air_risk == 'High' else 'orange' if vegetation_air_risk == 'Moderate' else 'green'}'>{vegetation_air_risk}</span>)", unsafe_allow_html=True)
st.markdown(f"**Rain pH**: {ph} (<span style='color:{ph_color}'>{ph_level}</span>, Vegetation Risk: <span style='color:{'red' if vegetation_ph_risk == 'High' else 'orange' if vegetation_ph_risk == 'Moderate' else 'green'}'>{vegetation_ph_risk}</span>)", unsafe_allow_html=True)

# Visualizations
if not st.session_state.data.empty:
    # Air Quality Bar Chart
    st.subheader("Air Quality Metrics")
    air_df = pd.DataFrame({
        'Metric': ['PM2.5', 'PM10', 'AQI'],
        'Value': [pm25, pm10, aqi]
    })
    fig_air = px.bar(air_df, x='Metric', y='Value', title="Current Air Quality Metrics")
    st.plotly_chart(fig_air)

    # pH Gauge
    st.subheader("Rainwater pH")
    fig_ph = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ph,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "pH Level"},
        gauge={
            'axis': {'range': [0, 14]},
            'bar': {'color': ph_color},
            'steps': [
                {'range': [0, 5.6], 'color': "orange"},
                {'range': [5.6, 7.0], 'color': "blue"},
                {'range': [7.0, 14], 'color': "purple"}
            ]
        }
    ))
    st.plotly_chart(fig_ph)

    # Historical Rainfall Trend
    st.subheader("Historical Rainfall Trend (Landslide Risk)")
    fig_rain = px.line(st.session_state.data, x='Date', y='Rainfall_mm', title="Rainfall Over Time", markers=True)
    # Highlight high-risk days
    high_risk = st.session_state.data[st.session_state.data['Landslide_Risk'] == 'High']
    if not high_risk.empty:
        fig_rain.add_scatter(x=high_risk['Date'], y=high_risk['Rainfall_mm'], mode='markers', marker=dict(color='red', size=10), name='High Landslide Risk')
    st.plotly_chart(fig_rain)

    # Historical AQI Trend
    st.subheader("Historical Air Quality (Vegetation Risk)")
    fig_aqi = px.line(st.session_state.data, x='Date', y='AQI', title="AQI Over Time", markers=True)
    high_air_risk = st.session_state.data[st.session_state.data['Vegetation_Air_Risk'] == 'High']
    if not high_air_risk.empty:
        fig_aqi.add_scatter(x=high_air_risk['Date'], y=high_air_risk['AQI'], mode='markers', marker=dict(color='red', size=10), name='High Vegetation Risk')
    st.plotly_chart(fig_aqi)

# Display Historical Data
if not st.session_state.data.empty:
    st.subheader("📈 Historical Data")
    st.dataframe(st.session_state.data)
