# src/anomaly_detector.py

def detect_anomalies(row):
    anomalies = []
    if row["HR"] < 50 or row["HR"] > 120:
        anomalies.append("HR")
    if row["SpO2"] < 90:
        anomalies.append("SpO2")
    if row["BP_sys"] > 160 or row["BP_dia"] > 100:
        anomalies.append("BP")
    if row["Temp"] > 38:
        anomalies.append("Temp")
    return anomalies
