# inside src/streamlit_app.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_generator import stream_simulation, simulate_multiple_patients
import streamlit as st
import pandas as pd

# One-shot:
df = simulate_multiple_patients(num_patients=1, num_points=300, sampling_interval_seconds=1, seed=123)
st.line_chart(df.set_index("timestamp")[["heart_rate", "spo2", "temperature"]])

# Streaming:
placeholder = st.empty()
rows = []
for row in stream_simulation(num_points=120, sampling_interval_seconds=1, seed=123):
    rows.append(row)
    df_live = pd.DataFrame(rows)
    placeholder.line_chart(df_live.set_index("timestamp")[["heart_rate"]])
    # sleep handled by Streamlit rerun rate or use time.sleep in a non-blocking way in demo
