# 🎗️ BreastCare Kenya
### Clinical Decision Support Platform for Breast Cancer Screening

> *"In Kenya, 54% of health practitioners have poor breast cancer knowledge scores.
> 78% of patients present at Stage III or IV.
> BreastCare Kenya closes the gap between knowing and doing — at the point of care."*

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?style=flat-square&logo=streamlit)
![Offline](https://img.shields.io/badge/Works-Offline-2e7d32?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

## 🌍 The Problem

Our research with **250 Kenyan health practitioners** revealed a striking KAP (Knowledge, Attitudes & Practices) gap:

| Domain | Mean Score | Category |
|--------|-----------|----------|
| 🧠 Knowledge | 54.7% | Poor |
| 💬 Attitude | 65.2% | Neutral |
| 🏥 Practice | **29.2%** | **Critical** |

Practitioners **know** about breast cancer. They **want** to act. But practice scores are alarmingly low — especially Community Health Workers (12.7%) and Nurses (27%). This is not a knowledge problem. It is a **point-of-care support problem.**

**BreastCare Kenya solves it.**

### Breastcare app snippet

<img width="1203" height="572" alt="image" src="https://github.com/user-attachments/assets/f266ac47-23ba-4169-bdbf-2408f088da62" />

### Breast Care App Live Demo

https://breastcarekenya.streamlit.app/

### Dashbord snippet
<img width="1231" height="558" alt="image" src="https://github.com/user-attachments/assets/b9ae3f38-f167-41f0-8d60-46f73da5f4a6" />

### Breast Care Dashboard Live Demo
https://breastcaredashboard.streamlit.app/

## ✨ What It Does

A fully connected, 6-module clinical decision support platform built in Python & Streamlit. Every module feeds the next — one patient, one journey, zero re-entering data. Works fully offline. Includes a built-in clinical chatbot.

```
🩺 Risk Assessment
      ↓  patient auto-added to tracker · symptoms flow forward
✅ Screening Checklist
      ↓  symptoms auto-fill
🔀 Referral Intelligence
      ↓  one-click save to tracker
🔔 Follow-Up Tracker  ←→  🩺 Risk Re-Assessment
      ↓  live data · journey timeline per patient
📊 Analytics Dashboard  ←  updates automatically
      +
💬 Clinical Chatbot  ←  available from any module
```

## 🔗 The 6 Live Connections

| # | From | To | What flows automatically |
|---|------|----|--------------------------|
| 1 | Risk Assessment | Screening Checklist | Patient name, age, county, risk level · symptoms pre-loaded · red flags pre-highlighted in Step 5 |
| 2 | Screening Checklist | Referral Intelligence | All ticked symptoms auto-filled · zero re-entry |
| 3 | Referral Intelligence | Follow-Up Tracker | Due date, risk level, referral type — one click saves everything |
| 4 | Follow-Up Tracker | Risk Re-Assessment | Full patient context pre-filled · practitioner only updates what changed |
| 5 | All modules | Analytics Dashboard | Every assessment & referral reflected in real time — live during demo |
| 6 | Follow-Up Tracker | Patient Journey Timeline | Full visual history per patient: Assessment → Checklist → Referral → Follow-up |


## 🖥️ Modules

### 🩺 1. Quick Risk Assessment
- Input: age, symptoms, family history, reproductive history, risk factors
- Output: weighted risk score (0–100), risk level (LOW / MODERATE / HIGH), referral decision, red flags, follow-up date
- **Patient automatically added to Follow-Up Tracker on submission** — no manual entry needed
- Symptoms flow directly to Screening Checklist
- Pre-fill mode for follow-up re-assessments (full continuity of care)

### ✅ 2. Guided Screening Checklist
- 5-step clinical workflow: History → Visual Inspection → Palpation → Lymph Nodes → Red Flag Detection
- **Symptoms pre-loaded from Risk Assessment** — practitioner just confirms, doesn't re-enter
- Red flags from assessment pre-highlighted in Step 5
- Red flags auto-detected and counted at end of checklist
- Clinical tips at every step
- One-click navigation to Referral Intelligence on completion

### 🔀 3. Referral Intelligence Engine
- Evidence-weighted referral decision: Urgent / Imaging / Routine / Education
- **All symptoms pre-filled from Screening Checklist**
- Patient context (age group, family history, menopausal status) carried from Risk Assessment
- Score breakdown chart showing evidence weighting behind recommendation
- Practice gap alert when urgent criteria are met
- One-click save to Follow-Up Tracker

### 🔔 4. Smart Follow-Up Tracker
- **All patients from Risk Assessment appear here automatically** — no duplication
- Referral decisions from Referral Intelligence update patient records in one click
- Auto-detects and flags overdue follow-ups daily
- **Patient Journey Timeline** — click any patient to see their full visual history
- Actions per patient: Mark Done · Reschedule +2 weeks · Flag Urgent · Start Re-Assessment
- Re-Assessment button pre-fills Risk Assessment with the patient's existing details
- Manual add for patients entered outside the app flow

### 📊 5. Analytics Dashboard
- **Pulls live from session data** — every assessment and referral appears in real time
- Live banner shows new screenings added in the current session
- Screenings over time · by county · by facility · by profession
- Referral breakdown · follow-up compliance by county
- Overdue patient alert table
- CSV export of all screening data

### 💬 6. Clinical Chatbot
- Built-in assistant available from any module
- Answers clinical questions on breast cancer screening, risk factors, referral pathways, and BSE technique
- Supports practitioners in the field without needing to leave the app
- Works alongside the decision support tools — not a replacement for them

## 📡 Offline Support

BreastCare Kenya is designed for **real-world Kenyan health settings** — including rural facilities with unreliable internet.

- The core risk assessment, screening checklist, and referral decision engine run **entirely without internet**
- All patient data and session state are cached locally
- The sidebar displays a live **Online / Offline badge** so practitioners always know their connectivity status
- Follow-up tracking and analytics sync from cached data whether online or offline

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

> A mother of three who almost ignored a lump she found three months ago. Without BreastCare Kenya, she was told "come back if it gets worse." Three months later she returned — Stage III.

**Run the full connected demo in 4 minutes:**

1. Open **🩺 Risk Assessment** → expand *"Hackathon Demo — Follow Grace's Journey"*
2. Click **"Pre-fill Grace's Case"** → hit **Calculate Risk**
3. Watch HIGH RISK flag · red flags listed · follow-up date set
4. **Grace is already in the Follow-Up Tracker** — automatically
5. Click **"Continue to Screening Checklist"** → symptoms pre-loaded, no re-entry
6. Step through to Step 5 → red flags pre-highlighted from assessment
7. Click **"Continue to Referral Intelligence"** → symptoms auto-filled
8. Click **"Generate Referral Decision"** → Urgent Referral with action steps
9. Click **"Save Referral & Create Follow-Up"** → Grace's tracker record updated
10. Open **🔔 Follow-Up Tracker** → expand Grace → see her full **Journey Timeline**
11. Open **📊 Analytics Dashboard** → Grace's screening in live charts, updated automatically

## 📊 Data

The app uses a **synthetic dataset of 250 Kenyan health practitioners** calibrated from published Kenya KAP literature (2013–2024). It covers:

- Profession, sex, age, county, facility setting, education level
- Knowledge scores, attitude scores, practice scores
- Categorised KAP levels following standard public health thresholds

> ⚠️ **Note:** All patient data shown in the demo is entirely synthetic and does not represent real individuals. This app is not a substitute for clinical judgement.

## 🗂️ Project Structure

```
breastcare-kenya/
│
├── breast_cancer_kap_app.py   # Main Streamlit application (all 6 modules)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── data/
    └── kap_dataset.xlsx        # Source KAP dataset (synthetic, n=250)
```

## 🏥 Clinical Basis

Risk scoring is based on established breast cancer risk factors from:
- Kenya National Cancer Screening Guidelines (2018)
- WHO Breast Cancer Early Detection Framework
- Published KAP studies from Kenya (Otieno et al., 2020; Mwangi et al., 2022)
- IARC breast cancer risk factor evidence summaries

Referral decisions follow the **Kenya Ministry of Health referral pathway** for breast conditions at primary care level.

## 🔮 Roadmap

- [x] Fully connected module flow — zero re-entry of data
- [x] Patient auto-added to Follow-Up Tracker on assessment
- [x] Patient Journey Timeline — visual history per patient
- [x] Re-Assessment with pre-filled patient context
- [x] Live analytics from session data
- [x] Offline support
- [x] Built-in clinical chatbot
- [ ] Kenya Health Information System (KHIS) API integration
- [ ] SMS follow-up reminders via Africa's Talking API
- [ ] Multi-user login (per-facility practitioner accounts)
- [ ] IRB-approved pilot — Nairobi / Kisumu County
- [ ] Swahili language support


## 👩🏾‍💻 Built With

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io) | App framework |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [Pandas](https://pandas.pydata.org) | Data handling |
| Python 3 | Core language |

## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first.

If you are a Kenyan health facility, county health department, or NGO interested in piloting BreastCare Kenya — please reach out. We are actively seeking implementation partners.


## ⚠️ Disclaimer

BreastCare Kenya is a **clinical decision support tool**. It is designed to assist trained health practitioners — not replace clinical judgement. All referral and treatment decisions remain the responsibility of the treating practitioner.

<div align="center">

**Built for the KAP gap. Built for Kenya. Built to save lives.**

🎗️


</div>
