# 🎗️ BreastCare Kenya

### Clinical Decision Support Platform for Breast Cancer Screening

In Kenya, 54% of health practitioners have poor breast cancer knowledge scores. 
78% of patients present at Stage III or IV. 
BreastCare Kenya closes the gap between knowing and doing, at the point of care.

## 🌍 The Problem

Our research with **250 Kenyan health practitioners** revealed a striking KAP (Knowledge, Attitudes & Practices) gap:

| Domain | Mean Score | Category |
|--------|-----------|----------|
| 🧠 Knowledge | 54.7% | Poor |
| 💬 Attitude | 65.2% | Neutral |
| 🏥 Practice | **29.2%** | **Critical** |

Practitioners **know** about breast cancer. 
They **want** to act. 
But practice scores are alarmingly low, especially Community Health Workers (12.7%) and Nurses (27%). 
This is not a knowledge problem. It is a **point-of-care support problem.**

**BreastCare Kenya solves it.**

## ✨ What It Does

A fully connected, 5-module clinical decision support platform built in Python & Streamlit. 
Every module feeds the next, one patient, one journey, zero re-entering data.

### Breastcare app snippet

<img width="1203" height="572" alt="image" src="https://github.com/user-attachments/assets/f266ac47-23ba-4169-bdbf-2408f088da62" />

### Breast Care App Live Demo

https://breastcarekenya.streamlit.app/

### Dashbord snippet
<img width="1231" height="558" alt="image" src="https://github.com/user-attachments/assets/b9ae3f38-f167-41f0-8d60-46f73da5f4a6" />

### Breast Care Dashboard Live Demo
https://breastcaredashboard.streamlit.app/

```
🩺 Risk Assessment
      ↓  (patient context + symptoms flow forward)
✅ Screening Checklist
      ↓  (symptoms auto-fill)
🔀 Referral Intelligence
      ↓  (one-click save)
🔔 Follow-Up Tracker  ←→  🩺 Risk Re-Assessment
      ↓  (live data)
📊 Analytics Dashboard
```

## 🔗 The 6 Live Connections

| # | From | To | What flows |
|---|------|----|------------|
| 1 | Risk Assessment | Screening Checklist | Patient name, age, county, risk level, red flags pre-highlighted |
| 2 | Screening Checklist | Referral Intelligence | All ticked symptoms auto-filled |
| 3 | Referral Intelligence | Follow-Up Tracker | Due date, risk level, referral type — zero manual entry |
| 4 | Follow-Up Tracker | Risk Re-Assessment | Full patient context pre-filled for continuity of care |
| 5 | All modules | Analytics Dashboard | Every assessment & referral reflected in real time |
| 6 | Follow-Up Tracker | Patient Journey Timeline | Full visual history: Assessment → Checklist → Referral → Follow-up |

## 🖥️ Modules

### 🩺 1. Quick Risk Assessment
- Input: age, symptoms, family history, reproductive history, risk factors
- Output: weighted risk score (0–100), risk level (LOW / MODERATE / HIGH), referral decision, red flags, follow-up date
- Saves patient to tracker automatically
- Pre-fill mode for re-assessments (continuity of care)

### ✅ 2. Guided Screening Checklist
- 5-step clinical workflow: History → Visual Inspection → Palpation → Lymph Nodes → Red Flag Detection
- Symptoms from Risk Assessment pre-loaded into Step 5
- Red flags auto-detected and counted
- Clinical tips at every step

### 🔀 3. Referral Intelligence Engine
- Evidence-weighted referral decision: Urgent / Imaging / Routine / Education
- All symptoms pre-filled from Screening Checklist
- Patient context (age group, family history, menopausal status) carried from Risk Assessment
- Score breakdown chart showing evidence weighting
- Practice gap alert when urgent criteria met

### 🔔 4. Smart Follow-Up Tracker
- All patients from Risk Assessment and Referral Intelligence appear automatically
- Auto-detects overdue follow-ups daily
- Patient Journey Timeline — full visual history per patient
- Actions: Mark Done, Reschedule +2 weeks, Flag Urgent, Start Re-Assessment
- Manual add for patients entered outside the app flow

