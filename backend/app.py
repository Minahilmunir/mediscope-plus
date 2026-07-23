from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from collections import Counter
import re

app = Flask(__name__)
CORS(app)

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
#   MEDISCOPE+  ┬╖  MEDICAL AI ANALYSIS ENGINE  v1.0
#   ΓÜá DISCLAIMER: For educational/demo purposes only.
#   Not a substitute for professional medical advice.
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ

patient_records = []

# ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
#   SYMPTOM ΓåÆ CONDITION DATABASE
# ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
SYMPTOM_DB = {
    # Cardiovascular
    "chest pain":        {"conditions": ["Angina", "Heart Attack", "GERD", "Costochondritis"], "urgency": "critical", "system": "Cardiovascular"},
    "chest tightness":   {"conditions": ["Angina", "Asthma", "Anxiety Disorder"],              "urgency": "high",     "system": "Cardiovascular"},
    "palpitations":      {"conditions": ["Arrhythmia", "Anxiety", "Hyperthyroidism"],           "urgency": "medium",   "system": "Cardiovascular"},
    "shortness of breath":{"conditions": ["Asthma", "Heart Failure", "Pneumonia", "Anemia"],   "urgency": "high",     "system": "Respiratory"},
    "rapid heartbeat":   {"conditions": ["Tachycardia", "Anxiety", "Fever", "Anemia"],          "urgency": "high",     "system": "Cardiovascular"},
    "slow heartbeat":    {"conditions": ["Bradycardia", "Hypothyroidism", "Heart Block"],        "urgency": "high",     "system": "Cardiovascular"},

    # Respiratory
    "cough":             {"conditions": ["Common Cold", "Bronchitis", "Asthma", "COVID-19"],    "urgency": "low",      "system": "Respiratory"},
    "dry cough":         {"conditions": ["COVID-19", "Asthma", "GERD", "ACE Inhibitor Side Effect"], "urgency": "medium","system": "Respiratory"},
    "wheezing":          {"conditions": ["Asthma", "COPD", "Bronchitis"],                        "urgency": "medium",   "system": "Respiratory"},
    "sore throat":       {"conditions": ["Pharyngitis", "Tonsillitis", "Strep Throat", "Cold"],  "urgency": "low",      "system": "ENT"},
    "runny nose":        {"conditions": ["Common Cold", "Allergic Rhinitis", "Sinusitis"],        "urgency": "low",      "system": "ENT"},
    "nasal congestion":  {"conditions": ["Sinusitis", "Allergic Rhinitis", "Common Cold"],        "urgency": "low",      "system": "ENT"},

    # Neurological
    "headache":          {"conditions": ["Tension Headache", "Migraine", "Hypertension", "Dehydration"], "urgency": "low","system": "Neurological"},
    "severe headache":   {"conditions": ["Migraine", "Hypertensive Crisis", "Meningitis", "Subarachnoid Hemorrhage"], "urgency": "critical", "system": "Neurological"},
    "dizziness":         {"conditions": ["Vertigo", "Hypotension", "Anemia", "Inner Ear Disorder"], "urgency": "medium","system": "Neurological"},
    "numbness":          {"conditions": ["Peripheral Neuropathy", "Stroke", "Multiple Sclerosis", "Vitamin B12 Deficiency"], "urgency": "high", "system": "Neurological"},
    "seizure":           {"conditions": ["Epilepsy", "Febrile Seizure", "Hypoglycemia"],          "urgency": "critical", "system": "Neurological"},
    "confusion":         {"conditions": ["Delirium", "Stroke", "Hypoglycemia", "Encephalitis"],   "urgency": "critical", "system": "Neurological"},
    "memory loss":       {"conditions": ["Dementia", "Alzheimer's", "Depression", "Hypothyroidism"], "urgency": "medium","system": "Neurological"},
    "tremors":           {"conditions": ["Parkinson's Disease", "Essential Tremor", "Hyperthyroidism"], "urgency": "medium","system": "Neurological"},

    # Gastrointestinal
    "nausea":            {"conditions": ["Gastritis", "Food Poisoning", "Pregnancy", "Migraine"],  "urgency": "low",     "system": "Gastrointestinal"},
    "vomiting":          {"conditions": ["Gastroenteritis", "Food Poisoning", "Appendicitis"],     "urgency": "medium",  "system": "Gastrointestinal"},
    "abdominal pain":    {"conditions": ["Appendicitis", "Gastritis", "IBS", "Kidney Stone"],      "urgency": "medium",  "system": "Gastrointestinal"},
    "severe abdominal pain":{"conditions": ["Appendicitis", "Perforated Ulcer", "Pancreatitis"],   "urgency": "critical","system": "Gastrointestinal"},
    "diarrhea":          {"conditions": ["Gastroenteritis", "IBS", "Food Poisoning", "Crohn's Disease"], "urgency": "low","system": "Gastrointestinal"},
    "constipation":      {"conditions": ["IBS", "Hypothyroidism", "Colorectal Issues", "Dehydration"], "urgency": "low", "system": "Gastrointestinal"},
    "bloating":          {"conditions": ["IBS", "Lactose Intolerance", "GERD", "Celiac Disease"],  "urgency": "low",     "system": "Gastrointestinal"},
    "heartburn":         {"conditions": ["GERD", "Peptic Ulcer", "Hiatal Hernia"],                 "urgency": "low",     "system": "Gastrointestinal"},
    "jaundice":          {"conditions": ["Hepatitis", "Gallstones", "Liver Disease", "Hemolysis"], "urgency": "high",    "system": "Hepatic"},

    # Musculoskeletal
    "joint pain":        {"conditions": ["Arthritis", "Gout", "Lupus", "Lyme Disease"],            "urgency": "low",     "system": "Musculoskeletal"},
    "back pain":         {"conditions": ["Lumbar Strain", "Herniated Disc", "Kidney Infection", "Osteoporosis"], "urgency": "low","system": "Musculoskeletal"},
    "muscle weakness":   {"conditions": ["Myopathy", "Multiple Sclerosis", "ALS", "Hypokalemia"],  "urgency": "medium",  "system": "Musculoskeletal"},
    "swollen joints":    {"conditions": ["Rheumatoid Arthritis", "Gout", "Septic Arthritis"],       "urgency": "medium",  "system": "Musculoskeletal"},

    # Dermatological
    "rash":              {"conditions": ["Allergic Reaction", "Eczema", "Psoriasis", "Viral Infection"], "urgency": "low","system": "Dermatological"},
    "hives":             {"conditions": ["Allergic Reaction", "Urticaria", "Angioedema"],           "urgency": "medium",  "system": "Dermatological"},
    "itching":           {"conditions": ["Eczema", "Psoriasis", "Allergic Reaction", "Liver Disease"], "urgency": "low",  "system": "Dermatological"},
    "pale skin":         {"conditions": ["Anemia", "Shock", "Hypotension", "Hypothyroidism"],       "urgency": "medium",  "system": "Hematological"},

    # General / Systemic
    "fever":             {"conditions": ["Infection", "COVID-19", "Influenza", "UTI"],              "urgency": "medium",  "system": "General"},
    "high fever":        {"conditions": ["Sepsis", "Meningitis", "Severe Infection"],               "urgency": "critical","system": "General"},
    "fatigue":           {"conditions": ["Anemia", "Hypothyroidism", "Depression", "Diabetes", "Sleep Disorder"], "urgency": "low","system": "General"},
    "weight loss":       {"conditions": ["Diabetes", "Cancer", "Hyperthyroidism", "Depression"],    "urgency": "medium",  "system": "General"},
    "weight gain":       {"conditions": ["Hypothyroidism", "Cushing's Syndrome", "PCOS"],           "urgency": "low",     "system": "General"},
    "night sweats":      {"conditions": ["Tuberculosis", "Lymphoma", "Menopause", "Infection"],     "urgency": "medium",  "system": "General"},
    "loss of appetite":  {"conditions": ["Depression", "Cancer", "Hepatitis", "Chronic Illness"],   "urgency": "medium",  "system": "General"},
    "excessive thirst":  {"conditions": ["Diabetes Mellitus", "Diabetes Insipidus", "Hypercalcemia"], "urgency": "medium","system": "Endocrine"},
    "frequent urination":{"conditions": ["Diabetes", "UTI", "Overactive Bladder", "Prostate Issues"], "urgency": "low",  "system": "Urological"},
    "swelling":          {"conditions": ["Heart Failure", "Kidney Disease", "Deep Vein Thrombosis", "Lymphedema"], "urgency": "medium","system": "General"},
    "vision changes":    {"conditions": ["Glaucoma", "Cataracts", "Diabetic Retinopathy", "Hypertension"], "urgency": "high","system": "Ophthalmological"},
    "eye pain":          {"conditions": ["Glaucoma", "Conjunctivitis", "Uveitis"],                  "urgency": "high",    "system": "Ophthalmological"},
}

# ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
#   VITALS ANALYSIS
# ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
def analyze_vitals(vitals):
    issues = []
    recommendations = []

    # Blood Pressure
    bp = vitals.get("blood_pressure", "")
    if bp:
        try:
            sys_val, dia_val = map(int, bp.strip().split("/"))
            if sys_val >= 180 or dia_val >= 120:
                issues.append({"vital": "Blood Pressure", "value": bp, "status": "critical", "note": "Hypertensive Crisis ΓÇö seek emergency care immediately"})
            elif sys_val >= 140 or dia_val >= 90:
                issues.append({"vital": "Blood Pressure", "value": bp, "status": "high", "note": "Stage 2 Hypertension"})
                recommendations.append("Monitor BP every 15 min, reduce sodium intake, consult physician")
            elif sys_val >= 130 or dia_val >= 80:
                issues.append({"vital": "Blood Pressure", "value": bp, "status": "elevated", "note": "Stage 1 Hypertension"})
                recommendations.append("Lifestyle changes: exercise, DASH diet, reduce stress")
            elif sys_val < 90 or dia_val < 60:
                issues.append({"vital": "Blood Pressure", "value": bp, "status": "low", "note": "Hypotension ΓÇö risk of fainting/shock"})
                recommendations.append("Increase fluid intake, rise slowly from sitting position")
            else:
                issues.append({"vital": "Blood Pressure", "value": bp, "status": "normal", "note": "Within normal range"})
        except:
            pass

    # Heart Rate
    hr = vitals.get("heart_rate")
    if hr is not None:
        try:
            hr = int(hr)
            if hr > 150:
                issues.append({"vital": "Heart Rate", "value": f"{hr} bpm", "status": "critical", "note": "Severe Tachycardia ΓÇö emergency evaluation needed"})
            elif hr > 100:
                issues.append({"vital": "Heart Rate", "value": f"{hr} bpm", "status": "high", "note": "Tachycardia"})
                recommendations.append("Avoid caffeine, check for fever or anxiety triggers")
            elif hr < 40:
                issues.append({"vital": "Heart Rate", "value": f"{hr} bpm", "status": "critical", "note": "Severe Bradycardia ΓÇö emergency evaluation needed"})
            elif hr < 60:
                issues.append({"vital": "Heart Rate", "value": f"{hr} bpm", "status": "low", "note": "Bradycardia ΓÇö may be normal for athletes"})
            else:
                issues.append({"vital": "Heart Rate", "value": f"{hr} bpm", "status": "normal", "note": "Normal range (60ΓÇô100 bpm)"})
        except:
            pass

    # Temperature
    temp = vitals.get("temperature")
    if temp is not None:
        try:
            temp = float(temp)
            if temp >= 39.5:
                issues.append({"vital": "Temperature", "value": f"{temp}┬░C", "status": "critical", "note": "High Fever ΓÇö risk of febrile seizure"})
                recommendations.append("Antipyretics, cooling measures, seek medical attention")
            elif temp >= 38.0:
                issues.append({"vital": "Temperature", "value": f"{temp}┬░C", "status": "high", "note": "Fever ΓÇö possible infection"})
                recommendations.append("Rest, hydration, monitor closely, paracetamol if needed")
            elif temp < 35.0:
                issues.append({"vital": "Temperature", "value": f"{temp}┬░C", "status": "low", "note": "Hypothermia ΓÇö seek immediate warmth"})
            else:
                issues.append({"vital": "Temperature", "value": f"{temp}┬░C", "status": "normal", "note": "Normal (36.1ΓÇô37.2┬░C)"})
        except:
            pass

    # Oxygen Saturation
    spo2 = vitals.get("oxygen_saturation")
    if spo2 is not None:
        try:
            spo2 = int(spo2)
            if spo2 < 90:
                issues.append({"vital": "SpOΓéé", "value": f"{spo2}%", "status": "critical", "note": "Severe Hypoxemia ΓÇö emergency oxygen required"})
            elif spo2 < 95:
                issues.append({"vital": "SpOΓéé", "value": f"{spo2}%", "status": "high", "note": "Low Oxygen ΓÇö monitor closely"})
                recommendations.append("Supplemental oxygen, check airway, avoid exertion")
            else:
                issues.append({"vital": "SpOΓéé", "value": f"{spo2}%", "status": "normal", "note": "Normal (ΓëÑ95%)"})
        except:
            pass

    # Blood Sugar
    sugar = vitals.get("blood_sugar")
    if sugar is not None:
        try:
            sugar = int(sugar)
            if sugar > 300:
                issues.append({"vital": "Blood Sugar", "value": f"{sugar} mg/dL", "status": "critical", "note": "Severe Hyperglycemia ΓÇö risk of diabetic ketoacidosis"})
                recommendations.append("Insulin administration, immediate medical attention, IV fluids")
            elif sugar > 180:
                issues.append({"vital": "Blood Sugar", "value": f"{sugar} mg/dL", "status": "high", "note": "Hyperglycemia"})
                recommendations.append("Check insulin dosage, avoid carbohydrates, consult endocrinologist")
            elif sugar < 70:
                issues.append({"vital": "Blood Sugar", "value": f"{sugar} mg/dL", "status": "low", "note": "Hypoglycemia ΓÇö give glucose immediately"})
                recommendations.append("15g fast-acting carbs (juice/glucose tablets), recheck in 15 min")
            else:
                issues.append({"vital": "Blood Sugar", "value": f"{sugar} mg/dL", "status": "normal", "note": "Normal fasting (70ΓÇô180 mg/dL)"})
        except:
            pass

    return issues, list(set(recommendations))


# ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
#   SYMPTOM MATCHING ENGINE
# ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
def match_symptoms(symptom_text):
    symptom_text = symptom_text.lower().strip()
    matched = {}

    for symptom_key, data in SYMPTOM_DB.items():
        if symptom_key in symptom_text:
            matched[symptom_key] = data

    # Also split by comma/semicolon for listed symptoms
    parts = re.split(r"[,;\n]", symptom_text)
    for part in parts:
        part = part.strip()
        for symptom_key, data in SYMPTOM_DB.items():
            if symptom_key in part and symptom_key not in matched:
                matched[symptom_key] = data

    return matched


def get_overall_urgency(matched_symptoms, vital_issues):
    urgency_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    max_urgency = "low"

    for data in matched_symptoms.values():
        u = data.get("urgency", "low")
        if urgency_order.get(u, 0) > urgency_order.get(max_urgency, 0):
            max_urgency = u

    for issue in vital_issues:
        u = issue.get("status", "low")
        if u in urgency_order and urgency_order[u] > urgency_order.get(max_urgency, 0):
            max_urgency = u

    return max_urgency


def get_urgency_action(urgency, age=None):
    actions = {
        "critical": "≡ƒÜ¿ SEEK EMERGENCY CARE IMMEDIATELY ΓÇö Call 115 or go to the nearest ER",
        "high":     "ΓÜá∩╕Å Consult a doctor within 24 hours ΓÇö Do not delay treatment",
        "medium":   "≡ƒôï Schedule a medical appointment within 3ΓÇô5 days",
        "low":      "≡ƒÆè Monitor symptoms ΓÇö Rest, hydration, and OTC remedies may help"
    }
    if age and age >= 65 and urgency in ("medium", "low"):
        return "ΓÜá∩╕Å Due to patient age, consult a doctor within 24 hours even for mild symptoms"
    return actions.get(urgency, actions["low"])


