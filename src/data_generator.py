"""
src/data_generator.py

Generates simulated hospital-grade wearable telemetry:
- Heart Rate (bpm)
- SpO2 (%)
- Temperature (°C)
- Activity level (0..1)

Functions:
- simulate_single_patient(...) -> pd.DataFrame
- simulate_multiple_patients(...) -> pd.DataFrame
- stream_simulation(...) -> generator yielding rows (for real-time dashboards)
- save_simulation_csv(...) -> writes CSV file

Anomalies are injected (spikes/drops/duration) and flagged with `anomaly_flag` and `anomaly_type`.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional

# -------------------------
# Helper / default params
# -------------------------
DEFAULT_HR_MEAN = 75           # bpm
DEFAULT_SPO2_MEAN = 97.0       # %
DEFAULT_TEMP_MEAN = 36.6       # °C
DEFAULT_ACTIVITY_BASE = 0.2     # 0..1 baseline movement

# -------------------------
# Anomaly utilities
# -------------------------
def _inject_event(signal: np.ndarray, index: int, duration: int, magnitude: float, mode: str = "add"):
    """Apply an additive or multiplicative event to a numeric numpy array in place."""
    end = min(len(signal), index + duration)
    if mode == "add":
        signal[index:end] += magnitude
    elif mode == "mul":
        signal[index:end] *= magnitude
    else:
        raise ValueError("mode must be 'add' or 'mul'")

# -------------------------
# Core simulation functions
# -------------------------
def simulate_single_patient(
    num_points: int = 300,
    start_time: Optional[datetime] = None,
    sampling_interval_seconds: int = 1,
    hr_mean: float = DEFAULT_HR_MEAN,
    spo2_mean: float = DEFAULT_SPO2_MEAN,
    temp_mean: float = DEFAULT_TEMP_MEAN,
    activity_base: float = DEFAULT_ACTIVITY_BASE,
    anomaly_rate: float = 0.05,
    seed: Optional[int] = None,
    patient_id: int = 1
) -> pd.DataFrame:
    """
    Simulate vitals for a single patient.

    Returns a DataFrame with columns:
    timestamp, patient_id, heart_rate, spo2, temperature, activity_level, anomaly_flag, anomaly_type

    Parameters:
      - num_points: number of samples to generate (e.g., seconds)
      - sampling_interval_seconds: spacing between timestamps
      - anomaly_rate: fraction of points to inject anomalies (0-1)
      - seed: RNG seed for reproducibility
    """
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    if start_time is None:
        start_time = datetime.now()

    # timestamps
    timestamps = [start_time + timedelta(seconds=i * sampling_interval_seconds) for i in range(num_points)]

    # Base signals
    t = np.linspace(0, 2 * np.pi, num_points)
    # Heart rate: mean + small sinusoidal variation + gaussian noise
    heart_rate = hr_mean + 3.0 * np.sin(0.5 * t * 3) + np.random.normal(0, 1.5, num_points)

    # SpO2: near-constant with small noise
    spo2 = spo2_mean + np.random.normal(0, 0.4, num_points)

    # Temperature: slow drift + noise
    temperature = temp_mean + 0.05 * np.sin(0.1 * t) + np.random.normal(0, 0.05, num_points)

    # Activity: baseline + bursts
    activity = activity_base + 0.3 * np.abs(np.sin(1.5 * t)) + np.random.normal(0, 0.05, num_points)
    activity = np.clip(activity, 0.0, 1.0)

    # Initialize anomaly meta arrays
    anomaly_flag = np.zeros(num_points, dtype=int)
    anomaly_type = np.array([""] * num_points, dtype=object)

    # Decide number of anomaly events to inject
    expected_events = max(1, int(anomaly_rate * num_points))
    possible_indices = list(range(5, num_points - 5))  # avoid edges
    event_indices = random.sample(possible_indices, k=expected_events)

    for idx in event_indices:
        # Pick anomaly type probabilistically
        choice = random.choices(
            ["tachy", "brady", "hypoxia", "fever", "motion_spike", "sensor_dropout"],
            weights=[0.25, 0.15, 0.2, 0.1, 0.2, 0.1],
            k=1
        )[0]

        if choice == "tachy":
            # sudden HR spike +20..40 bpm for 5-15 sec
            dur = random.randint(5, 15)
            _inject_event(heart_rate, idx, dur, magnitude=random.uniform(20, 40), mode="add")
            anomaly_type[idx:idx+dur] = "tachy"
        elif choice == "brady":
            dur = random.randint(5, 12)
            _inject_event(heart_rate, idx, dur, magnitude=-random.uniform(15, 30), mode="add")
            anomaly_type[idx:idx+dur] = "brady"
        elif choice == "hypoxia":
            dur = random.randint(5, 20)
            _inject_event(spo2, idx, dur, magnitude=-random.uniform(4, 8), mode="add")
            anomaly_type[idx:idx+dur] = "hypoxia"
        elif choice == "fever":
            dur = random.randint(30, 120)
            _inject_event(temperature, idx, dur, magnitude=random.uniform(0.7, 1.5), mode="add")
            anomaly_type[idx:idx+dur] = "fever"
        elif choice == "motion_spike":
            # activity jump then drop (e.g., fall or sudden motion)
            dur = random.randint(3, 10)
            _inject_event(activity, idx, dur, magnitude=random.uniform(0.6, 1.5), mode="add")
            anomaly_type[idx:idx+dur] = "motion_spike"
        elif choice == "sensor_dropout":
            dur = random.randint(3, 10)
            spo2[idx:idx+dur] = np.nan  # simulate missing readings
            anomaly_type[idx:idx+dur] = "dropout"

        anomaly_flag[idx:idx+dur] = 1

    # Ensure physiologic bounds
    heart_rate = np.clip(heart_rate, 30, 220)
    spo2 = np.clip(spo2, 60, 100)
    temperature = np.clip(temperature, 34.0, 42.0)
    activity = np.clip(activity, 0.0, 3.0)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "patient_id": int(patient_id),
        "heart_rate": np.round(heart_rate, 1),
        "spo2": np.round(spo2, 1),
        "temperature": np.round(temperature, 2),
        "activity_level": np.round(activity, 2),
        "anomaly_flag": anomaly_flag,
        "anomaly_type": anomaly_type
    })

    return df


def simulate_multiple_patients(
    num_patients: int = 1,
    **kwargs
) -> pd.DataFrame:
    """
    Simulate multiple patients and concatenate into a single DataFrame.
    kwargs are forwarded to simulate_single_patient (like num_points, seed).
    """
    dfs = []
    base_seed = kwargs.pop("seed", None)
    for pid in range(1, num_patients + 1):
        seed = (base_seed + pid) if base_seed is not None else None
        df = simulate_single_patient(patient_id=pid, seed=seed, **kwargs)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def stream_simulation(
    num_points: int = 300,
    sampling_interval_seconds: int = 1,
    patient_id: int = 1,
    **kwargs
):
    """
    Generator that yields one row (as dict) at a time for live dashboards.
    Use in Streamlit as: for row in stream_simulation(...): append to dataframe and plot.
    """
    df = simulate_single_patient(num_points=num_points, sampling_interval_seconds=sampling_interval_seconds, patient_id=patient_id, **kwargs)
    for _, row in df.iterrows():
        yield row.to_dict()


def save_simulation_csv(df: pd.DataFrame, path: str = "data/simulated_patient_data.csv"):
    """Save DataFrame to CSV (creates directories if needed)."""
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return path


# -------------------------
# Quick test / demo runner
# -------------------------
if __name__ == "__main__":
    # Quick smoke test: generate 120 seconds for 2 patients and save CSV
    demo_df = simulate_multiple_patients(num_patients=2, num_points=120, sampling_interval_seconds=1, anomaly_rate=0.06, seed=42)
    outpath = save_simulation_csv(demo_df, path="data/demo_simulated_vitals.csv")
    print(f"Saved demo CSV to {outpath}")
    print(demo_df.head())