### 📊 5. Analytics Dashboard
- Pulls live from session — every assessment and referral appears in real time
- Screenings over time, by county, by facility, by profession
- Referral breakdown, follow-up compliance by county
- Overdue patient alert table
- CSV export

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/kerubobosire254/breastcare-kenya.git
cd breastcare-kenya

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run breast_cancer_kap_app.py
```

The app opens at `http://localhost:8501`

### Dependencies

```
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
```

Or install directly:
```bash
pip install streamlit plotly pandas
```

## 🎬 Demo: Grace's Journey

The app ships with a built-in demo story — **Grace Wanjiku, 42, Nairobi.**

1. Open the app → **🩺 Risk Assessment**
2. Expand *"Hackathon Demo — Follow Grace's Journey"*
3. Click **"Pre-fill Grace's Case"**
4. Hit **Calculate Risk** → watch HIGH RISK flag in under 3 seconds
5. Click **"Continue to Screening Checklist"** — symptoms pre-loaded
6. Navigate to Step 5 → red flags pre-highlighted
7. Click **"Continue to Referral Intelligence"** — symptoms auto-filled
8. Click **"Generate Referral Decision"** → Urgent Referral
9. Click **"Save Referral & Create Follow-Up"** → Grace lands in tracker
10. Open **🔔 Follow-Up Tracker** → expand Grace's card → see her full Journey Timeline
11. Open **📊 Analytics Dashboard** → Grace's screening appears in live charts

**Full clinical loop. 4 minutes. No re-entering data.**

## 📊 Data

The app uses a **synthetic dataset of 250 Kenyan health practitioners** calibrated from published Kenya KAP literature (2013–2024). 
It covers:

- Profession, sex, age, county, facility setting, education level
- Knowledge scores, attitude scores, practice scores
- Categorised KAP levels following standard public health thresholds

> ⚠️ **Note:** All patient data shown in the demo is entirely synthetic and does not represent real individuals.
> This app is not a substitute for clinical judgement.

## 🗂️ Project Structure

```
breastcare-kenya/
│
├── breast_cancer_kap_app.py   # Main Streamlit application (all 5 modules)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── data/
    └── kap_dataset.xlsx        # Source KAP dataset (synthetic, n=250)
```

---

## 🏥 Clinical Basis

Risk scoring is based on established breast cancer risk factors from:
- Kenya National Cancer Screening Guidelines (2018)
- WHO Breast Cancer Early Detection Framework
- Published KAP studies from Kenya (Otieno et al., 2020; Mwangi et al., 2022)
- IARC breast cancer risk factor evidence summaries

Referral decisions follow the **Kenya Ministry of Health referral pathway** for breast conditions at primary care level.

## 🔮 Roadmap

- [ ] Mobile-first PWA (installable on Android, works offline)
- [ ] Kenya Health Information System (KHIS) API integration
- [ ] SMS follow-up reminders via Africa's Talking API
- [ ] Multi-user login (per-facility practitioner accounts)
- [ ] IRB-approved pilot at Level 4 facility — Nairobi / Kisumu County
- [ ] Swahili language support

## 👩🏾‍💻 Built With

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | App framework |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [Pandas](https://pandas.pydata.org) | Data handling |
| Python 3 | Core language |

## 📄 License

MIT License — free to use, adapt, and build on.

## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first.

If you are a Kenyan health facility, county health department, or NGO interested in piloting BreastCare Kenya please reach out. 
We are actively seeking implementation partners.


## ⚠️ Disclaimer

BreastCare Kenya is a **clinical decision support tool**. 
It is designed to assist trained health practitioners not replace clinical judgement. 
All referral and treatment decisions remain the responsibility of the treating practitioner.

---

<div align="center">

**Built for the KAP gap. Built for Kenya. Built to save lives.**

🎗️

</div>
