# inside src/streamlit_app.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# src/streamlit_app.py
import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go

from src.data_generator import generate_vitals
from src.anomaly_detector import detect_anomalies

st.set_page_config(page_title="Patient Monitor Simulator", layout="wide")
st.title("🏥 Single-Patient Real-Time Monitor Simulator")

# Sidebar controls
sim_speed = st.sidebar.slider("Simulation speed (sec per update)", 0.5, 3.0, 1.0)
max_points = st.sidebar.slider("Number of points to display", 10, 100, 30)

# Placeholder for metrics
metric_hr = st.empty()
metric_spo2 = st.empty()
metric_bp = st.empty()
metric_temp = st.empty()
metric_alerts = st.empty()

# Placeholder for plot
plot_placeholder = st.empty()

# Initialize DataFrame
data = pd.DataFrame(columns=["timestamp","HR","SpO2","BP_sys","BP_dia","Temp","anomalies"])
prev_row = None

while True:
    # Generate new vitals
    new_row = generate_vitals(prev_row)
    anomalies = detect_anomalies(new_row)
    new_row["anomalies"] = ", ".join(anomalies) if anomalies else ""
    prev_row = new_row
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    data = data.tail(max_points)  # Keep only last N points

    # Update metrics
    metric_hr.metric("Heart Rate (bpm)", new_row["HR"])
    metric_spo2.metric("SpO₂ (%)", new_row["SpO2"])
    metric_bp.metric("BP (sys/dia mmHg)", f"{new_row['BP_sys']}/{new_row['BP_dia']}")
    metric_temp.metric("Temperature (°C)", new_row["Temp"])
    if anomalies:
        metric_alerts.warning(f"Anomalies detected: {', '.join(anomalies)}")
    else:
        metric_alerts.success("Vitals Normal")

    # Plot vitals
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['HR'], mode='lines+markers', name='HR'))
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['SpO2'], mode='lines+markers', name='SpO₂'))
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['BP_sys'], mode='lines', name='BP_sys'))
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['BP_dia'], mode='lines', name='BP_dia'))
    fig.add_trace(go.Scatter(x=data['timestamp'], y=data['Temp'], mode='lines', name='Temp'))

    # Highlight anomalies
    for col in ["HR","SpO2","BP_sys","BP_dia","Temp"]:
        anomaly_points = data[data["anomalies"].str.contains(col)]
        if not anomaly_points.empty:
            fig.add_trace(go.Scatter(
                x=anomaly_points['timestamp'],
                y=anomaly_points[col],
                mode='markers',
                marker=dict(color='red', size=10, symbol='x'),
                name=f"{col} anomaly"
            ))

    fig.update_layout(title="Patient Vitals Over Time", xaxis_title="Time", yaxis_title="Value",
                      legend_title="Vitals")
    plot_placeholder.plotly_chart(fig, use_container_width=True)

    time.sleep(sim_speed)

