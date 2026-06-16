# 🎗️ BreastCare Kenya
### A Clinical Decision Support Platform Built for the KAP Gap

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org) [![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?style=flat-square&logo=streamlit)](https://streamlit.io) [![Offline](https://img.shields.io/badge/Works-Offline-2e7d32?style=flat-square)](https://github.com/kerubobosire254/breastcancer_help_app) [![Zero API Keys](https://img.shields.io/badge/Zero-API%20Keys-e91e8c?style=flat-square)](https://github.com/kerubobosire254/breastcancer_help_app)

### Breastcare app snippet

<img width="1353" height="595" alt="image" src="https://github.com/user-attachments/assets/f7b9cf58-d0cd-47a5-ad63-cb5155b661cc" />


### Breast Care App Live Demo

**Live App:** https://breastcarekenya.streamlit.app/

### Dashbord snippet
<img width="1231" height="558" alt="image" src="https://github.com/user-attachments/assets/b9ae3f38-f167-41f0-8d60-46f73da5f4a6" />

### Breast Care Dashboard Live Demo

**Dashboard:** https://breastcaredashboard.streamlit.app/

## The Gap That Killed Grace

Grace Wanjiku, 42, found a lump. She went to a Level 2 facility in Nairobi. The nurse assessed her and said: *"Come back if it gets worse."*

Three months later, she came back. Stage III.

This isn't a story about a bad nurse. The nurse knew what breast cancer was. She had decent knowledge scores. What she didn't have was a structured tool to move from *knowing* to *doing* — especially under the pressure of a busy outpatient queue with 40 other patients waiting.

That gap between knowing and doing has a name in public health: the **KAP gap** (Knowledge, Attitudes & Practices). And in Kenya, it's catastrophic.

---

## The Problem, In Numbers

This project began with original research surveying **250 Kenyan health practitioners** across professions, counties, and facility levels. Here's what the data showed:

| Domain | Mean Score | Category |
|--------|-----------|----------|
| 🧠 Knowledge | 54.7% | Poor |
| 💬 Attitude | 65.2% | Neutral |
| 🏥 Practice | **29.2%** | **Critical** |

That's a **36-point gap** between attitude and practice. Practitioners want to screen. They don't have the clinical scaffolding to act when it matters — at the point of care, with a real patient in the room.

The gap is worse at the frontline. Community Health Workers, the first point of contact for most Kenyans, scored **12.7% on practice**. Nurses scored **27%**. The people patients see first are the least equipped to act.

And the result: **78% of Kenyan breast cancer patients present at Stage III or IV**, when survival rates drop dramatically. The problem is not awareness. It is not funding. It is the absence of a functional point-of-care decision tool.

---

## What BreastCare Kenya Does

BreastCare Kenya is a **7-module clinical decision support platform** that guides a practitioner from first contact with a patient all the way through risk assessment, screening, referral, and follow-up — without ever making them re-enter data.

It works offline. It requires no API keys. It runs on three Python packages. It was designed for real Kenyan health settings: rural clinics with intermittent electricity, nurses managing 80 patients a day, CHWs with basic smartphones.

```
🏠 Home Dashboard
    ↓  KAP impact stats · overdue alerts · quick start
🩺 Risk Assessment
    ↓  patient auto-added to tracker · symptoms flow forward · risk gauge
✅ Screening Checklist
    ↓  symptoms auto-fill · red flags pre-highlighted
🔀 Referral Intelligence
    ↓  evidence-weighted decision · one-click save to tracker
🔔 Follow-Up Tracker  ←→  🩺 Risk Re-Assessment
    ↓  live data · journey timeline per patient
📊 Analytics Dashboard  ←  updates automatically · KAP insights tab
🤖 CareBot  ←  rule-based clinical NLP · no API needed
```

The critical design decision: **everything flows forward**. When a practitioner completes a risk assessment, the patient appears in the tracker automatically. When they move to the screening checklist, the symptoms are pre-loaded. When they generate a referral, the patient record updates in one click. No data re-entry. No dropped information. No "I'll do the paperwork later" — because there is no separate paperwork.

---

## The 7 Modules

### 🏠 Home Dashboard
Live overview of the KAP gap (the 36-point waterfall chart), overdue patient alerts, and quick-start navigation. The home screen exists to remind practitioners *why* the tool matters before they use it.

### 🩺 Quick Risk Assessment
Takes 8 inputs — age, symptoms, family history, reproductive history, risk factors — and returns a weighted risk score on a colour-coded gauge (LOW / MODERATE / HIGH), a referral decision, flagged red flags, and a follow-up date. Generates a one-click downloadable Clinical Handover Summary in `.txt`. Designed to be completable in under 3 minutes.

### ✅ Guided Screening Checklist
A 5-step structured workflow: History → Visual Inspection → Palpation → Lymph Nodes → Red Flag Detection. Symptoms from the risk assessment are pre-loaded. Red flags from the prior assessment are pre-highlighted in Step 5. The practitioner confirms, not re-enters. Clinical tips at every step.

### 🔀 Referral Intelligence Engine
Evidence-weighted referral recommendation: Urgent / Imaging / Routine / Education. The recommendation comes with a score breakdown bar chart showing exactly which clinical factors drove the decision — making it defensible, auditable, and educational. Follows the Kenya MOH referral pathway for breast conditions at primary care level.

### 🔔 Smart Follow-Up Tracker
Every patient assessed flows here automatically. Records update in one click when a referral is generated. The tracker auto-flags overdue follow-ups, supports rescheduling, and includes a **Patient Journey Timeline** — a full visual history of every assessment, screening, and referral for each patient. Filters by status, risk level, and county.

### 📊 Analytics Dashboard
Pulls live from session data — every assessment and referral appears in real time. Four tabs: Trends, By County, By Profession, and KAP Insights. The KAP Insights tab shows the original research data alongside app usage data — connecting the evidence base to actual practice patterns. Exportable as CSV.

### 🤖 CareBot — Clinical AI Assistant
A rule-based NLP engine covering 11 clinical topics: BSE technique, referral criteria, staging, KAP data, imaging, treatment, prevention, lump assessment, nipple discharge, and follow-up protocols. Works entirely offline. No API keys, no subscriptions, no latency. Quick-question chips for common queries. Built for nurses who need a fast answer without leaving the clinical flow.

---

## Run the Demo: Grace's Journey

The app ships with Grace Wanjiku's case pre-built. Run it in 5 minutes:

1. Open **🏠 Home** → click **"Run Grace's Demo"**
2. In **🩺 Risk Assessment** → click **"Pre-fill Grace's Case"** → hit **Calculate Risk**
3. The gauge hits **HIGH RISK** · red flags listed · handover summary generated
4. Grace is already in the Follow-Up Tracker — automatically
5. Click **"Continue to Screening Checklist"** → symptoms pre-loaded
6. Step through to Step 5 → red flags pre-highlighted
7. **"Continue to Referral Intelligence"** → symptoms auto-filled
8. **"Generate Referral Decision"** → Urgent Referral with evidence breakdown
9. **"Save Referral & Create Follow-Up"** → tracker record updated
10. **🔔 Follow-Up Tracker** → expand Grace → see full Journey Timeline
11. **📊 Analytics Dashboard** → Grace's screening in live charts
12. Ask **🤖 CareBot** *"What are the stages?"* — no internet needed

---

## Installation

```bash
git clone https://github.com/kerubobosire254/breastcancer_help_app.git
cd breastcancer_help_app
pip install -r requirements.txt
streamlit run breastcare.py
```

**Dependencies:** `streamlit>=1.28.0`, `pandas>=1.5.0`, `plotly>=5.15.0`. No API keys. No environment variables.

---

## Data

The app uses a synthetic dataset of 250 Kenyan health practitioners calibrated from published Kenya KAP literature (2013–2024), covering profession, county, facility setting, education level, and knowledge/attitude/practice scores. KAP categories follow standard public health thresholds.

All patient data in the demo is synthetic.

---

## Clinical Basis

Risk scoring draws on:
- Kenya National Cancer Screening Guidelines (2018)
- WHO Breast Cancer Early Detection Framework
- Kenya KAP studies (Otieno et al., 2020; Mwangi et al., 2022)
- IARC breast cancer risk factor evidence summaries

Referral logic follows the **Kenya Ministry of Health referral pathway** for breast conditions at Level 2–3.

---

## What's Next

The platform is functional. What would make it production-ready:

- **Hospital system integration** — connecting to NHIF records or facility EMRs so patient data persists beyond sessions
- **SMS follow-up reminders** — automated outreach to patients via Africa's Talking or similar
- **County-level deployment analytics** — understanding which counties have the highest referral rates and lowest follow-up compliance, so county health departments can target training
- **Expanded CareBot training** — moving from rule-based NLP to a lightweight fine-tuned model on clinical Kenyan content, while preserving offline capability
- **CHW-specific module** — a simplified interface for Community Health Workers with fewer inputs and more visual guidance, targeting the 12.7% practice gap at the front line

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Streamlit | App framework |
| Plotly | Interactive charts, gauges, KAP visualisations |
| Pandas | Data handling and analytics |
| Python 3 | Core language |
| Regex (built-in) | CareBot NLP pattern matching |

---

## Built By

**Kerubo Bosire** — Actuarial Science | Risk Analytics | Machine Learning

Built for the **Build54 Hackathon**. Built for the KAP gap. Built for Kenya. 🎗️

[![GitHub](https://img.shields.io/badge/GitHub-kerubobosire254-181717?style=flat-square&logo=github)](https://github.com/kerubobosire254) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Kerubo%20Bosire-0077B5?style=flat-square&logo=linkedin)](https://linkedin.com/in/kerubo-bosire-364523283)

> ⚠️ **Disclaimer:** BreastCare Kenya is a clinical decision support tool designed to assist trained health practitioners — not replace clinical judgement. All referral and treatment decisions remain the responsibility of the treating practitioner.
