# src/streamlit_app.py
import sys
import os
import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # Try absolute import (works on Streamlit Cloud)
    from src.data_generator import generate_vitals
    from src.anomaly_detector import detect_anomalies, get_hr_diagnosis, get_spo2_diagnosis, get_bp_diagnosis, get_temp_diagnosis
except ImportError:
    # Fall back to relative import (works locally)
    from data_generator import generate_vitals
    from anomaly_detector import detect_anomalies, get_hr_diagnosis, get_spo2_diagnosis, get_bp_diagnosis, get_temp_diagnosis

st.set_page_config(page_title="Patient Monitor Simulator", layout="wide")
st.title("🏥 Single-Patient Real-Time Monitor Simulator")

sim_speed = st.sidebar.slider("Simulation speed (sec per update)", 0.5, 3.0, 1.0)
max_points = st.sidebar.slider("Number of points to display", 10, 100, 30)

# Initialize DataFrame
data = pd.DataFrame(columns=["timestamp","HR","SpO2","BP_sys","BP_dia","Temp","anomalies"])
prev_row = None

# Create placeholders for each vital sign (graph on left, metric on right)
# Heart Rate row
hr_graph_col, hr_metric_col = st.columns([3, 1])
plot_hr = hr_graph_col.empty()
metric_hr = hr_metric_col.empty()

# SpO2 row
spo2_graph_col, spo2_metric_col = st.columns([3, 1])
plot_spo2 = spo2_graph_col.empty()
metric_spo2 = spo2_metric_col.empty()

# Blood Pressure row
bp_graph_col, bp_metric_col = st.columns([3, 1])
plot_bp = bp_graph_col.empty()
metric_bp = bp_metric_col.empty()

# Temperature row
temp_graph_col, temp_metric_col = st.columns([3, 1])
plot_temp = temp_graph_col.empty()
metric_temp = temp_metric_col.empty()

while True:
    # Generate new vitals
    new_row = generate_vitals(prev_row)
    anomalies = detect_anomalies(new_row)
    new_row["anomalies"] = ", ".join(anomalies) if anomalies else ""
    prev_row = new_row
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    data = data.tail(max_points)

    # Update metrics
    hr_condition, hr_status = get_hr_diagnosis(new_row["HR"])
    spo2_condition, spo2_status = get_spo2_diagnosis(new_row["SpO2"])
    bp_condition, bp_status = get_bp_diagnosis(new_row["BP_sys"], new_row["BP_dia"])
    temp_condition, temp_status = get_temp_diagnosis(new_row["Temp"])
    
    # Status emoji mapping
    status_emoji = {
        "Good": "✅",
        "Caution": "⚡",
        "Concern": "⚠️",
        "Critical": "🚨"
    }
    
    # Update metrics using containers
    metric_hr.markdown(f"""
    <div style='text-align: left;'>
        <h3 style='margin-bottom: 5px;'>Heart Rate</h3>
        <h1 style='margin: 0;'>{new_row["HR"]} bpm</h1>
        <p style='margin: 5px 0; font-weight: bold;'>{hr_condition}</p>
        <p style='margin: 0;'>{status_emoji.get(hr_status, '')} {hr_status}</p>
    </div>
    """, unsafe_allow_html=True)
    
    metric_spo2.markdown(f"""
    <div style='text-align: left;'>
        <h3 style='margin-bottom: 5px;'>SpO₂</h3>
        <h1 style='margin: 0;'>{new_row["SpO2"]}%</h1>
        <p style='margin: 5px 0; font-weight: bold;'>{spo2_condition}</p>
        <p style='margin: 0;'>{status_emoji.get(spo2_status, '')} {spo2_status}</p>
    </div>
    """, unsafe_allow_html=True)
    
    metric_bp.markdown(f"""
    <div style='text-align: left;'>
        <h3 style='margin-bottom: 5px;'>Blood Pressure</h3>
        <h1 style='margin: 0;'>{new_row['BP_sys']}/{new_row['BP_dia']}</h1>
        <p style='margin: 5px 0; font-weight: bold;'>{bp_condition}</p>
        <p style='margin: 0;'>{status_emoji.get(bp_status, '')} {bp_status}</p>
    </div>
    """, unsafe_allow_html=True)
    
    metric_temp.markdown(f"""
    <div style='text-align: left;'>
        <h3 style='margin-bottom: 5px;'>Temperature</h3>
        <h1 style='margin: 0;'>{new_row["Temp"]}°C</h1>
        <p style='margin: 5px 0; font-weight: bold;'>{temp_condition}</p>
        <p style='margin: 0;'>{status_emoji.get(temp_status, '')} {temp_status}</p>
    </div>
    """, unsafe_allow_html=True)

    # Individual plots
    def plot_vital(y_col, name, plot_placeholder, color):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['timestamp'], 
            y=data[y_col], 
            mode='lines+markers', 
            name=name,
            line=dict(color=color),
            marker=dict(color=color)
        ))
        # Highlight anomalies
        anomaly_points = data[data["anomalies"].str.contains(y_col)]
        if not anomaly_points.empty:
            fig.add_trace(go.Scatter(
                x=anomaly_points['timestamp'],
                y=anomaly_points[y_col],
                mode='markers',
                marker=dict(color='red', size=10, symbol='x'),
                name=f"{name} anomaly"
            ))
        fig.update_layout(title=f"{name} Over Time", xaxis_title="Time", yaxis_title=name, showlegend=False)
        plot_placeholder.plotly_chart(fig, use_container_width=True)

    plot_vital("HR", "Heart Rate", plot_hr, "#00FF00")  # Bright Green
    plot_vital("SpO2", "SpO₂", plot_spo2, "#87CEEB")  # Sky Blue
    plot_vital("BP_sys", "BP Systolic", plot_bp, "#FFD700")  # Yellow
    plot_vital("Temp", "Temperature", plot_temp, "#FFA07A")  # Orange

    time.sleep(sim_speed)
