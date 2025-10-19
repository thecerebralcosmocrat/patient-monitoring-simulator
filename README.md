# 🏥 Patient Monitoring Simulator

A real-time single-patient vital signs monitoring system with intelligent anomaly detection and clinical diagnostics, built using Python and Streamlit. Inspired by GE HealthCare’s CARESCAPE™ ONE systems.

## ✨ Features

- **Real-Time Vital Signs Simulation**
  - Heart Rate (HR)
  - Oxygen Saturation (SpO₂)
  - Blood Pressure (Systolic/Diastolic)
  - Body Temperature

- **Clinical Diagnostic System**
  - Automatic condition detection (Bradycardia, Tachycardia, Hypoxemia, etc.)
  - Health status indicators with visual feedback
  - Intelligent anomaly detection with red markers on graphs

- **Interactive Dashboard**
  - Color-coded graphs for each vital sign
  - Live updates with configurable simulation speed
  - Adjustable data window (10-100 points)
  - Clean, monitor-like layout

- **Health Status Indicators**
  - ✅ **Good**: Normal/healthy range
  - ⚡ **Caution**: Slightly elevated/borderline values
  - ⚠️ **Concern**: Abnormal readings requiring attention
  - 🚨 **Critical**: Dangerous levels requiring immediate action

## 🚀 Live Demo

View Live Demo on [Patient Monitoring Simulator](https://patient-monitoring-simulator.streamlit.app/)

## 🛠️ Tech Stack

- **Python** 3.13.5
- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[NumPy](https://numpy.org/)** - Numerical computing
- **[Plotly](https://plotly.com/)** - Interactive data visualization
- **[Matplotlib](https://matplotlib.org/)** - Additional plotting capabilities

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thecerebralcosmocrat/patient-monitoring-simulator.git
   cd patient-monitoring-simulator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows (Git Bash)**:
     ```bash
     source venv/Scripts/activate
     ```
   - **Windows (CMD)**:
     ```cmd
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

Run the Streamlit application:

```bash
streamlit run src/streamlit_app.py
```

The app will open in your default web browser at `http://localhost:8501`

### Controls

- **Simulation Speed**: Adjust how frequently vital signs update (0.5-3 seconds)
- **Display Points**: Configure how many data points to show on graphs (10-100)

## 📁 Project Structure

```
patient-monitoring-simulator/
├── src/
│   ├── streamlit_app.py      # Main Streamlit application
│   ├── data_generator.py     # Patient vital signs generation
│   ├── anomaly_detector.py   # Anomaly detection & clinical diagnostics
│   └── __init__.py           # Package initialization
├── data/                      # Data storage directory
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

## 🎨 Visual Design

- **Heart Rate**: Bright green graph
- **SpO₂**: Sky blue graph
- **Blood Pressure**: Yellow graph
- **Temperature**: Orange graph

Each vital sign displays:
- Real-time waveform/trend
- Current reading in large text
- Clinical condition diagnosis
- Health status with emoji indicator

## 🧪 Clinical Diagnoses

### Heart Rate (HR)
- **Bradycardia**: < 50 bpm
- **Tachycardia**: > 120 bpm
- **Elevated HR**: 100-120 bpm
- **Normal Sinus**: 60-100 bpm

### Oxygen Saturation (SpO₂)
- **Hypoxemia**: < 90%
- **Low SpO₂**: 90-94%
- **Normal O₂**: ≥ 95%

### Blood Pressure (BP)
- **Hypertensive Crisis**: > 180/120 mmHg
- **Hypertension**: > 160/100 mmHg
- **Elevated BP**: > 140/90 mmHg
- **Prehypertension**: 120-139/80-89 mmHg
- **Hypotension**: < 90/60 mmHg
- **Normal BP**: 90-120/60-80 mmHg

### Body Temperature
- **High Fever**: > 39.5°C
- **Fever**: > 38°C
- **Low-Grade Fever**: 37.5-38°C
- **Hypothermia**: < 35°C
- **Normal Temp**: 35-37.5°C

## 🫶 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Future Enhancements

- [ ] Multiple patient monitoring
- [ ] Historical data export (CSV/JSON)
- [ ] Customizable vital sign ranges
- [ ] Alert sounds for critical conditions
- [ ] Different patient profiles (pediatric, geriatric, athletic)
- [ ] ECG waveform simulation
- [ ] Data persistence and replay
- [ ] User authentication and patient records

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Ankita Sivaramakrishnan**
- GitHub: [@thecerebralcosmocrat](https://github.com/thecerebralcosmocrat)
- Repository: [patient-monitoring-simulator](https://github.com/thecerebralcosmocrat/patient-monitoring-simulator)

⭐ **Star this repository if you find it helpful!**