def get_affected_systems(matched):
    return list(set(v["system"] for v in matched.values()))


def get_possible_conditions(matched):
    all_conditions = []
    for data in matched.values():
        all_conditions.extend(data["conditions"])
    freq = Counter(all_conditions)
    return [{"condition": c, "mentions": m} for c, m in freq.most_common(8)]


# ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ
#   ROUTES
# ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇ

@app.route('/')
def home():
    return jsonify({
        "app": "MediScope+",
        "version": "1.0",
        "status": "running",
        "disclaimer": "For educational/demo purposes only. Not a substitute for medical advice.",
        "endpoints": {
            "POST /diagnose":       "Analyze symptoms + vitals",
            "GET  /patients":       "All patient records",
            "GET  /patient/<id>":   "Single patient record",
            "DELETE /patients":     "Clear all records",
            "GET  /stats":          "Session statistics",
            "GET  /symptoms-list":  "All supported symptoms"
        }
    })


@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # ΓöÇΓöÇ Patient Info ΓöÇΓöÇ
    patient_name = data.get("patient_name", "Anonymous").strip()
    age          = data.get("age")
    gender       = data.get("gender", "unknown")
    symptoms_raw = data.get("symptoms", "").strip()
    vitals       = data.get("vitals", {})
    notes        = data.get("notes", "").strip()

    if not symptoms_raw:
        return jsonify({"error": "Symptoms are required"}), 400

    try:
        age = int(age) if age else None
    except:
        age = None

    # ΓöÇΓöÇ Analysis ΓöÇΓöÇ
    matched_symptoms = match_symptoms(symptoms_raw)
    vital_issues, vital_recs = analyze_vitals(vitals)
    overall_urgency  = get_overall_urgency(matched_symptoms, vital_issues)
    possible_conditions = get_possible_conditions(matched_symptoms)
    affected_systems = get_affected_systems(matched_symptoms)
    urgency_action   = get_urgency_action(overall_urgency, age)

    # ΓöÇΓöÇ General recommendations by urgency ΓöÇΓöÇ
    general_recs = {
        "critical": [
            "Call emergency services (115) immediately",
            "Do not eat or drink anything until evaluated",
            "Keep patient calm and still",
            "Note the time symptoms started"
        ],
        "high": [
            "Do not drive yourself to the hospital",
            "Keep a record of all current medications",
            "Avoid self-medicating until diagnosis",
            "Have someone stay with the patient"
        ],
        "medium": [
            "Maintain a symptom diary with times and triggers",
            "Stay hydrated and get adequate rest",
            "Avoid alcohol and tobacco",
            "Bring medical history to the appointment"
        ],
        "low": [
            "Rest and drink plenty of fluids",
            "Over-the-counter medication may relieve symptoms",
            "Monitor for any worsening symptoms",
            "Maintain a healthy diet and sleep schedule"
        ]
    }

    symptom_count = len(matched_symptoms)
    recognition_rate = min(round(symptom_count / max(len(symptoms_raw.split(",")), 1) * 100), 100)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record_id = len(patient_records) + 1

    result = {
        "status": "success",
        "record_id": record_id,
        "timestamp": timestamp,
        "disclaimer": "ΓÜá AI-generated analysis for educational purposes only. Always consult a licensed physician.",
        "patient": {
            "name": patient_name,
            "age": age,
            "gender": gender,
        },
        "analysis": {
            "symptoms_entered": symptoms_raw,
            "symptoms_recognized": list(matched_symptoms.keys()),
            "symptom_count": symptom_count,
            "recognition_rate": recognition_rate,
            "affected_systems": affected_systems,
        },
        "diagnosis": {
            "possible_conditions": possible_conditions,
            "overall_urgency": overall_urgency,
            "urgency_action": urgency_action,
            "general_recommendations": general_recs.get(overall_urgency, general_recs["low"]),
            "vital_recommendations": vital_recs,
        },
        "vitals_analysis": vital_issues,
        "notes": notes,
    }

    # Save record
    patient_records.append({
        "id": record_id,
        "timestamp": timestamp,
        "patient_name": patient_name,
        "age": age,
        "gender": gender,
        "symptoms_recognized": list(matched_symptoms.keys()),
        "possible_conditions": [c["condition"] for c in possible_conditions[:3]],
        "overall_urgency": overall_urgency,
        "vitals": vitals,
    })

    return jsonify(result)


