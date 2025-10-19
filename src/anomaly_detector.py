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


def get_hr_diagnosis(hr):
    """Diagnose heart rate condition"""
    if hr < 50:
        return "Bradycardia", "Concern"
    elif hr > 120:
        return "Tachycardia", "Concern"
    elif hr > 100:
        return "Elevated HR", "Caution"
    elif hr >= 60 and hr <= 100:
        return "Normal Sinus", "Good"
    else:
        return "Low-Normal", "Caution"


def get_spo2_diagnosis(spo2):
    """Diagnose oxygen saturation"""
    if spo2 < 90:
        return "Hypoxemia", "Critical"
    elif spo2 < 95:
        return "Low SpO2", "Concern"
    else:
        return "Normal O2", "Good"


def get_bp_diagnosis(sys, dia):
    """Diagnose blood pressure"""
    if sys > 180 or dia > 120:
        return "Hypertensive Crisis", "Critical"
    elif sys > 160 or dia > 100:
        return "Hypertension", "Concern"
    elif sys > 140 or dia > 90:
        return "Elevated BP", "Caution"
    elif sys >= 120 and sys < 140 and dia >= 80 and dia < 90:
        return "Prehypertension", "Caution"
    elif sys < 90 or dia < 60:
        return "Hypotension", "Concern"
    else:
        return "Normal BP", "Good"


def get_temp_diagnosis(temp):
    """Diagnose body temperature"""
    if temp > 39.5:
        return "High Fever", "Critical"
    elif temp > 38:
        return "Fever", "Concern"
    elif temp > 37.5:
        return "Low-Grade Fever", "Caution"
    elif temp < 35:
        return "Hypothermia", "Concern"
    else:
        return "Normal Temp", "Good"
