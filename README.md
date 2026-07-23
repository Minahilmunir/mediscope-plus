# ⚕️ MediScope+

> **AI-Powered Medical Analysis System** | Python Flask + React.js  
> Built by **Minahil Munir**

---

> ⚠️ **Disclaimer:** This project is for **educational and demonstration purposes only**.  
> It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.  
> Always consult a licensed physician for any medical concerns.

---

## ✨ Features

### 🩺 AI Diagnosis
- 50+ symptoms mapped across 10+ body systems
- Possible conditions with signal scoring
- Urgency levels: 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low
- Affected body systems identification

### 📊 Vital Signs Monitor

| Vital Sign | Normal Range | Status Levels |
|---|---|---|
| Blood Pressure | 90/60 – 120/80 mmHg | Normal / Elevated / High / Critical |
| Heart Rate | 60 – 100 bpm | Normal / Tachycardia / Bradycardia |
| Temperature | 36.1 – 37.2 °C | Normal / Fever / High Fever |
| SpO₂ | ≥ 95% | Normal / Low / Critical |
| Blood Sugar | 70 – 180 mg/dL | Normal / High / Low / Critical |

### 📋 Patient History
- View all past diagnoses
- Urgency badges per record
- One-click clear all

### 📈 Statistics Dashboard
- Total patients, average age
- Urgency distribution bars
- Top diagnosed conditions

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.8+, Flask, Flask-CORS |
| Frontend | React.js, CSS3, Canvas API |
| Analysis | Custom NLP Symptom Engine |
| UI Style | Glassmorphism, Dark Theme, Neural Canvas |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### 1. Clone the repository
```bash
git clone https://github.com/Minahilmunir/mediscope-plus.git
cd mediscope-plus
```

### 2. Backend Setup
```bash
cd backend
pip install flask flask-cors
python app.py
```
Backend runs on → `http://127.0.0.1:5000`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```
Frontend runs on → `http://localhost:3000`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/diagnose` | Symptom analysis |
| GET | `/patients` | All patient records |
| DELETE | `/patients` | Clear all records |
| GET | `/stats` | Analytics & statistics |

---

## 📁 Project Structure

```
mediscope-plus/
├── backend/
│   └── app.py          # Flask API + Medical Analysis Engine
├── frontend/
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js      # Main App (3-tab UI)
│       ├── App.css     # Complete UI Styles
│       ├── index.js
│       └── index.css
└── README.md
```

---

## 🎨 UI Highlights
- **Dark Theme** — Deep background with green accents
- **Neural Canvas** — Animated particle background
- **3-Tab Layout** — Diagnose / History / Statistics
- **Glassmorphism** — Frosted glass cards

---

## 📜 License
MIT License — feel free to use, modify, and distribute.

---

Built with ❤️ by **Minahil Munir** | MediScope+ © 2026
