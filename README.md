# 🎗️ BreastCare Kenya v2.0
### Clinical Decision Support Platform for Breast Cancer Screening

> *"In Kenya, 54% of health practitioners have poor breast cancer knowledge scores.
> 78% of patients present at Stage III or IV.
> BreastCare Kenya closes the gap between knowing and doing — at the point of care."*

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Offline](https://img.shields.io/badge/Works-Offline-2e7d32?style=flat-square)](.)
[![Zero API Keys](https://img.shields.io/badge/Zero-API%20Keys-e91e8c?style=flat-square)](.)
[![Build54](https://img.shields.io/badge/Build54-Hackathon-7b1fa2?style=flat-square)](.)

### Breastcare app snippet

<img width="1353" height="595" alt="image" src="https://github.com/user-attachments/assets/f7b9cf58-d0cd-47a5-ad63-cb5155b661cc" />


### Breast Care App Live Demo

https://breastcarekenya.streamlit.app/

### Dashbord snippet
<img width="1231" height="558" alt="image" src="https://github.com/user-attachments/assets/b9ae3f38-f167-41f0-8d60-46f73da5f4a6" />

### Breast Care Dashboard Live Demo
https://breastcaredashboard.streamlit.app/

## 🌍 The Problem

Our original research with **250 Kenyan health practitioners** revealed a striking KAP (Knowledge, Attitudes & Practices) gap:

| Domain | Mean Score | Category |
|:---|:---:|:---:|
| 🧠 Knowledge | 54.7% | Poor |
| 💬 Attitude | 65.2% | Neutral |
| 🏥 Practice | **29.2%** | **Critical** |

**Practice scores by profession:**

| Profession | Practice Score |
|:---|:---:|
| Community Health Workers | 12.7% |
| Nurses | 27% |
| Clinical Officers | 31% |
| Doctors | 44% |

Practitioners **know** about breast cancer. They **want** to act. But there is a **36-point gap** between attitude and practice — especially for CHWs and nurses who are the first point of contact in most Kenyan facilities.

This is not a knowledge problem. It is a **point-of-care support problem.**

**BreastCare Kenya solves it.**


## ✨ What It Does — v2.0

A **7-module, fully connected, offline-first** clinical decision support platform built in Python & Streamlit. Every module feeds the next — one patient, one journey, zero re-entering data. No API keys. No internet required for core functions.

```
🏠 Home (NEW)
      ↓  KAP gap dashboard · overdue alerts · quick start
🩺 Risk Assessment
      ↓  patient auto-added to tracker · symptoms flow forward · risk gauge (NEW)
✅ Screening Checklist
      ↓  symptoms auto-fill · red flags pre-highlighted
🔀 Referral Intelligence
      ↓  one-click save to tracker · evidence score chart
🔔 Follow-Up Tracker  ←→  🩺 Risk Re-Assessment
      ↓  live data · journey timeline per patient
📊 Analytics Dashboard  ←  updates automatically · KAP insights tab (NEW)
      +
🤖 CareBot  ←  rule-based clinical NLP · no API needed (NEW)
```

| Topic | Coverage |
|:---|:---|
| 🔴 Risk Factors | Non-modifiable & modifiable risks, BRCA, protective factors |
| ✋ BSE Technique | Step-by-step visual & palpation guide, what to report |
| 🔀 Referral Criteria | Kenya MOH pathway: Urgent / Imaging / Routine / Education |
| 📊 Staging | Stage I–IV, survival rates, Kenya context |
| 🖼️ Imaging | Mammography vs ultrasound, availability & cost in Kenya |
| 💊 Treatment | Surgery, chemo, radiotherapy, hormone therapy, HER2 |
| 📋 KAP Data | Full survey findings, profession breakdown, the 36-point gap |
| 💧 Nipple Discharge | Concerning vs benign features, when to refer |
| 🔍 Lump Assessment | Concerning vs reassuring features, documentation |
| 🔔 Follow-Up Protocols | Post-referral steps, escalation, tracker usage |
| 🛡️ Prevention | Lifestyle, screening schedules, early detection |

CareBot uses regex pattern matching to parse clinical questions and returns structured, evidence-based answers — all offline. 7 pre-built quick-question chips for one-tap access.

### 📊 Risk Score Gauge
Risk Assessment results now display a **Plotly gauge chart** (0–100 scale, colour-coded green/amber/red) alongside the risk badge and referral decision — far more visual impact than a plain number.

### 📄 Clinical Handover Summary
One-click download of a formatted `.txt` handover note per patient — includes date/time, patient details, risk score, red flags, referral instructions, and disclaimer. Ready to hand to the receiving facility.

### 📊 KAP Insights Tab in Analytics
The research that motivated the entire platform now has its own dedicated analytics tab:
- Waterfall chart of the 36-point attitude–practice gap
- Practice score bar chart broken down by profession
- The core insight card explaining why CHWs are the primary target user

### 🎨 Design System Upgrade
- Switched to **Plus Jakarta Sans** — sharper, more professional than the previous Nunito
- **Glassmorphism cards** with backdrop blur replace flat cards
- **Pink/purple gradient brand identity** consistent across hero, sidebar, and UI elements
- **Active patient banner** in the sidebar — always visible as you navigate across modules
- **Builder bio** ("Built by Kerubo Bosire · Build54 · Solo builder · BSc Actuarial Science") always visible to anyone exploring the repo

## 🔗 The 7 Live Connections

| # | From | To | What flows automatically |
|:---:|:---|:---|:---|
| 1 | Risk Assessment | Screening Checklist | Patient name, age, county, risk level · symptoms pre-loaded · red flags pre-highlighted in Step 5 |
| 2 | Screening Checklist | Referral Intelligence | All ticked symptoms auto-filled · zero re-entry |
| 3 | Referral Intelligence | Follow-Up Tracker | Due date, risk level, referral type — one click saves everything |
| 4 | Follow-Up Tracker | Risk Re-Assessment | Full patient context pre-filled · practitioner only updates what changed |
| 5 | All modules | Analytics Dashboard | Every assessment & referral reflected in real time — live during demo |
| 6 | Follow-Up Tracker | Patient Journey Timeline | Full visual history per patient: Assessment → Checklist → Referral → Follow-up |
| 7 | Risk Assessment | Clinical Handover | One-click downloadable summary generated from live session data |


## 🖥️ Modules

### 🏠 0. Home Dashboard *(new in v2.0)*
- Cinematic hero banner with KAP impact statistics
- Interactive KAP gap chart — the 36-point attitude-practice gap visualised
- Live overdue patient alert cards
- Quick-start navigation to key workflows

### 🩺 1. Quick Risk Assessment
- Input: age, symptoms, family history, reproductive history, 8 risk factors
- Output: weighted risk score (0–100) displayed on a **colour-coded gauge**, risk level (LOW / MODERATE / HIGH), referral decision, red flags, follow-up date
- Patient automatically added to Follow-Up Tracker on submission — no manual entry needed
- Symptoms flow directly to Screening Checklist
- **Clinical Handover Summary** downloadable as `.txt`
- Pre-fill mode for follow-up re-assessments (full continuity of care)

### ✅ 2. Guided Screening Checklist
- 5-step clinical workflow: History → Visual Inspection → Palpation → Lymph Nodes → Red Flag Detection
- Symptoms pre-loaded from Risk Assessment — practitioner just confirms, doesn't re-enter
- Red flags from assessment pre-highlighted in Step 5
- Red flags auto-detected and counted at end of checklist
- Clinical tips at every step
- One-click navigation to Referral Intelligence on completion

### 🔀 3. Referral Intelligence Engine
- Evidence-weighted referral decision: Urgent / Imaging / Routine / Education
- All symptoms pre-filled from Screening Checklist
- Patient context (age group, family history, menopausal status) carried from Risk Assessment
- Score breakdown bar chart showing evidence weighting behind recommendation
- Practice gap alert when urgent criteria are met
- One-click save to Follow-Up Tracker

### 🔔 4. Smart Follow-Up Tracker
- All patients from Risk Assessment appear here automatically — no duplication
- Referral decisions from Referral Intelligence update patient records in one click
- Auto-detects and flags overdue follow-ups
- **Patient Journey Timeline** — expand any patient to see their full visual history
- Actions per patient: Mark Done · Reschedule +2 weeks · Flag Urgent · Start Re-Assessment
- Re-Assessment button pre-fills Risk Assessment with the patient's existing details
- Filters: by status, risk level, and county
- Manual add for patients entered outside the app flow

### 📊 5. Analytics Dashboard
- Pulls live from session data — every assessment and referral appears in real time
- **4 tabs:** Trends · By County · By Profession · KAP Insights *(new)*
- Screenings over time (line chart) · risk distribution (donut) · referral breakdown
- County heatmap coloured by high-risk count
- Follow-up compliance rate by county
- Profession breakdown bar chart
- KAP gap waterfall chart + practice-by-profession breakdown
- CSV export of all screening data

### 🤖 6. CareBot — Clinical AI Assistant *(new in v2.0)*
- Rule-based NLP engine with 11-topic clinical knowledge base
- **Zero API keys required — works fully offline**
- 7 quick-question chips for one-tap answers
- Full expandable knowledge base index
- Answers on: BSE, referral criteria, staging, KAP data, imaging, treatment, prevention, lump assessment, nipple discharge, follow-up protocols


## 📡 Offline Support

BreastCare Kenya is designed for **real-world Kenyan health settings** — including rural facilities with unreliable internet.

- The core risk assessment, screening checklist, referral engine, and CareBot run **entirely without internet**
- All patient data and session state are cached locally
- The sidebar displays a live **Online / Offline badge** so practitioners always know their connectivity status
- Analytics and follow-up tracking sync from cached data whether online or offline

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/kerubobosire254/KAPs.git
cd KAPs

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run breastcare.py
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

No additional API keys, environment variables, or external services required.


## 🎬 Demo: Grace's Journey

The app ships with a built-in demo story — **Grace Wanjiku, 42, Nairobi.**

> A mother of three who almost ignored a lump she found three months ago. Without BreastCare Kenya, she was told *"come back if it gets worse."* Three months later she returned — Stage III.

**Run the full connected demo in 5 minutes:**

1. Open **🏠 Home** → click **"Run Grace's Demo"**
2. In **🩺 Risk Assessment** → click **"Pre-fill Grace's Case"** → hit **Calculate Risk**
3. Watch the gauge hit **HIGH RISK** · red flags listed · handover summary generated
4. Grace is already in the Follow-Up Tracker — automatically
5. Click **"Continue to Screening Checklist"** → symptoms pre-loaded, zero re-entry
6. Step through to Step 5 → red flags pre-highlighted from assessment
7. Click **"Continue to Referral Intelligence"** → symptoms auto-filled
8. Click **"Generate Referral Decision"** → Urgent Referral with evidence breakdown chart
9. Click **"Save Referral & Create Follow-Up"** → Grace's tracker record updated
10. Open **🔔 Follow-Up Tracker** → expand Grace → see her full **Journey Timeline**
11. Open **📊 Analytics Dashboard** → Grace's screening in live charts, updated automatically
12. Ask **🤖 CareBot** *"What are the stages?"* — get a full clinical answer, no internet needed

## 📊 Data

The app uses a **synthetic dataset of 250 Kenyan health practitioners** calibrated from published Kenya KAP literature (2013–2024). It covers:

- Profession, sex, age, county, facility setting, education level
- Knowledge scores, attitude scores, practice scores
- Categorised KAP levels following standard public health thresholds

> ⚠️ **Note:** All patient data shown in the demo is entirely synthetic and does not represent real individuals. This app is not a substitute for clinical judgement.

## 🗂️ Project Structure

```
KAPs/
│
├── breastcare.py          # Main Streamlit application — all 7 modules
├── requirements.txt       # Python dependencies (3 packages, no API keys)
├── README.md              # This file
└── data/
    └── kap_dataset.xlsx   # Source KAP dataset (synthetic, n=250)
```


## 🏥 Clinical Basis

Risk scoring is based on established breast cancer risk factors from:

- Kenya National Cancer Screening Guidelines (2018)
- WHO Breast Cancer Early Detection Framework
- Published KAP studies from Kenya (Otieno et al., 2020; Mwangi et al., 2022)
- IARC breast cancer risk factor evidence summaries

Referral decisions follow the **Kenya Ministry of Health referral pathway** for breast conditions at primary care level.

CareBot clinical content is drawn from the same evidence base and the Kenya MOH Breast Cancer Referral Pathway (Level 2–3).


## 👩🏾‍💻 Built With

| Tool | Purpose |
|:---|:---|
| [Streamlit](https://streamlit.io) | App framework |
| [Plotly](https://plotly.com/python/) | Interactive charts, gauges, and KAP visualisations |
| [Pandas](https://pandas.pydata.org) | Data handling and analytics |
| Python 3 | Core language |
| Regex (built-in) | CareBot NLP pattern matching |


## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first.

If you are a Kenyan health facility, county health department, or NGO interested in piloting BreastCare Kenya — please reach out. We are actively seeking implementation partners.


## 👩🏾‍💻 About the Builder

Built by **Kerubo Bosire** for the **Build54 Hackathon.**

[![GitHub](https://img.shields.io/badge/GitHub-kerubobosire254-181717?style=flat-square&logo=github)](https://github.com/kerubobosire254)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Kerubo%20Bosire-0077B5?style=flat-square&logo=linkedin)](https://linkedin.com/in/kerubo-bosire-364523283)


## ⚠️ Disclaimer

BreastCare Kenya is a **clinical decision support tool**. It is designed to assist trained health practitioners — not replace clinical judgement. All referral and treatment decisions remain the responsibility of the treating practitioner.


*Built for the KAP gap. Built for Kenya. Built to save lives.* 🎗️

**Built for the KAP gap. Built for Kenya. Built to save lives.**

🎗️


</div>
