# src/data_generator.py
import numpy as np
import pandas as pd
from datetime import datetime

def generate_vitals(prev_row=None):
    """Generate next vitals row based on previous row (or initial)."""
    if prev_row is None:
        prev_row = {
            "timestamp": datetime.now(),
            "HR": 75,
            "SpO2": 98,
            "BP_sys": 120,
            "BP_dia": 80,
            "Temp": 36.7
        }

    # Add small random changes to simulate natural fluctuations
    next_row = {
        "timestamp": datetime.now(),
        "HR": max(40, min(180, int(prev_row["HR"] + np.random.randint(-3, 4)))),
        "SpO2": max(85, min(100, int(prev_row["SpO2"] + np.random.randint(-2, 3)))),
        "BP_sys": max(90, min(180, int(prev_row["BP_sys"] + np.random.randint(-2, 3)))),
        "BP_dia": max(60, min(120, int(prev_row["BP_dia"] + np.random.randint(-2, 3)))),
        "Temp": round(max(35, min(40, prev_row["Temp"] + np.random.uniform(-0.1, 0.1))), 1)
    }

    # Occasionally inject anomalies
    if np.random.rand() < 0.02:
        next_row["HR"] += np.random.randint(20, 40)  # tachycardia spike
    if np.random.rand() < 0.01:
        next_row["SpO2"] -= np.random.randint(5, 10)  # hypoxia

    return next_row