@app.route('/patients', methods=['GET'])
def get_patients():
    return jsonify({
        "status": "success",
        "total": len(patient_records),
        "records": list(reversed(patient_records))
    })


@app.route('/patient/<int:record_id>', methods=['GET'])
def get_patient(record_id):
    record = next((r for r in patient_records if r["id"] == record_id), None)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify({"status": "success", "record": record})


@app.route('/patients', methods=['DELETE'])
def clear_patients():
    patient_records.clear()
    return jsonify({"status": "success", "message": "All records cleared"})


@app.route('/stats', methods=['GET'])
def stats():
    if not patient_records:
        return jsonify({"status": "success", "total": 0, "message": "No records yet"})

    urgency_counts = Counter(r["overall_urgency"] for r in patient_records)
    gender_counts  = Counter(r["gender"] for r in patient_records)
    all_conditions = []
    for r in patient_records:
        all_conditions.extend(r["possible_conditions"])
    top_conditions = Counter(all_conditions).most_common(5)
    ages = [r["age"] for r in patient_records if r["age"]]
    avg_age = round(sum(ages) / len(ages), 1) if ages else None

    return jsonify({
        "status": "success",
        "total_patients": len(patient_records),
        "urgency_distribution": dict(urgency_counts),
        "gender_distribution": dict(gender_counts),
        "top_conditions": [{"condition": c, "count": n} for c, n in top_conditions],
        "average_age": avg_age,
    })


@app.route('/symptoms-list', methods=['GET'])
def symptoms_list():
    by_system = {}
    for symptom, data in SYMPTOM_DB.items():
        sys = data["system"]
        if sys not in by_system:
            by_system[sys] = []
        by_system[sys].append({"symptom": symptom, "urgency": data["urgency"]})
    return jsonify({"status": "success", "total": len(SYMPTOM_DB), "by_system": by_system})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
