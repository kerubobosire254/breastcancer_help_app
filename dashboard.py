"""
BreastCare Kenya — Clinical Decision Support Platform
FULLY CONNECTED — All 6 module connections active:
  1. Risk Assessment → Screening Checklist (pre-tagged with patient + red flags)
  2. Screening Checklist → Referral Intelligence (symptoms auto-filled)
  3. Referral Intelligence → Follow-Up Tracker (save referral in one click)
  4. Follow-Up Tracker → Risk Re-Assessment (continuity of care)
  5. Analytics pulls from live session data (real-time)
  6. Patient Journey Timeline (visual showstopper)

Run:
    pip install streamlit plotly pandas
    streamlit run breast_cancer_kap_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BreastCare Kenya",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown, .stText,
button, input, select, textarea, label, p, h1, h2, h3, h4, h5 {
    font-family: 'Nunito', sans-serif !important;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0a2e 0%, #2d1054 60%, #4a1068 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {
    color: #f0e6ff !important;
    font-family: 'Nunito', sans-serif !important;
}
section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.06);
    border-radius: 10px; padding: 10px 14px;
    margin: 3px 0; display: block;
    transition: background 0.2s; cursor: pointer;
    font-weight: 600; font-size: .93rem;
}
section[data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.14); }
.main { background: #faf7ff; }
.kcard {
    background: white; border-radius: 16px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 16px rgba(74,16,104,0.08);
    margin-bottom: 1rem; border-left: 5px solid #9c27b0;
}
.kcard.red    { border-color:#e53935; background:#fff5f5; }
.kcard.orange { border-color:#f57c00; background:#fff8f0; }
.kcard.green  { border-color:#2e7d32; background:#f5fff5; }
.kcard.blue   { border-color:#1565c0; background:#f0f6ff; }
.kcard.purple { border-color:#6a1b9a; }
.kcard h3 { margin:0 0 .3rem; font-size:1.1rem; font-weight:700; }
.kcard p  { margin:0; color:#555; font-size:.9rem; }
.risk-badge {
    display:inline-block; padding:7px 20px; border-radius:30px;
    font-weight:800; font-size:1rem; margin:10px 0;
    letter-spacing:.04em; text-transform:uppercase;
}
.risk-HIGH     { background:#e53935; color:white; }
.risk-MODERATE { background:#f57c00; color:white; }
.risk-LOW      { background:#2e7d32; color:white; }
.section-head {
    font-size:1.75rem; font-weight:800; color:#2d1054;
    border-bottom:3px solid #9c27b0;
    padding-bottom:.4rem; margin-bottom:1.1rem;
}
.section-sub { color:#6a1b9a; font-weight:600; font-size:.93rem; margin-bottom:1rem; }
.ref-card {
    border-radius:12px; padding:1rem 1.4rem;
    font-weight:700; font-size:.97rem; text-align:center; margin:.5rem 0;
}
.ref-URGENT    { background:#e53935; color:white; }
.ref-ROUTINE   { background:#f57c00; color:white; }
.ref-IMAGING   { background:#1565c0; color:white; }
.ref-EDUCATION { background:#2e7d32; color:white; }
.mtile {
    background:white; border-radius:14px; padding:1.2rem; text-align:center;
    box-shadow:0 2px 10px rgba(74,16,104,0.1); border-top:4px solid #9c27b0;
}
.mtile h2 { font-size:2.1rem; margin:0; color:#2d1054; font-weight:800; }
.mtile p  { margin:0; color:#888; font-size:.85rem; font-weight:600; }
.check-item {
    background:white; border-radius:10px; padding:.75rem 1rem; margin:.35rem 0;
    box-shadow:0 1px 6px rgba(0,0,0,0.05); border-left:4px solid #9c27b0; font-size:.91rem;
}
.check-item.flag { border-color:#e53935; background:#fff5f5; font-weight:700; }
.story-banner {
    background:linear-gradient(90deg,#880e4f,#4a148c);
    border-radius:14px; padding:1.1rem 1.5rem;
    color:white; margin-bottom:1.1rem;
}
.story-banner h4 { margin:0 0 .3rem; font-size:1.05rem; font-weight:800; }
.story-banner p  { margin:0; font-size:.87rem; opacity:.9; }
/* Connection banners */
.conn-flow {
    background:linear-gradient(90deg,#1a0a2e,#4a1068);
    border-radius:12px; padding:.85rem 1.3rem;
    color:#e1bee7; font-size:.88rem; font-weight:600;
    margin:1rem 0; border:1px solid rgba(156,39,176,0.35);
}
.conn-flow span { color:#ce93d8; font-weight:800; }
/* Journey timeline */
.tl-wrap { padding:.5rem 0; }
.tl-step {
    display:flex; gap:14px; align-items:flex-start; padding:.7rem 0;
    border-bottom:1px dashed #e8d5f5;
}
.tl-dot {
    width:14px; height:14px; border-radius:50%; flex-shrink:0;
    margin-top:4px;
}
.tl-done    { background:#2e7d32; }
.tl-active  { background:#f57c00; box-shadow:0 0 0 4px rgba(245,124,0,.2); }
.tl-pending { background:#bdbdbd; }
.tl-urgent  { background:#e53935; box-shadow:0 0 0 4px rgba(229,57,53,.2); }
.tl-label   { font-weight:700; font-size:.92rem; color:#2d1054; }
.tl-sub     { font-size:.8rem; color:#888; margin-top:2px; }
/* Connectivity */
.conn-badge { display:inline-block; border-radius:20px; padding:5px 16px;
              font-size:.78rem; font-weight:700; letter-spacing:.03em; }
.conn-online  { background:rgba(46,125,50,.18); color:#a5d6a7; border:1.5px solid #a5d6a7; }
.conn-offline { background:rgba(255,193,7,.15); color:#ffe082; border:1.5px solid #ffe082; }

/* ── Chatbot styles ── */
.chat-wrap {
    display:flex; flex-direction:column; gap:.6rem;
    max-height:480px; overflow-y:auto;
    padding:.5rem .2rem; margin-bottom:1rem;
}
.chat-msg {
    display:flex; gap:.65rem; align-items:flex-start;
}
.chat-msg.user { flex-direction:row-reverse; }
.chat-avatar {
    width:34px; height:34px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:1.1rem; flex-shrink:0;
}
.chat-avatar.bot  { background:#6a1b9a; }
.chat-avatar.user { background:#e8d5f5; }
.chat-bubble {
    max-width:80%; padding:.7rem 1rem; border-radius:14px;
    font-size:.91rem; line-height:1.55;
}
.chat-bubble.bot  {
    background:white; color:#2d1054;
    border:1px solid #e8d5f5;
    border-top-left-radius:4px;
    box-shadow:0 1px 6px rgba(74,16,104,0.08);
}
.chat-bubble.user {
    background:#6a1b9a; color:white;
    border-top-right-radius:4px;
}
.chat-chip-row { display:flex; flex-wrap:wrap; gap:.4rem; margin-top:.5rem; }
.chat-typing {
    display:inline-block; padding:.5rem .9rem;
    background:white; border-radius:12px; border:1px solid #e8d5f5;
    color:#888; font-size:.85rem; font-style:italic;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE — single source of truth for all connections
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    # Active patient context — the shared object flowing across modules
    if "active_patient" not in st.session_state:
        st.session_state.active_patient = {}   # {name, age, county, facility, practitioner}

    # Symptoms written by Screening Checklist → read by Referral Intelligence
    if "checklist_symptoms" not in st.session_state:
        st.session_state.checklist_symptoms = {
            "lump":False,"nipple_dc":False,"skin_changes":False,
            "nipple_invert":False,"axillary":False,"ulceration":False,
            "breast_pain":False,"asymmetry":False,
        }

    # Red flags from Risk Assessment → highlighted in Checklist Step 5
    if "assessment_red_flags" not in st.session_state:
        st.session_state.assessment_red_flags = []

    # Risk context from Assessment → carried into Referral
    if "assessment_context" not in st.session_state:
        st.session_state.assessment_context = {}  # {risk, score, fam_hist, menopause, age_group}

    # Last referral decision → saved to Follow-Up Tracker
    if "last_referral" not in st.session_state:
        st.session_state.last_referral = {}

    # Patient journey log: patient_id → list of {step, timestamp, detail}
    if "journeys" not in st.session_state:
        st.session_state.journeys = {}

    # Patient registry
    if "patients" not in st.session_state:
        st.session_state.patients = [
            {"id":"PT-001","name":"Grace Wanjiku","age":42,"county":"Nairobi",
             "facility":"Kenyatta National Hospital","practitioner":"Nurse Achieng",
             "risk":"HIGH","referral":"Urgent",
             "next_due":(datetime.today()-timedelta(days=3)).strftime("%Y-%m-%d"),
             "status":"Overdue","notes":"Palpable lump, nipple discharge",
             "journey":[
                 {"step":"Risk Assessment","ts":(datetime.today()-timedelta(days=10)).strftime("%d %b %Y"),"detail":"Score 75 · HIGH RISK","done":True},
                 {"step":"Screening Checklist","ts":(datetime.today()-timedelta(days=10)).strftime("%d %b %Y"),"detail":"3 red flags detected","done":True},
                 {"step":"Referral Generated","ts":(datetime.today()-timedelta(days=10)).strftime("%d %b %Y"),"detail":"Urgent referral to oncology","done":True},
                 {"step":"Follow-Up Due","ts":(datetime.today()-timedelta(days=3)).strftime("%d %b %Y"),"detail":"Overdue — no response","done":False,"urgent":True},
                 {"step":"Re-Assessment","ts":"Pending","detail":"Not yet done","done":False},
             ]},
            {"id":"PT-002","name":"Fatuma Hassan","age":35,"county":"Mombasa",
             "facility":"Coast General Hospital","practitioner":"Dr. Mwenda",
             "risk":"MODERATE","referral":"Imaging",
             "next_due":(datetime.today()+timedelta(days=2)).strftime("%Y-%m-%d"),
             "status":"Pending","notes":"Family history positive",
             "journey":[
                 {"step":"Risk Assessment","ts":(datetime.today()-timedelta(days=5)).strftime("%d %b %Y"),"detail":"Score 40 · MODERATE RISK","done":True},
                 {"step":"Referral Generated","ts":(datetime.today()-timedelta(days=5)).strftime("%d %b %Y"),"detail":"Imaging — mammogram ordered","done":True},
                 {"step":"Follow-Up Due","ts":(datetime.today()+timedelta(days=2)).strftime("%d %b %Y"),"detail":"Upcoming","done":False},
             ]},
            {"id":"PT-003","name":"Esther Chebet","age":28,"county":"Uasin Gishu",
             "facility":"Moi Teaching Hospital","practitioner":"Clinical Officer Ruto",
             "risk":"LOW","referral":"Education",
             "next_due":(datetime.today()+timedelta(days=30)).strftime("%Y-%m-%d"),
             "status":"Scheduled","notes":"Routine screening",
             "journey":[
                 {"step":"Risk Assessment","ts":(datetime.today()-timedelta(days=2)).strftime("%d %b %Y"),"detail":"Score 10 · LOW RISK","done":True},
                 {"step":"Education Provided","ts":(datetime.today()-timedelta(days=2)).strftime("%d %b %Y"),"detail":"BSE demonstrated","done":True},
                 {"step":"Follow-Up Due","ts":(datetime.today()+timedelta(days=30)).strftime("%d %b %Y"),"detail":"Annual screening scheduled","done":False},
             ]},
            {"id":"PT-004","name":"Mary Auma","age":55,"county":"Kisumu",
             "facility":"Kisumu County Hospital","practitioner":"Nurse Otieno",
             "risk":"HIGH","referral":"Urgent",
             "next_due":(datetime.today()-timedelta(days=7)).strftime("%Y-%m-%d"),
             "status":"Overdue","notes":"Post-menopausal bleeding, skin changes",
             "journey":[
                 {"step":"Risk Assessment","ts":(datetime.today()-timedelta(days=14)).strftime("%d %b %Y"),"detail":"Score 82 · HIGH RISK","done":True},
                 {"step":"Screening Checklist","ts":(datetime.today()-timedelta(days=14)).strftime("%d %b %Y"),"detail":"5 red flags detected","done":True},
                 {"step":"Referral Generated","ts":(datetime.today()-timedelta(days=14)).strftime("%d %b %Y"),"detail":"Urgent — called ahead","done":True},
                 {"step":"Follow-Up Due","ts":(datetime.today()-timedelta(days=7)).strftime("%d %b %Y"),"detail":"7 days overdue","done":False,"urgent":True},
                 {"step":"Re-Assessment","ts":"Pending","detail":"Not yet done","done":False},
             ]},
            {"id":"PT-005","name":"Jane Muthoni","age":48,"county":"Kiambu",
             "facility":"Thika Level 5","practitioner":"Dr. Kamau",
             "risk":"MODERATE","referral":"Routine",
             "next_due":(datetime.today()+timedelta(days=14)).strftime("%Y-%m-%d"),
             "status":"Pending","notes":"Asymmetric density on self-exam",
             "journey":[
                 {"step":"Risk Assessment","ts":(datetime.today()-timedelta(days=3)).strftime("%d %b %Y"),"detail":"Score 30 · MODERATE RISK","done":True},
                 {"step":"Follow-Up Due","ts":(datetime.today()+timedelta(days=14)).strftime("%d %b %Y"),"detail":"Routine follow-up","done":False},
             ]},
        ]

    # Screenings — now pulls live from patients too
    if "screenings" not in st.session_state:
        counties    = ["Nairobi","Mombasa","Kisumu","Kiambu","Nakuru","Uasin Gishu","Homa Bay"]
        facilities  = ["Public Hospital","Health Centre","Private Hospital","Dispensary","Community"]
        professions = ["Nurse","Clinical Officer","Doctor/Medical Officer","Midwife","Community Health Worker"]
        random.seed(42)
        rows = []
        for _ in range(120):
            d = datetime.today() - timedelta(days=random.randint(0,89))
            rows.append({
                "date":       d.strftime("%Y-%m-%d"),
                "month":      d.strftime("%b %Y"),
                "county":     random.choice(counties),
                "facility":   random.choice(facilities),
                "profession": random.choice(professions),
                "risk":       random.choices(["HIGH","MODERATE","LOW"],   weights=[15,35,50])[0],
                "referral":   random.choices(["Urgent","Imaging","Routine","Education"], weights=[12,20,30,38])[0],
                "followed_up":random.choices([True,False], weights=[55,45])[0],
            })
        st.session_state.screenings = pd.DataFrame(rows)

    if "grace_demo"       not in st.session_state: st.session_state.grace_demo       = False
    if "checklist_step"   not in st.session_state: st.session_state.checklist_step   = 1
    if "navigate_to"      not in st.session_state: st.session_state.navigate_to      = None
    if "chat_history"     not in st.session_state:
        st.session_state.chat_history = [
            {"role":"bot","text":"👋 Hi! I'm **BreastCare AI**, your clinical support assistant.\n\nI can help you with:\n- 🔴 Understanding **risk factors** & scores\n- ✅ **Screening checklist** guidance\n- 🔀 **Referral decisions** explained\n- 📋 **Follow-up** protocols\n- 🇰🇪 Kenya-specific breast cancer facts\n\nAsk me anything, or tap a quick question below."}
        ]

init_state()


# ── Helper: log a journey event ───────────────────────────────────────────────
def log_journey(patient_id, step, detail, done=True, urgent=False):
    for i, p in enumerate(st.session_state.patients):
        if p["id"] == patient_id:
            if "journey" not in st.session_state.patients[i]:
                st.session_state.patients[i]["journey"] = []
            st.session_state.patients[i]["journey"].append({
                "step":step, "ts":datetime.today().strftime("%d %b %Y"),
                "detail":detail, "done":done, "urgent":urgent,
            })


# ── Helper: compute risk score ────────────────────────────────────────────────
def compute_risk(lump, nipple_dc, skin_changes, nipple_invert, axillary,
                 ulceration, breast_pain, fam_hist, menopause, menarche,
                 parity, hrt, prev_biopsy, obesity, breastfed, age):
    s = 0
    if ulceration:    s += 40
    if axillary:      s += 30
    if skin_changes:  s += 25
    if nipple_invert: s += 20
    if lump:          s += 20
    if nipple_dc:     s += 15
    if breast_pain:   s += 5
    if fam_hist == "2+ relatives or BRCA known": s += 25
    elif fam_hist == "1st-degree relative":      s += 15
    if menopause == "Post-menopausal (>5 yrs)":  s += 15
    elif menopause == "Post-menopausal (<5 yrs)":s += 8
    if menarche == "<13 years (early)":          s += 8
    if parity   == "Nulliparous or first child ≥30": s += 8
    if hrt:          s += 8
    if prev_biopsy:  s += 10
    if obesity:      s += 5
    if breastfed:    s -= 8
    if age >= 50:    s += 15
    elif age >= 40:  s += 8
    elif age >= 35:  s += 4

    if s >= 50 or ulceration or (lump and axillary) or (lump and skin_changes):
        risk = "HIGH"
    elif s >= 25:
        risk = "MODERATE"
    else:
        risk = "LOW"
    return min(s, 100), risk


# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center;padding:1.1rem 0 .6rem;'>
  <div style='font-size:2.2rem;'>🎗️</div>
  <div style='font-size:1.3rem;font-weight:800;color:#f0e6ff;letter-spacing:.02em;'>
    BreastCare Kenya</div>
  <div style='font-size:.78rem;color:#c9a8e8;margin-top:.25rem;font-weight:600;'>
    Clinical Decision Support</div>
</div>
<hr style='border-color:rgba(255,255,255,0.12);margin:.5rem 0 1rem;'>
""", unsafe_allow_html=True)

# Active patient banner in sidebar
ap = st.session_state.active_patient
if ap.get("name"):
    risk_col = "#e53935" if ap.get("risk")=="HIGH" else "#f57c00" if ap.get("risk")=="MODERATE" else "#2e7d32"
    st.sidebar.markdown(f"""
    <div style='background:rgba(255,255,255,0.08);border-radius:10px;padding:.8rem 1rem;
                margin-bottom:.8rem;border-left:3px solid {risk_col};'>
      <div style='font-size:.72rem;color:#c9a8e8;font-weight:700;text-transform:uppercase;
                  letter-spacing:.06em;'>Active Patient</div>
      <div style='font-weight:800;font-size:.95rem;color:#f0e6ff;margin-top:.2rem;'>
        👩🏾 {ap["name"]}</div>
      <div style='font-size:.78rem;color:#c9a8e8;'>{ap.get("county","")} · {ap.get("facility","")}</div>
      <div style='font-size:.78rem;margin-top:.3rem;'>
        <span style='background:{risk_col};color:white;border-radius:10px;
                     padding:2px 8px;font-weight:700;font-size:.7rem;'>
          {ap.get("risk","—")} RISK
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Navigation — support programmatic navigation via session state key
nav_options = [
    "🩺  Risk Assessment",
    "✅  Screening Checklist",
    "🔔  Follow-Up Tracker",
    "🔀  Referral Intelligence",
    "📊  Analytics Dashboard",
    "🤖  AI Assistant Chatbot",
]

# Initialise radio state on first load
if "_nav_radio" not in st.session_state:
    st.session_state["_nav_radio"] = nav_options[0]

module = st.sidebar.radio("", nav_options, key="_nav_radio")

st.sidebar.markdown("<hr style='border-color:rgba(255,255,255,0.12);margin:1rem 0;'>", unsafe_allow_html=True)

# Cache connectivity check — runs once per session, not on every rerun
if "_connectivity" not in st.session_state:
    try:
        import urllib.request
        urllib.request.urlopen("https://dns.google", timeout=2)
        st.session_state._connectivity = ("conn-online", "🟢  Online")
    except Exception:
        st.session_state._connectivity = ("conn-offline", "🟡  Offline — cached data active")
cc, ct = st.session_state._connectivity
st.sidebar.markdown(
    f"<div style='text-align:center;'><span class='conn-badge {cc}'>{ct}</span></div>",
    unsafe_allow_html=True)

st.sidebar.markdown("""
<hr style='border-color:rgba(255,255,255,0.12);margin:1rem 0;'>
<div style='font-size:.75rem;color:#c9a8e8;text-align:center;line-height:1.7;'>
  Calibrated from Kenya KAP literature<br>2013–2024 · Synthetic demo data<br>
  <em>Not a substitute for clinical judgement</em>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — RISK ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════
if "Risk Assessment" in module:
    st.markdown('<div class="section-head">🩺 Quick Breast Cancer Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Complete the form · Risk calculated instantly · Patient context flows to all modules</div>', unsafe_allow_html=True)

    # Re-assessment pre-fill from Follow-Up Tracker
    reassess = st.session_state.get("reassess_patient", {})
    if reassess:
        st.markdown(f"""
        <div class="conn-flow">
          🔄 <span>Re-Assessment</span> — continuing care for
          <span>{reassess.get("name","")}</span> ·
          Previous risk: <span>{reassess.get("risk","")}</span> ·
          Last seen: <span>{reassess.get("last_seen","—")}</span>
        </div>
        """, unsafe_allow_html=True)

    # Grace demo banner
    with st.expander("🎬 Hackathon Demo — Follow Grace's Journey", expanded=False):
        st.markdown("""
        <div class="story-banner">
          <h4>👩🏾 Meet Grace Wanjiku — 42, Nairobi</h4>
          <p>A mother of three who almost ignored a lump she found three months ago.
          Watch how BreastCare Kenya catches what could have been missed.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        **Without this app:** Grace visited a busy health centre. She mentioned a lump almost
        as an afterthought. The nurse had no structured tool. Grace was told *"come back if it
        gets worse."* Three months later she returned — Stage III.

        **With BreastCare Kenya:** That first visit flags HIGH RISK in under 2 minutes,
        triggers an urgent referral, and automatically tracks her follow-up.
        """)
        ca, cb = st.columns(2)
        if ca.button("🚀 Pre-fill Grace's Case", use_container_width=True):
            st.session_state.grace_demo = True
            st.session_state.reassess_patient = {}
            st.rerun()
        if cb.button("🔄 Clear / New Patient",   use_container_width=True):
            st.session_state.grace_demo = False
            st.session_state.reassess_patient = {}
            st.rerun()

    grace = st.session_state.grace_demo

    # Decide pre-fill source: reassess > grace > blank
    pf_name  = reassess.get("name","Grace Wanjiku" if grace else "")
    pf_age   = reassess.get("age", 42 if grace else 40)
    pf_county= reassess.get("county","Nairobi")
    pf_fac   = reassess.get("facility","Health Centre")
    pf_prac  = reassess.get("practitioner","Nurse Achieng" if grace else "")

    if grace and not reassess:
        st.info("👩🏾 **Grace's case loaded.** Review below and click Calculate Risk.")

    with st.form("risk_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("**Patient Information**")
            p_name       = st.text_input("Patient Name",      value=pf_name,  placeholder="e.g. Grace Wanjiku")
            p_age        = st.number_input("Age (years)", 18, 90, value=int(pf_age))
            counties_list= ["Nairobi","Mombasa","Kisumu","Kiambu","Nakuru","Uasin Gishu","Homa Bay","Other"]
            fac_list     = ["Public Hospital","Health Centre","Private Hospital","Dispensary","Community"]
            ci           = counties_list.index(pf_county) if pf_county in counties_list else 0
            fi           = fac_list.index(pf_fac) if pf_fac in fac_list else 0
            p_county     = st.selectbox("County", counties_list, index=ci)
            p_facility   = st.selectbox("Facility", fac_list, index=fi)
            practitioner = st.text_input("Practitioner Name", value=pf_prac, placeholder="Your name")

        with c2:
            st.markdown("**Symptoms & Signs**")
            lump          = st.checkbox("Palpable breast lump",                   value=True  if grace else False)
            nipple_dc     = st.checkbox("Nipple discharge (non-milk)",            value=True  if grace else False)
            skin_changes  = st.checkbox("Skin changes (peau d'orange, dimpling)", value=False)
            nipple_invert = st.checkbox("Nipple inversion / retraction",          value=False)
            axillary      = st.checkbox("Axillary lymph node enlargement",        value=True  if grace else False)
            breast_pain   = st.checkbox("Persistent unexplained breast pain",     value=True  if grace else False)
            ulceration    = st.checkbox("Ulceration / open wound on breast",      value=False)

        with c3:
            st.markdown("**Risk Factors**")
            fam_hist    = st.selectbox("Family history",
                                       ["None","1st-degree relative","2+ relatives or BRCA known"],
                                       index=1 if grace else 0)
            menarche    = st.selectbox("Age at first period",  ["≥13 years (normal)","<13 years (early)"])
            menopause   = st.selectbox("Menopausal status",    ["Pre-menopausal","Post-menopausal (<5 yrs)","Post-menopausal (>5 yrs)"])
            parity      = st.selectbox("Parity",               ["Parous, first child <30","Nulliparous or first child ≥30"])
            breastfed   = st.checkbox("Breastfed ≥1 year (protective)", value=True if grace else False)
            hrt         = st.checkbox("Current HRT / OCP use (>5 yrs)", value=False)
            prev_biopsy = st.checkbox("Previous abnormal breast biopsy",value=False)
            obesity     = st.checkbox("BMI ≥30 / obesity",              value=False)

        submitted = st.form_submit_button("🔍  Calculate Risk & Recommend Action", use_container_width=True)

    if submitted:
        score, risk = compute_risk(
            lump, nipple_dc, skin_changes, nipple_invert, axillary, ulceration,
            breast_pain, fam_hist, menopause, menarche, parity, hrt,
            prev_biopsy, obesity, breastfed, p_age
        )

        if risk == "HIGH":
            referral   = "Urgent"
            ref_action = "Refer IMMEDIATELY to oncology/surgical unit. Do not delay. Document and call ahead."
            ref_class  = "red"
        elif risk == "MODERATE":
            referral   = "Imaging" if (lump or axillary) else "Routine"
            ref_action = ("Order mammogram/ultrasound within 2 weeks." if referral=="Imaging"
                          else "Schedule follow-up in 4–6 weeks. Educate on BSE.")
            ref_class  = "orange"
        else:
            referral   = "Education"
            ref_action = "Provide BSE education. Schedule annual screening."
            ref_class  = "green"

        red_flags = [s for s,v in {
            "Palpable lump":lump,"Nipple discharge":nipple_dc,
            "Skin changes":skin_changes,"Nipple inversion":nipple_invert,
            "Axillary nodes":axillary,"Ulceration":ulceration,
        }.items() if v]

        next_due = (datetime.today() + timedelta(
            days=1 if risk=="HIGH" else 14 if risk=="MODERATE" else 365
        )).strftime("%Y-%m-%d")

        # ── CONNECTION 1: write active patient + context to session state ──
        st.session_state.active_patient = {
            "name":p_name,"age":p_age,"county":p_county,
            "facility":p_facility,"practitioner":practitioner,
            "risk":risk,"score":score,"referral":referral,
        }
        st.session_state.assessment_red_flags = red_flags
        st.session_state.assessment_context = {
            "risk":risk,"score":score,"fam_hist":fam_hist,
            "menopause":menopause,"age_group":"50+" if p_age>=50 else "35–49" if p_age>=35 else "<35",
            "post_meno": menopause != "Pre-menopausal",
        }
        # Pre-fill checklist symptoms from assessment
        st.session_state.checklist_symptoms = {
            "lump":lump,"nipple_dc":nipple_dc,"skin_changes":skin_changes,
            "nipple_invert":nipple_invert,"axillary":axillary,
            "ulceration":ulceration,"breast_pain":breast_pain,"asymmetry":False,
        }
        st.session_state.checklist_step = 1

        # Results display
        st.markdown("---")
        st.markdown("### 📋 Assessment Result")
        rc1, rc2 = st.columns([1,2])
        with rc1:
            sc = "#e53935" if risk=="HIGH" else "#f57c00" if risk=="MODERATE" else "#2e7d32"
            ri = "🚨" if referral=="Urgent" else "🖼️" if referral=="Imaging" else "📅" if referral=="Routine" else "📚"
            st.markdown(f"""
            <div class="kcard {ref_class}">
              <h3>{p_name or 'Patient'} · Age {p_age}</h3>
              <p>{p_county} · {p_facility}</p><br>
              <div style='font-size:.82rem;color:#888;font-weight:600;'>Risk Score</div>
              <div style='font-size:2.6rem;font-weight:800;color:{sc};line-height:1.1;'>{score}</div>
              <span class='risk-badge risk-{risk}'>{risk} RISK</span><br><br>
              <div style='font-size:.82rem;color:#888;font-weight:600;'>Referral Decision</div>
              <div class='ref-card ref-{referral}' style='margin-top:.4rem;'>{ri} {referral} Referral</div>
            </div>
            """, unsafe_allow_html=True)

        with rc2:
            st.markdown(f"""
            <div class="kcard blue">
              <h3>Recommended Action</h3>
              <p style='font-size:1rem;color:#1a237e;font-weight:700;'>{ref_action}</p>
            </div>
            """, unsafe_allow_html=True)
            if red_flags:
                fl = "".join([f"<li style='margin:.3rem 0;'>⚠️ {f}</li>" for f in red_flags])
                st.markdown(f"""
                <div class="kcard red">
                  <h3>🚩 Red Flags Detected</h3>
                  <ul style='margin:.5rem 0 0;padding-left:1.2rem;'>{fl}</ul>
                </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="kcard purple">
              <h3>📅 Follow-Up Due</h3>
              <p style='font-size:1rem;font-weight:700;color:#4a148c;'>{next_due}</p>
              <p>Practitioner: {practitioner or 'Not recorded'}</p>
            </div>""", unsafe_allow_html=True)

        # Save patient + screening
        if p_name:
            pid = f"PT-{len(st.session_state.patients)+1:03d}"
            st.session_state.patients.append({
                "id":pid,"name":p_name,"age":p_age,"county":p_county,
                "facility":p_facility,"practitioner":practitioner,
                "risk":risk,"referral":referral,"next_due":next_due,
                "status":"Urgent" if risk=="HIGH" else "Pending",
                "notes":", ".join(red_flags) if red_flags else "No red flags",
                "journey":[{
                    "step":"Risk Assessment",
                    "ts":datetime.today().strftime("%d %b %Y"),
                    "detail":f"Score {score} · {risk} RISK",
                    "done":True,"urgent":risk=="HIGH",
                }],
            })
            st.session_state.active_patient["id"] = pid
            st.session_state.screenings = pd.concat([
                st.session_state.screenings,
                pd.DataFrame([{
                    "date":datetime.today().strftime("%Y-%m-%d"),
                    "month":datetime.today().strftime("%b %Y"),
                    "county":p_county,"facility":p_facility,
                    "profession":practitioner or "Unknown","risk":risk,
                    "referral":referral,"followed_up":False,
                }])
            ], ignore_index=True)

        # ── CONNECTION 1 CTA ───────────────────────────────────────────────
        st.markdown("""
        <div class="conn-flow">
          ✅ Assessment complete.
          <span>Next step:</span> proceed to the Screening Checklist —
          symptoms are already filled in for this patient.
        </div>
        """, unsafe_allow_html=True)
        if st.button("➡️  Continue to Screening Checklist for " + (p_name or "Patient"), use_container_width=True):
            st.session_state["_nav_radio"] = "✅  Screening Checklist"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — SCREENING CHECKLIST
# ══════════════════════════════════════════════════════════════════════════════
elif "Screening Checklist" in module:
    st.markdown('<div class="section-head">✅ Guided Screening Checklist</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Step-by-step examination workflow · Symptoms pre-filled from Risk Assessment · Red flags auto-detected</div>', unsafe_allow_html=True)

    ap = st.session_state.active_patient
    if ap.get("name"):
        st.markdown(f"""
        <div class="conn-flow">
          🔗 <span>Connected from Risk Assessment</span> —
          examining <span>{ap["name"]}</span> ·
          Risk: <span>{ap.get("risk","—")}</span> ·
          Symptoms pre-loaded below
        </div>
        """, unsafe_allow_html=True)

    cs = st.session_state.checklist_symptoms
    rf_from_assessment = st.session_state.assessment_red_flags

    steps = {
        1:("📋 History Taking",[
            "Chief complaint documented",
            "Duration of symptoms recorded",
            "Previous breast conditions / biopsies noted",
            "Menstrual & reproductive history taken",
            "Family history (1st & 2nd degree) documented",
            "Medication history (HRT, OCP) reviewed",
            "Alcohol / smoking history noted",
        ]),
        2:("👁️ Visual Inspection (patient seated)",[
            "Breast symmetry assessed — note asymmetry",
            "Skin surface checked: peau d'orange, dimpling",
            "Nipple position & symmetry checked",
            "Areola colour changes noted",
            "Visible lump or contour change observed",
            "Arms raised — repeat inspection",
            "Hands on hips (pectoral contraction) — repeat",
        ]),
        3:("🖐️ Palpation (patient supine)",[
            "Systematic pattern chosen (spiral / radial / grid)",
            "All 4 quadrants palpated with 3-finger technique",
            "Tail of Spence (axillary extension) palpated",
            "Areola & nipple gently compressed",
            "Nipple discharge — colour & consistency noted",
            "Lump characteristics: size, shape, mobility, tenderness",
        ]),
        4:("🔍 Lymph Node Examination",[
            "Axillary nodes — anterior, posterior, medial",
            "Supraclavicular nodes palpated",
            "Infraclavicular nodes palpated",
            "Node size, consistency, mobility noted",
            "Bilateral comparison performed",
        ]),
        5:("🚩 Red Flag Detection & Decision",[
            "Hard, irregular, fixed lump present?",
            "Skin tethering or dimpling present?",
            "Bloody or spontaneous nipple discharge?",
            "Nipple retraction (new)?",
            "Axillary nodes enlarged / fixed?",
            "Ulceration or skin breakdown?",
            "Post-menopausal patient with any lump?",
        ]),
    }

    # Map assessment symptoms to step-5 red flags for pre-highlighting
    flag_map = {
        0: cs.get("lump", False),
        2: cs.get("skin_changes", False),
        3: cs.get("nipple_invert", False),
        4: cs.get("axillary", False),
        5: cs.get("ulceration", False),
    }

    step = st.session_state.checklist_step
    cp, cm, cn = st.columns([1,4,1])
    with cp:
        if st.button("← Back") and step > 1:
            st.session_state.checklist_step -= 1
            st.rerun()
    with cm:
        st.progress(step / len(steps))
        st.markdown(f"**Step {step} of {len(steps)}**")
    with cn:
        if st.button("Next →") and step < len(steps):
            st.session_state.checklist_step += 1
            st.rerun()

    title, items = steps[step]
    st.markdown(f"### {title}")

    if step == 5 and rf_from_assessment:
        st.info(f"🔗 **Pre-highlighted from Risk Assessment:** {', '.join(rf_from_assessment)}")

    checked = []
    for i, item in enumerate(items):
        # Pre-tick red flags on step 5 based on assessment
        pre = flag_map.get(i, False) if step == 5 else False
        val = st.checkbox(item, value=pre, key=f"chk_{step}_{i}")
        is_flag_step = (step == 5)
        css  = "check-item flag" if (is_flag_step and val) else "check-item"
        icon = "🚩" if (is_flag_step and val) else "✔️" if val else "○"
        st.markdown(f'<div class="{css}">{icon} {item}</div>', unsafe_allow_html=True)
        checked.append(val)

        # ── CONNECTION 2: write symptoms back to session state on step 3 ──
        if step == 3:
            sym_map = {4:"nipple_dc", 5:"lump"}
            if i in sym_map and val:
                st.session_state.checklist_symptoms[sym_map[i]] = True

    st.markdown(f"<br>**{sum(checked)}/{len(items)} items completed**", unsafe_allow_html=True)

    tips = {
        1:"💡 Ensure patient privacy and explain each step before proceeding.",
        2:"💡 Adequate lighting essential. Ask patient to disrobe to waist.",
        3:"💡 Use pads of fingers — not tips. Apply light, medium, and firm pressure.",
        4:"💡 Stand on same side as axilla. Support patient's arm throughout.",
        5:"💡 Red flags must be documented and acted on immediately.",
    }
    st.info(tips[step])

    if step == 5:
        rf_count = sum(checked)
        if rf_count >= 3:
            st.error(f"🚨 **{rf_count} red flags — URGENT REFERRAL required.**")
        elif rf_count >= 1:
            st.warning(f"⚠️ **{rf_count} red flag(s) — imaging within 2 weeks.**")
        else:
            st.success("✅ No red flags — educate on BSE and schedule annual follow-up.")

        # ── CONNECTION 2 CTA ───────────────────────────────────────────────
        st.markdown("""
        <div class="conn-flow">
          🔗 Checklist complete. <span>Symptoms auto-filled</span> in Referral Intelligence.
          One click to generate the referral decision.
        </div>
        """, unsafe_allow_html=True)

        # Log checklist in patient journey
        if ap.get("id"):
            log_journey(ap["id"], "Screening Checklist",
                        f"{rf_count} red flag(s) detected", done=True, urgent=rf_count>=3)

        if st.button("➡️  Continue to Referral Intelligence", use_container_width=True):
            st.session_state["_nav_radio"] = "🔀  Referral Intelligence"
            st.rerun()

    if st.button("🔄 Restart Checklist"):
        st.session_state.checklist_step = 1
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 4 — REFERRAL INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif "Referral" in module:
    st.markdown('<div class="section-head">🔀 Referral Intelligence Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Symptoms auto-filled from Screening Checklist · Evidence-based referral decision</div>', unsafe_allow_html=True)

    ap  = st.session_state.active_patient
    cs  = st.session_state.checklist_symptoms
    ctx = st.session_state.assessment_context

    if ap.get("name"):
        st.markdown(f"""
        <div class="conn-flow">
          🔗 <span>Connected from Screening Checklist</span> —
          generating referral for <span>{ap["name"]}</span> ·
          Symptoms pre-loaded · Risk context carried forward
        </div>
        """, unsafe_allow_html=True)

    rc1, rc2 = st.columns(2)
    with rc1:
        st.markdown("**Clinical Signs** *(pre-filled from Screening Checklist)*")
        s_lump     = st.checkbox("🔴 Palpable breast lump",          value=cs.get("lump",False))
        s_axillary = st.checkbox("🔴 Axillary lymphadenopathy",      value=cs.get("axillary",False))
        s_skin     = st.checkbox("🟠 Skin changes / dimpling",       value=cs.get("skin_changes",False))
        s_nipple_i = st.checkbox("🟠 Nipple inversion (new)",        value=cs.get("nipple_invert",False))
        s_nipple_d = st.checkbox("🟠 Nipple discharge (non-milk)",   value=cs.get("nipple_dc",False))
        s_ulcer    = st.checkbox("🔴 Ulceration / wound on breast",  value=cs.get("ulceration",False))
        s_pain     = st.checkbox("🟡 Breast pain (persistent)",      value=cs.get("breast_pain",False))
        s_asymm    = st.checkbox("🟡 Breast asymmetry (new)",        value=cs.get("asymmetry",False))

    with rc2:
        st.markdown("**Patient Context** *(carried from Risk Assessment)*")
        age_options = ["<35 years","35–49 years","50+ years"]
        age_default = age_options.index(ctx["age_group"]) if ctx.get("age_group") in age_options else 0
        age_grp     = st.selectbox("Age group", age_options, index=age_default)

        fhx_options = ["None","1st-degree relative","Strong / BRCA"]
        fhx_map     = {"None":0,"1st-degree relative":1,"2+ relatives or BRCA known":2}
        fhx_default = fhx_map.get(ctx.get("fam_hist","None"),0)
        fhx         = st.selectbox("Family history", fhx_options, index=min(fhx_default,2))

        prev_ca   = st.checkbox("Personal history of any cancer")
        post_meno = st.checkbox("Post-menopausal", value=ctx.get("post_meno",False))
        rapid_chg = st.checkbox("Rapid change in size / appearance")

    if st.button("🔀  Generate Referral Decision", use_container_width=True):
        u, img, r, e = 0, 0, 0, 0
        if s_lump:     u += 3; img += 2
        if s_axillary: u += 4
        if s_ulcer:    u += 5
        if s_skin:     u += 3; img += 2
        if s_nipple_i: u += 2; img += 2
        if s_nipple_d: u += 1; img += 3
        if rapid_chg:  u += 2
        if prev_ca:    u += 3
        if fhx == "Strong / BRCA":         u += 2; img += 2
        elif fhx == "1st-degree relative": img += 2; r += 1
        if post_meno and s_lump: u += 2
        if age_grp == "50+ years": img += 1
        if s_pain and not s_lump:  r += 2; e += 1
        if s_asymm and not s_lump: img += 1; r += 1
        if not any([s_lump,s_axillary,s_skin,s_nipple_i,s_nipple_d,s_ulcer]): e += 3

        scores   = {"Urgent":u,"Imaging":img,"Routine":r,"Education":e}
        decision = max(scores, key=scores.get)

        ref_details = {
            "Urgent":    ("🚨","#e53935","Refer within 24 hours to oncology/surgical unit.",
                          ["Contact facility before sending patient","Provide written referral letter",
                           "Ensure patient has transport support","Document and notify in-charge"]),
            "Imaging":   ("🖼️","#1565c0","Mammogram and/or ultrasound within 2 weeks.",
                          ["Bilateral mammogram if ≥40 years","Ultrasound if <40 or dense breasts",
                           "Provide written imaging request","Book follow-up to review results"]),
            "Routine":   ("📅","#f57c00","Reassess within 4–6 weeks.",
                          ["Educate patient on BSE","Document current findings",
                           "Book follow-up before patient leaves","Advise return if symptoms worsen"]),
            "Education": ("📚","#2e7d32","No acute clinical concern identified.",
                          ["Demonstrate BSE technique","Provide take-home BSE card",
                           "Discuss annual screening schedule","Advise on risk reduction"]),
        }
        icon, clr, headline, actions = ref_details[decision]
        actions_html = "".join([f"<li style='margin:.4rem 0;'>{a}</li>" for a in actions])

        next_due = (datetime.today() + timedelta(
            days=1 if decision=="Urgent" else 14 if decision=="Imaging" else 42 if decision=="Routine" else 365
        )).strftime("%Y-%m-%d")

        st.markdown("---")
        st.markdown(f"""
        <div style='background:{clr};color:white;border-radius:16px;padding:1.5rem 2rem;
                    margin-bottom:1rem;font-family:Nunito,sans-serif;'>
          <div style='font-size:2rem;'>{icon}</div>
          <div style='font-size:1.45rem;font-weight:800;margin:.25rem 0;'>{decision} Referral</div>
          <div style='font-size:.97rem;opacity:.92;'>{headline}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="kcard">
          <h3>📋 Action Steps</h3>
          <ul style='margin:.5rem 0;padding-left:1.3rem;color:#333;font-size:.93rem;'>
            {actions_html}
          </ul>
        </div>
        """, unsafe_allow_html=True)

        fig_s = px.bar(x=list(scores.keys()), y=list(scores.values()),
                       color=list(scores.keys()),
                       color_discrete_map={"Urgent":"#e53935","Imaging":"#1565c0",
                                           "Routine":"#f57c00","Education":"#2e7d32"},
                       template="plotly_white",
                       labels={"x":"Decision","y":"Evidence Score"},
                       title="Evidence weighting behind recommendation")
        fig_s.update_layout(showlegend=False, font_family="Nunito")
        st.plotly_chart(fig_s, use_container_width=True)

        if decision in ["Urgent","Imaging"]:
            st.warning("⚠️ **Practice gap alert:** Kenya KAP data shows only 12–20% of cases meeting urgent criteria are referred. This patient meets the threshold — please act.")

        # Save referral to session state for Follow-Up Tracker connection
        st.session_state.last_referral = {
            "decision":   decision,
            "next_due":   next_due,
            "patient":    ap.get("name","Unknown"),
            "patient_id": ap.get("id",""),
            "risk":       ap.get("risk","MODERATE"),
            "county":     ap.get("county",""),
            "facility":   ap.get("facility",""),
            "practitioner":ap.get("practitioner",""),
            "age":        ap.get("age",0),
        }

        # Log in journey
        if ap.get("id"):
            log_journey(ap["id"],"Referral Generated",
                        f"{decision} referral · due {next_due}",
                        done=True, urgent=decision=="Urgent")

        # ── CONNECTION 3 CTA ───────────────────────────────────────────────
        st.markdown("""
        <div class="conn-flow">
          🔗 Referral decision generated.
          <span>One click</span> to save to Follow-Up Tracker —
          due date, risk level, and referral type auto-filled.
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"➡️  Save Referral & Create Follow-Up for {ap.get('name','Patient')}", use_container_width=True):
            lr = st.session_state.last_referral
            # Update existing patient or add new
            found = False
            for i, p in enumerate(st.session_state.patients):
                if p["id"] == lr["patient_id"]:
                    st.session_state.patients[i]["referral"]  = lr["decision"]
                    st.session_state.patients[i]["next_due"]  = lr["next_due"]
                    st.session_state.patients[i]["status"]    = "Urgent" if lr["decision"]=="Urgent" else "Pending"
                    found = True
            if not found and lr["patient"]:
                st.session_state.patients.append({
                    "id":f"PT-{len(st.session_state.patients)+1:03d}",
                    "name":lr["patient"],"age":lr["age"],
                    "county":lr["county"],"facility":lr["facility"],
                    "practitioner":lr["practitioner"],"risk":lr["risk"],
                    "referral":lr["decision"],"next_due":lr["next_due"],
                    "status":"Urgent" if lr["decision"]=="Urgent" else "Pending",
                    "notes":f"Auto-saved from Referral Intelligence",
                    "journey":[{
                        "step":"Referral Generated","ts":datetime.today().strftime("%d %b %Y"),
                        "detail":f"{lr['decision']} · due {lr['next_due']}","done":True,
                    }],
                })
            st.success(f"✅ Referral saved. {lr['patient']} is now in the Follow-Up Tracker.")
            st.session_state["_nav_radio"] = "🔔  Follow-Up Tracker"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3 — FOLLOW-UP TRACKER
# ══════════════════════════════════════════════════════════════════════════════
elif "Follow-Up" in module:
    st.markdown('<div class="section-head">🔔 Smart Follow-Up Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">All patients from Risk Assessment & Referral Intelligence appear here · Full journey timeline per patient</div>', unsafe_allow_html=True)

    df_p  = pd.DataFrame(st.session_state.patients)
    today = datetime.today().strftime("%Y-%m-%d")

    def auto_status(row):
        if row["next_due"] < today and row["status"] not in ("Done",):
            return "Overdue"
        return row["status"]
    df_p["status"] = df_p.apply(auto_status, axis=1)

    n_total   = len(df_p)
    n_overdue = len(df_p[df_p["status"]=="Overdue"])
    n_high    = len(df_p[df_p["risk"]=="HIGH"])
    n_pending = len(df_p[df_p["status"]=="Pending"])

    t1,t2,t3,t4 = st.columns(4)
    for col,val,lbl,clr in [
        (t1,n_total,  "Total Patients",    "#6a1b9a"),
        (t2,n_overdue,"Overdue",           "#e53935"),
        (t3,n_high,   "High Risk",         "#f57c00"),
        (t4,n_pending,"Pending Follow-Up", "#1565c0"),
    ]:
        col.markdown(f"""<div class="mtile" style="border-top-color:{clr};">
          <h2 style="color:{clr};">{val}</h2><p>{lbl}</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    f_status = fc1.selectbox("Filter by Status",["All","Overdue","Pending","Scheduled","Urgent","Done"])
    f_risk   = fc2.selectbox("Filter by Risk",  ["All","HIGH","MODERATE","LOW"])

    view = df_p.copy()
    if f_status != "All": view = view[view["status"]==f_status]
    if f_risk   != "All": view = view[view["risk"]  ==f_risk]

    st.markdown(f"**Showing {len(view)} patients**")
    st.markdown("---")

    for _, row in view.iterrows():
        diff      = (datetime.strptime(row["next_due"],"%Y-%m-%d") - datetime.today()).days
        due_txt   = f"⚠️ {abs(diff)} days overdue" if diff < 0 else f"Due in {diff} days"
        ri        = "🔴" if row["risk"]=="HIGH" else "🟡" if row["risk"]=="MODERATE" else "🟢"

        with st.expander(f"**{row['id']}** · {row['name']} · {row['county']} · {ri} {row['risk']} · {row['status']}"):

            # ── CONNECTION 6: PATIENT JOURNEY TIMELINE ─────────────────────
            journey = row.get("journey") if isinstance(row.get("journey"), list) else []
            if journey:
                st.markdown("#### 🗺️ Patient Journey")
                st.markdown('<div class="tl-wrap">', unsafe_allow_html=True)
                for jstep in journey:
                    if jstep.get("urgent") and not jstep.get("done"):
                        dot_class = "tl-dot tl-urgent"
                    elif jstep.get("done"):
                        dot_class = "tl-dot tl-done"
                    else:
                        dot_class = "tl-dot tl-pending"
                    status_icon = "✅" if jstep.get("done") else ("🚨" if jstep.get("urgent") else "⏳")
                    st.markdown(f"""
                    <div class="tl-step">
                      <div class="{dot_class}"></div>
                      <div>
                        <div class="tl-label">{status_icon} {jstep["step"]}</div>
                        <div class="tl-sub">{jstep["ts"]} · {jstep["detail"]}</div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            # Patient details
            ec1,ec2,ec3 = st.columns(3)
            ec1.markdown(f"**Age:** {row['age']}  \n**Facility:** {row['facility']}")
            ec2.markdown(f"**Practitioner:** {row['practitioner']}  \n**Referral:** {row['referral']}")
            ec3.markdown(f"**Next Due:** `{row['next_due']}`  \n**{due_txt}**")
            st.markdown(f"**Notes:** {row['notes']}")
            st.markdown("")

            # Action buttons
            a1,a2,a3 = st.columns(3)
            if a1.button("✅ Mark Done",         key=f"done_{row['id']}"):
                for i,p in enumerate(st.session_state.patients):
                    if p["id"]==row["id"]:
                        st.session_state.patients[i]["status"]="Done"
                        if "journey" not in st.session_state.patients[i]:
                            st.session_state.patients[i]["journey"]=[]
                        st.session_state.patients[i]["journey"].append({
                            "step":"Follow-Up Completed","ts":datetime.today().strftime("%d %b %Y"),
                            "detail":"Marked done by practitioner","done":True,
                        })
                st.rerun()

            if a2.button("📅 Reschedule +2 wks", key=f"rs_{row['id']}"):
                nd = (datetime.today()+timedelta(weeks=2)).strftime("%Y-%m-%d")
                for i,p in enumerate(st.session_state.patients):
                    if p["id"]==row["id"]:
                        st.session_state.patients[i]["next_due"]=nd
                        st.session_state.patients[i]["status"]="Scheduled"
                st.rerun()

            if a3.button("🚨 Flag Urgent",        key=f"urg_{row['id']}"):
                for i,p in enumerate(st.session_state.patients):
                    if p["id"]==row["id"]:
                        st.session_state.patients[i]["status"]="Urgent"
                        st.session_state.patients[i]["risk"]="HIGH"
                st.rerun()

            # ── CONNECTION 4: Re-Assessment button ─────────────────────────
            st.markdown("""
            <div class="conn-flow">
              🔗 Follow-up due? <span>Start Re-Assessment</span> —
              patient details pre-filled, only update what has changed.
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"🩺 Start Re-Assessment for {row['name']}", key=f"reassess_{row['id']}"):
                st.session_state.reassess_patient = {
                    "name":       row["name"],
                    "age":        row["age"],
                    "county":     row["county"],
                    "facility":   row["facility"],
                    "practitioner":row["practitioner"],
                    "risk":       row["risk"],
                    "last_seen":  row["next_due"],
                }
                st.session_state.active_patient = {
                    "name":row["name"],"age":row["age"],"county":row["county"],
                    "facility":row["facility"],"practitioner":row["practitioner"],
                    "risk":row["risk"],"id":row["id"],
                }
                st.session_state.grace_demo = False
                st.session_state["_nav_radio"] = "🩺  Risk Assessment"
                st.rerun()

    # Add patient manually
    st.markdown("---")
    st.markdown("### ➕ Add Patient Manually")
    with st.form("add_pt"):
        nc1,nc2,nc3 = st.columns(3)
        np_name  = nc1.text_input("Patient Name")
        np_age   = nc1.number_input("Age",18,90,35)
        np_county= nc2.selectbox("County",["Nairobi","Mombasa","Kisumu","Kiambu","Nakuru","Uasin Gishu","Homa Bay","Other"])
        np_prac  = nc2.text_input("Practitioner")
        np_risk  = nc3.selectbox("Risk Level",["LOW","MODERATE","HIGH"])
        np_ref   = nc3.selectbox("Referral",  ["Education","Routine","Imaging","Urgent"])
        np_notes = st.text_area("Clinical Notes",height=68)
        np_due   = st.date_input("Next Follow-Up Date",datetime.today()+timedelta(days=14))
        if st.form_submit_button("➕ Add Patient",use_container_width=True) and np_name:
            st.session_state.patients.append({
                "id":f"PT-{len(st.session_state.patients)+1:03d}",
                "name":np_name,"age":np_age,"county":np_county,
                "facility":"—","practitioner":np_prac,
                "risk":np_risk,"referral":np_ref,
                "next_due":np_due.strftime("%Y-%m-%d"),
                "status":"Scheduled","notes":np_notes,
                "journey":[{"step":"Manually Added","ts":datetime.today().strftime("%d %b %Y"),
                             "detail":"Added via Follow-Up Tracker","done":True}],
            })
            st.success(f"✅ {np_name} added.")
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 5 — ANALYTICS DASHBOARD (CONNECTION 5: live session data)
# ══════════════════════════════════════════════════════════════════════════════
elif "Analytics" in module:
    st.markdown('<div class="section-head">📊 Administrator Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Live data from this session · Every assessment, referral and follow-up reflected in real time</div>', unsafe_allow_html=True)

    # ── CONNECTION 5: analytics pulls from live session data ──────────────
    df_s = st.session_state.screenings.copy()
    df_p = pd.DataFrame(st.session_state.patients)

    live_count = len(df_s[df_s["date"]==datetime.today().strftime("%Y-%m-%d")])
    if live_count:
        st.markdown(f"""
        <div class="conn-flow">
          📡 <span>Live session:</span> {live_count} new screening(s) added today
          from Risk Assessment and Referral Intelligence — reflected in all charts below.
        </div>
        """, unsafe_allow_html=True)

    fc1,fc2 = st.columns(2)
    cf = fc1.selectbox("County",  ["All"]+sorted(df_s["county"].unique()))
    ff = fc2.selectbox("Facility",["All"]+sorted(df_s["facility"].unique()))
    if cf!="All": df_s = df_s[df_s["county"]  ==cf]
    if ff!="All": df_s = df_s[df_s["facility"]==ff]

    n_screen    = len(df_s)
    n_urgent    = len(df_s[df_s["risk"]=="HIGH"])
    pct_fu      = round(df_s["followed_up"].mean()*100,1) if len(df_s) else 0
    n_overdue_p = len(df_p[df_p["status"]=="Overdue"])

    t1,t2,t3,t4 = st.columns(4)
    for col,val,lbl,clr in [
        (t1,n_screen,       "Screenings (90 days)","#6a1b9a"),
        (t2,n_urgent,       "High-Risk Cases",     "#e53935"),
        (t3,f"{pct_fu}%",   "Follow-Up Rate",      "#f57c00"),
        (t4,n_overdue_p,    "Overdue Follow-Ups",  "#1565c0"),
    ]:
        col.markdown(f"""<div class="mtile" style="border-top-color:{clr};">
          <h2 style="color:{clr};">{val}</h2><p>{lbl}</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    month_order = sorted(df_s["month"].unique(), key=lambda m: datetime.strptime(m,"%b %Y"))
    trend = df_s.groupby("month").size().reset_index(name="Screenings")
    trend["month"] = pd.Categorical(trend["month"], categories=month_order, ordered=True)
    trend = trend.sort_values("month")
    fig = px.line(trend,x="month",y="Screenings",markers=True,
                  template="plotly_white",title="📈 Screenings Over Time",
                  color_discrete_sequence=["#6a1b9a"])
    fig.update_traces(line_width=3,marker_size=8)
    fig.update_layout(font_family="Nunito")
    st.plotly_chart(fig, use_container_width=True)

    cl,cr = st.columns(2)
    with cl:
        cnt = df_s.groupby("county").size().reset_index(name="Screenings").sort_values("Screenings")
        fig = px.bar(cnt,x="Screenings",y="county",orientation="h",
                     color_discrete_sequence=["#7b1fa2"],
                     template="plotly_white",title="🗺️ Screenings by County")
        fig.update_layout(font_family="Nunito")
        st.plotly_chart(fig, use_container_width=True)
    with cr:
        rc = df_s["referral"].value_counts().reset_index()
        rc.columns=["Referral","Count"]
        fig = px.pie(rc,names="Referral",values="Count",color="Referral",
                     color_discrete_map={"Urgent":"#e53935","Imaging":"#1565c0",
                                         "Routine":"#f57c00","Education":"#2e7d32"},
                     template="plotly_white",title="🔀 Referral Breakdown")
        fig.update_layout(font_family="Nunito")
        st.plotly_chart(fig, use_container_width=True)

    cl2,cr2 = st.columns(2)
    with cl2:
        fc_cnt = df_s.groupby("facility").size().reset_index(name="Screenings")
        fig = px.bar(fc_cnt,x="facility",y="Screenings",
                     color_discrete_sequence=["#1565c0"],
                     template="plotly_white",title="🏥 Screenings by Facility")
        fig.update_layout(xaxis_tickangle=-20,font_family="Nunito")
        st.plotly_chart(fig, use_container_width=True)
    with cr2:
        fu = df_s.groupby("county")["followed_up"].mean().mul(100).round(1).reset_index()
        fu.columns=["County","Follow-Up Rate (%)"]
        fig = px.bar(fu.sort_values("Follow-Up Rate (%)"),
                     x="Follow-Up Rate (%)",y="County",orientation="h",
                     color="Follow-Up Rate (%)",
                     color_continuous_scale=["#e53935","#f57c00","#2e7d32"],
                     template="plotly_white",title="📋 Follow-Up Compliance by County")
        if len(df_s): fig.add_vline(x=pct_fu,line_dash="dash",line_color="#6a1b9a",annotation_text="Avg")
        fig.update_layout(font_family="Nunito")
        st.plotly_chart(fig, use_container_width=True)

    rp = df_s.groupby(["profession","risk"]).size().reset_index(name="Count")
    fig = px.bar(rp,x="profession",y="Count",color="risk",
                 color_discrete_map={"HIGH":"#e53935","MODERATE":"#f57c00","LOW":"#2e7d32"},
                 template="plotly_white",barmode="stack",
                 title="⚕️ Risk Distribution by Profession")
    fig.update_layout(xaxis_tickangle=-20,font_family="Nunito")
    st.plotly_chart(fig, use_container_width=True)

    overdue = df_p[df_p["status"]=="Overdue"].sort_values("next_due")
    if not overdue.empty:
        st.markdown("### 🚨 Overdue Follow-Ups")
        st.error(f"**{len(overdue)} patient(s) have missed their follow-up.** Immediate action required.")
        st.dataframe(
            overdue[["id","name","county","facility","risk","referral","next_due","practitioner","notes"]]
            .reset_index(drop=True), use_container_width=True)
    else:
        st.success("✅ No overdue follow-ups at this time.")

    st.markdown("---")
    csv = df_s.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export Screening Data (CSV)",data=csv,
                       file_name="breastcare_kenya_screenings.csv",mime="text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 6 — AI ASSISTANT CHATBOT (fully offline, no API key required)
# ══════════════════════════════════════════════════════════════════════════════
elif "AI Assistant Chatbot" in module:
    st.markdown('<div class="section-head">🤖 AI Assistant Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Clinical Q&A · Generate patient summaries & referral letters · BSE in Swahili · Kenya-specific guidance — no internet needed</div>', unsafe_allow_html=True)

    # ── Knowledge base ──────────────────────────────────────────────────────
    KB = {
        # RISK FACTORS
        "risk_score": {
            "keys": ["score","risk score","what does my score","interpret","points","calculate","scoring"],
            "answer": """**📊 Understanding Your Risk Score**

The score runs from **0–100** based on clinical signs, history, and demographics:

| Score | Risk Level | Action |
|-------|-----------|--------|
| ≥ 50 (or red flags*) | 🔴 HIGH | Urgent referral — same day |
| 25–49 | 🟠 MODERATE | Routine referral + imaging |
| < 25  | 🟢 LOW | Education + annual screening |

**⚠️ Instant HIGH regardless of score if:**
- Ulceration present
- Lump + axillary nodes
- Lump + skin changes

*The score is a decision support tool — always apply clinical judgement.*"""
        },
        "lump": {
            "keys": ["lump","mass","palpable","swelling in breast"],
            "answer": """**🔍 Breast Lump — What to Know**

A palpable breast lump adds **+20 points** to the risk score.

**Concerning features (refer urgently if present):**
- Hard, irregular, fixed lump
- Lump + skin dimpling or thickening
- Lump + axillary lymph nodes (adds +30 pts — instant HIGH)
- Lump that has grown quickly

**Less concerning (but still document):**
- Soft, mobile, round — may be a cyst or fibroadenoma
- Cyclical tenderness with lump

**Action:** Any lump in a woman ≥35 warrants clinical breast examination and imaging referral even if score is moderate."""
        },
        "nipple": {
            "keys": ["nipple discharge","nipple inversion","nipple","discharge"],
            "answer": """**🔴 Nipple Changes — Clinical Guide**

| Sign | Points | Notes |
|------|--------|-------|
| Nipple discharge | +15 | Especially if bloody or unilateral |
| Nipple inversion (new) | +20 | Long-standing inversion is less concerning |

**Refer urgently if discharge is:**
- Bloody or blood-stained
- Unilateral and spontaneous
- From a single duct

Bilateral milky discharge in non-breastfeeding women → consider prolactinoma (endocrine referral)."""
        },
        "skin_changes": {
            "keys": ["skin","peau d'orange","dimpling","redness","erythema","skin changes","orange peel"],
            "answer": """**🟠 Skin Changes — Red Flag Signs**

Skin changes add **+25 points** and combined with a lump → instant **HIGH RISK**.

**What to look for:**
- *Peau d'orange* (orange-peel texture) — classic inflammatory BC sign
- Dimpling or puckering
- Redness or warmth over breast (may suggest inflammatory BC)
- Ulceration (+40 pts — single highest-scoring sign)
- Thickening of skin

**Ulceration = automatic HIGH RISK referral regardless of other findings.**"""
        },
        "axillary": {
            "keys": ["axillary","lymph node","armpit","lymph","nodes"],
            "answer": """**⚠️ Axillary Lymphadenopathy**

Axillary lymph nodes add **+30 points** — one of the highest individual scores.

- Lump + axillary nodes = **automatic HIGH RISK**
- Suggests possible regional spread
- Document: size, mobility, tenderness, number

This warrants same-day or next-day urgent oncology referral."""
        },
        "family_history": {
            "keys": ["family history","brca","genetic","mother","sister","hereditary","relative"],
            "answer": """**🧬 Family History & Genetic Risk**

| History | Points |
|---------|--------|
| 2+ relatives or BRCA known | +25 |
| 1st-degree relative (mother/sister) | +15 |
| No family history | 0 |

**BRCA1/BRCA2 in Kenya:**
Testing is limited to major referral hospitals (KNH, Aga Khan). Counsel patients with strong family history about:
- Increased lifetime risk (up to 85% with BRCA1)
- Earlier screening start age (35 or 10 yrs before youngest affected relative)
- Bilateral risk

In resource-limited settings, a strong family history alone is sufficient grounds for enhanced surveillance."""
        },
        "menopause": {
            "keys": ["menopause","postmenopausal","post-menopausal","menopausal","menstrual"],
            "answer": """**🔵 Menopause & Breast Cancer Risk**

| Status | Points |
|--------|--------|
| Post-menopausal > 5 years | +15 |
| Post-menopausal < 5 years | +8 |
| Pre-menopausal | 0 |

Post-menopausal women have higher risk because:
- Prolonged estrogen exposure over lifetime
- Adipose tissue becomes main estrogen source after menopause
- Breast changes are harder to detect (denser → fatty tissue)

**Recommend annual clinical breast exam** for all post-menopausal women."""
        },
        "hrt": {
            "keys": ["hrt","hormone","hormone replacement","combined pill","ocp","oral contraceptive"],
            "answer": """**💊 Hormones & Breast Cancer Risk**

- **HRT (combined)** adds +8 points — use >5 years increases risk ~26%
- **OCP** — small increased risk, returns to baseline ~10 yrs after stopping
- **Progestogen-only** — lower risk than combined preparations

**Counsel patients:**
- Benefits of HRT (bone, cardiovascular, quality of life) vs risk
- Encourage shortest effective duration
- Regular breast screening during use

Kenya guidance: Refer to *KOGS guidelines* for menopausal management."""
        },
        "breastfeeding": {
            "keys": ["breastfeed","breastfeeding","breast feed","lactation","nursing"],
            "answer": """**🍼 Breastfeeding — A Protective Factor**

Breastfeeding **reduces** the risk score by **−8 points**.

**Why it's protective:**
- Delays return of ovulation (less lifetime estrogen exposure)
- Promotes differentiation of breast cells
- Each year of breastfeeding reduces risk ~4.3%

**Encourage breastfeeding as part of breast health education.**
This is particularly important messaging in Kenyan community health education programmes."""
        },
        "referral": {
            "keys": ["referral","refer","where to send","which hospital","when to refer","refer urgent","routine referral"],
            "answer": """**🔀 Referral Decision Guide**

| Category | Trigger | Action |
|----------|---------|--------|
| 🔴 URGENT | HIGH risk, ulceration, lump+nodes | Same-day / next-day specialist |
| 🟠 ROUTINE | MODERATE risk, no red flags | Within 2 weeks |
| 🔵 IMAGING | MODERATE risk, focal finding | Mammogram/USS — 2–4 weeks |
| 🟢 EDUCATION | LOW risk | BSE teaching, annual review |

**Kenya referral pathway:**
Dispensary/Health Centre → Sub-County Hospital → County Hospital → National Referral (KNH, Moi Teaching, Coast General)

Always **call ahead** for urgent referrals and document the receiving clinician's name."""
        },
        "follow_up": {
            "keys": ["follow up","follow-up","tracker","overdue","when to follow","next appointment","schedule"],
            "answer": """**📋 Follow-Up Protocols**

| Risk | Follow-up Interval |
|------|--------------------|
| HIGH | 1–2 weeks post-referral |
| MODERATE | 2–4 weeks |
| LOW | 3–6 months / annually |

**Overdue patients (in Follow-Up Tracker):**
- Marked in red — contact immediately
- Document reason for missed appointment
- Escalate if no response within 48 hours for HIGH risk

**The Follow-Up Tracker** in this app auto-flags overdue patients and lets you start a re-assessment in one click."""
        },
        "screening": {
            "keys": ["screening","mammogram","ultrasound","bse","breast self exam","cbe","clinical breast","imaging"],
            "answer": """**🔬 Breast Screening in Kenya**

**Self-Examination (BSE):**
- Monthly, 7–10 days after period starts
- Post-menopausal: same date each month
- Teach all women from age 20

**Clinical Breast Exam (CBE):**
- Every 1–3 years, age 20–39
- Annually from age 40

**Mammography:**
- Recommended annually from age 40–50 (varies by risk)
- Limited availability in Kenya — major counties have access
- Ultrasound often used as primary imaging modality

**Barriers in Kenya (KAP literature 2013–2024):**
- Low awareness (key target for community health workers)
- Cost and distance
- Cultural beliefs and stigma
- Fear of diagnosis"""
        },
        "incidence": {
            "keys": ["incidence","statistics","prevalence","how common","kenya breast cancer","rate","burden","epidemiology"],
            "answer": """**📈 Breast Cancer in Kenya — Key Facts**

- Most common female cancer in Kenya (overtook cervical cancer ~2019)
- ~6,800 new cases per year (estimated)
- Mortality rate ~50% — largely due to late-stage presentation
- Median age at diagnosis: **~47 years** (younger than Western populations)
- **>60%** present at Stage III or IV

**Why late presentation?**
- Limited screening infrastructure
- Low awareness of early signs
- Cultural / stigma barriers
- Health-seeking behaviour delays

**This app directly addresses** the knowledge and practice gap identified in Kenyan KAP studies."""
        },
        "stages": {
            "keys": ["stage","stages","staging","stage i","stage ii","stage iii","stage iv","metastatic"],
            "answer": """**🎗️ Breast Cancer Stages**

| Stage | Description | 5-yr Survival (approx.) |
|-------|-------------|------------------------|
| I | Tumour ≤2 cm, no nodes | ~99% |
| II | Larger tumour or 1–3 nodes | ~86% |
| III | Locally advanced, skin/chest wall | ~57% |
| IV | Metastatic | ~28% |

**In Kenya, most women present at Stage III/IV.** This app aims to push detection toward Stage I/II through earlier clinical identification and timely referral."""
        },
        "how_to_use": {
            "keys": ["how to use","how do i","guide","tutorial","navigation","modules","what can this app","app guide","getting started"],
            "answer": """**📱 How to Use BreastCare Kenya**

The app has 5 clinical modules + this AI assistant:

1. **🩺 Risk Assessment** — Complete the patient form; the risk score calculates instantly. Patient data flows to all modules automatically.

2. **✅ Screening Checklist** — Step-by-step symptom checklist; auto-fills from the Risk Assessment.

3. **🔔 Follow-Up Tracker** — Manage patient follow-ups, flag overdue cases, start re-assessments.

4. **🔀 Referral Intelligence** — Evidence-based referral decisions with pathway guidance.

5. **📊 Analytics Dashboard** — Real-time stats across facilities, counties, and risk levels.

**Pro tip:** Use the *Grace Wanjiku demo* in Risk Assessment to see all 6 modules connected in a live walkthrough!"""
        },
        "grace": {
            "keys": ["grace","grace wanjiku","demo","example patient","sample case"],
            "answer": """**👩🏾 Grace Wanjiku — Demo Case**

Grace is the built-in demo patient:
- Age 42, Nairobi, presented with a palpable lump
- Risk score: **75 → HIGH RISK**
- 3 red flags detected on checklist
- Urgent oncology referral generated
- Currently **overdue** for follow-up in the tracker

**To try her case:**
Go to 🩺 Risk Assessment → click *"🚀 Pre-fill Grace's Case"* in the demo expander.

This shows the full connected workflow: assessment → checklist → referral → follow-up tracker."""
        },
        "treatment": {
            "keys": ["treatment","chemo","chemotherapy","surgery","mastectomy","radiation","radiotherapy","tamoxifen","trastuzumab"],
            "answer": """**💊 Breast Cancer Treatment Overview**

*(This app supports early detection, not treatment planning — always refer to oncology)*

**Standard modalities:**
- **Surgery:** Lumpectomy or mastectomy depending on stage/size
- **Chemotherapy:** Neo-adjuvant (before surgery) or adjuvant
- **Radiotherapy:** Post-lumpectomy standard; post-mastectomy if nodes involved
- **Hormonal therapy:** Tamoxifen (pre-menopausal ER+), aromatase inhibitors (post-menopausal)
- **Targeted therapy:** Trastuzumab (Herceptin) for HER2+ — limited availability in Kenya

**Kenya treatment access:**
- KNH, Moi Teaching, Coast General, and a few private facilities offer oncology
- NHIF covers some cancer treatments — encourage patients to check coverage

For treatment queries, refer to **Kenya National Cancer Treatment Protocols (KEMRI/MOH)**."""
        },
        "bse": {
            "keys": ["bse technique","how to do bse","self examination","self-exam","teach patient"],
            "answer": """**🤲 Teaching Breast Self-Examination (BSE)**

**When:** Monthly — 7–10 days after first day of period (pre-menopausal). Same date each month (post-menopausal).

**Steps to teach:**
1. **Stand before mirror** — look for any visible changes, asymmetry, dimpling
2. **Raise arms overhead** — check for changes in shape or skin
3. **Lie down** — place right hand under head; use left fingers to examine right breast in circular pattern
4. **Systematic pattern** — small circles, covering entire breast from armpit to sternum, collarbone to bottom
5. **Feel for lumps** — any new mass, thickening, or hard knot
6. **Check nipple** — gently squeeze; note any discharge
7. **Repeat** on opposite side

**Document and report any new change to a health worker immediately.**"""
        },
    }

    # ── Quick action buttons ────────────────────────────────────────────────
    QUICK_ACTIONS = [
        ("📋 Summarise last patient",  "summarise last patient assessed"),
        ("📝 Draft referral letter",   "draft referral letter for last patient"),
        ("🇰🇪 BSE in Swahili",          "explain BSE in Swahili / Kiswahili"),
        ("📊 Interpret analytics",     "interpret analytics and screening statistics"),
    ]

    QUICK_CHIPS = [
        "What does a HIGH risk score mean?",
        "When should I refer urgently?",
        "How to teach BSE to a patient?",
        "What are the breast cancer stages?",
        "Breast cancer statistics in Kenya",
        "What are WHO screening guidelines?",
        "What does peau d'orange mean?",
        "Referral pathways in Kenya",
    ]

    # ── Clinical generators (no API needed) ─────────────────────────────────
    def _make_clinical_summary(ctx):
        name, age, risk, score = ctx["name"], ctx["age"], ctx["risk"], ctx["score"]
        referral, symptoms = ctx["referral"], ctx["symptoms"]
        rf, facility, county = ctx["risk_factors"], ctx["facility"], ctx["county"]
        urgency = {"HIGH": ("requires urgent clinical attention", "same-day"),
                   "MODERATE": ("warrants prompt investigation", "within 2 weeks"),
                   "LOW": ("is currently low risk", "at annual review")}
        phrase, timeframe = urgency[risk]
        symp_line = f"presenting with {symptoms}" if symptoms != "No acute red flags" else "with no acute presenting symptoms"
        rf_line = f"Background risk factors include {rf}." if rf != "none documented" else "No significant background risk factors documented."
        ref_line = {
            "Urgent":    "She has been triaged for an URGENT referral and must be seen by an oncology or surgical unit today. Do not send her home without this referral actioned.",
            "Imaging":   "A mammogram or breast ultrasound has been requested and should be completed within 14 days. Ensure the imaging request is given to the patient before she leaves.",
            "Routine":   "A routine follow-up appointment has been scheduled. Educate the patient on breast self-examination before discharge.",
            "Education": "No clinical referral is required at this time. Provide BSE education and schedule an annual screening.",
        }.get(referral, ctx.get("ref_action",""))
        return (
            f"**Clinical Handover — {name}, Age {age} | {facility}, {county}**\n\n"
            f"{name} is a {age}-year-old patient {symp_line}. "
            f"Her risk score is **{score}/100**, placing her in the **{risk} RISK** category — this {phrase}. "
            f"{rf_line} {ref_line}\n\n"
            f"*Next action due: {timeframe}. Practitioner to confirm patient has understood and accepted the care plan.*"
        )

    def _make_referral_letter(ctx):
        today_str = datetime.today().strftime("%d %B %Y")
        name, age, symptoms = ctx["name"], ctx["age"], ctx["symptoms"]
        risk, facility, county, rf = ctx["risk"], ctx["facility"], ctx["county"], ctx["risk_factors"]
        urgency_label = {"HIGH":"URGENT — SAME DAY","MODERATE":"SEMI-URGENT — WITHIN 2 WEEKS","LOW":"ROUTINE"}.get(risk,"ROUTINE")
        return (
            f"**REFERRAL LETTER**\n\n"
            f"**Date:** {today_str}\n**From:** {facility}, {county} County\n"
            f"**To:** Oncology / Breast Surgery Unit\n**Priority:** {urgency_label}\n\n---\n\n"
            f"Dear Colleague,\n\nI am referring **{name}**, a **{age}-year-old** patient, for specialist review of suspected breast pathology. "
            f"The patient presented with {symptoms if symptoms != 'No acute red flags' else 'symptoms requiring further assessment'}. "
            f"{'Background risk factors include: ' + rf + '. ' if rf != 'none documented' else ''}"
            f"Clinical assessment returned a **{risk} RISK** result, indicating specialist evaluation is warranted {urgency_label.lower()}.\n\n"
            f"Please review and advise on further management.\n\nYours faithfully,\n[Practitioner Name]\n[Designation] — {facility}\n[Phone / NHIF No.]"
        )

    BSE_SWAHILI = """**Jinsi ya Kujifanyia Uchunguzi wa Matiti Nyumbani (BSE)**
*Fanya hivi kila mwezi, siku 7–10 baada ya hedhi yako*

**Hatua ya 1 — Angalia Mbele ya Kioo 👁️**
Simama mbele ya kioo, mikono upande. Tazama matiti yote mawili. Angalia kama kuna tofauti ya umbo, rangi ya ngozi, au chuchu.

**Hatua ya 2 — Inua Mikono Juu 🙌**
Inua mikono juu ya kichwa. Angalia kama kuna msukosuko wa ngozi au chuchu inavyovutwa ndani.

**Hatua ya 3 — Palpation — Lala Chini 🛏️**
Lala chini, weka mto chini ya bega la kulia. Tumia vidole vitatu vya mkono wa kushoto kupapasa titi la kulia kwa mzunguko mdogo mdogo. Rudia upande wa pili.

**Hatua ya 4 — Angalia Chuchu 🔍**
Kwa upole bonyeza chuchu. Kama kuna maji yanayotoka (si maziwa), au maumivu, nenda hospitali haraka.

**Hatua ya 5 — Palpation Ukiwa Umesimama 🚿**
Unaweza kufanya hivi ukiwa kwenye bafu. Tumia mkono mmoja kupapasa titi lingine.

⚠️ **Nenda Hospitali Mara Moja Ukiona:** Uvimbe wowote mpya · Ngozi inayokauka · Chuchu inavyovutwa ndani · Maumivu yanayoendelea"""

    def _analytics_summary():
        df_s = st.session_state.screenings
        n = len(df_s); hi = len(df_s[df_s["risk"]=="HIGH"])
        fu = round(df_s["followed_up"].mean()*100, 1)
        pct_hi = round(hi/n*100, 1)
        top_c = df_s["county"].value_counts().idxmax()
        low_fu = df_s.groupby("county")["followed_up"].mean().mul(100).round(1).idxmin()
        concern = "below the 60% WHO minimum threshold" if fu < 60 else "meeting the WHO minimum threshold"
        return (
            f"**Analytics Interpretation**\n\n"
            f"Over the last 90 days, **{n} screenings** have been recorded. "
            f"**{hi} ({pct_hi}%) are HIGH RISK** — each requires urgent action if not yet referred.\n\n"
            f"**Follow-up compliance is {fu}%**, which is {concern}. "
            f"**{low_fu}** county has the lowest compliance — prioritise for supervisory visit.\n\n"
            f"**{top_c}** has the highest screening volume.\n\n"
            f"**Recommended actions:**\n"
            f"1. Contact practitioners in {low_fu} to understand follow-up barriers\n"
            f"2. Review all HIGH RISK cases to confirm referral completion\n"
            f"3. Consider CHW outreach in lower-performing counties\n"
            f"4. Export CSV and share with County Director of Health monthly"
        )

    def chatbot_respond(user_msg):
        """Enhanced chatbot: smart generators + comprehensive KB matching."""
        msg = user_msg.lower()
        ctx = st.session_state.get("active_patient", {})
        ap_prefix = f"*(Active patient: **{ctx['name']}** — {ctx.get('risk','')} RISK)*\n\n" if ctx.get("name") and ctx.get("risk") else ""

        # ── Smart generators ─────────────────────────────────────────────────
        if any(w in msg for w in ["summarise","summarize","handover","summary","last patient"]):
            if ctx and ctx.get("score"):
                return _make_clinical_summary(ctx)
            return "No patient has been assessed yet this session. Please go to **🩺 Risk Assessment**, run a case, then come back."

        if ("referral" in msg and "letter" in msg) or "draft referral" in msg:
            if ctx and ctx.get("score"):
                return _make_referral_letter(ctx)
            return "No patient is loaded yet. Please complete a risk assessment first, then ask for the referral letter again."

        if "swahili" in msg or "kiswahili" in msg or ("bse" in msg and "swahili" in msg):
            return BSE_SWAHILI

        if any(w in msg for w in ["analytics","interpret","screening data","compliance","statistics"]):
            return _analytics_summary()

        # ── KB matching ──────────────────────────────────────────────────────
        for entry in KB.values():
            if any(kw in msg for kw in entry["keys"]):
                return ap_prefix + entry["answer"]

        # ── Extra direct matches from new KB ────────────────────────────────
        if "peau" in msg or "orange peel" in msg or "orange" in msg and "skin" in msg:
            return ap_prefix + KB["skin_changes"]["answer"]
        if "who" in msg and any(w in msg for w in ["guideline","recommendation","standard","protocol"]):
            return ap_prefix + """**WHO / IARC Breast Cancer Screening Guidelines (Low-Resource Settings)**

For countries like Kenya with limited mammography infrastructure, WHO recommends:

**1. Clinical Breast Examination (CBE)** as the primary screening tool — this is what BreastCare Kenya is built around.

**2. Target age:** Women aged 40–69 as priority; screen from 25 if high-risk.

**3. Frequency:** Every 1–2 years for average risk; annually for high risk.

**4. CBE by trained health workers** (nurses, clinical officers, CHWs) is considered effective and feasible where radiological screening is unavailable.

**5. Mammography** remains the gold standard but requires infrastructure; ultrasound is preferred for women under 40 or with dense breasts.

*Source: WHO Guide to Cancer Early Diagnosis (2017) & IARC Handbooks Vol. 15*"""

        if "pathway" in msg or ("where" in msg and "refer" in msg) or ("which hospital" in msg):
            return ap_prefix + """**Kenya Breast Cancer Referral Pathways**

**Level 2–3 (Dispensary / Health Centre):** Initial screening and risk assessment → refer to Level 4 for imaging.

**Level 4 (Sub-county Hospital):** Can order mammography or ultrasound. Refer biopsy-required or HIGH RISK cases upward.

**Level 5–6 (County / National Referral):**
- **Kenyatta National Hospital (KNH)** — Nairobi
- **Moi Teaching & Referral Hospital** — Eldoret (Rift Valley)
- **Coast General Hospital** — Mombasa
- **Kisumu County Referral** — Nyanza

**NHIF coverage:** Breast cancer treatment is covered under NHIF's chronic illness package. Advise patients to bring their NHIF card to every appointment."""

        # ── Greetings / social ───────────────────────────────────────────────
        if any(w in msg for w in ["hello","hi","hey","good morning","good afternoon","habari","jambo"]):
            return "Habari! 👋 Welcome to BreastCare AI Assistant. I'm here to support your clinical work.\n\nAsk me anything, tap a quick question, or use the action buttons above."
        if any(w in msg for w in ["thank","asante","thanks","asante sana"]):
            return "Karibu sana! 🎗️ Happy to help. Anything else you'd like to know?"
        if any(w in msg for w in ["symptoms","signs","red flag","warning sign"]):
            return ap_prefix + KB["lump"]["answer"] + "\n\n---\n" + KB["skin_changes"]["answer"]

        # ── Fallback ─────────────────────────────────────────────────────────
        return (
            "I can help with clinical questions about breast cancer screening, risk, and referrals in Kenya.\n\n"
            "**Try asking about:**\n"
            "- Risk score interpretation · BSE technique · Nipple discharge · Skin changes\n"
            "- Family history & BRCA · Staging · WHO guidelines · Menopause & HRT\n"
            "- Kenya referral pathways · Follow-up protocols\n\n"
            "Or use the **Quick Actions** above to generate a clinical summary, referral letter, or Swahili BSE guide."
        )

    # ── UI ──────────────────────────────────────────────────────────────────
    # Active patient context banner
    ap = st.session_state.get("active_patient", {})
    if ap.get("name"):
        risk_col = "#e53935" if ap.get("risk")=="HIGH" else "#f57c00" if ap.get("risk")=="MODERATE" else "#2e7d32"
        st.markdown(f"""
        <div class="conn-flow">
          👩🏾 Active patient: <span>{ap['name']}</span> ·
          Risk: <span style="color:{risk_col};">{ap.get('risk','—')}</span> ·
          I can answer questions specific to this patient's care pathway.
        </div>
        """, unsafe_allow_html=True)

    # ── Quick action buttons ─────────────────────────────────────────────────
    st.markdown("**⚡ Quick Actions**")
    qa_cols = st.columns(4)
    for col, (label, prompt) in zip(qa_cols, QUICK_ACTIONS):
        if col.button(label, use_container_width=True, key=f"qa_{label}"):
            st.session_state.chat_history.append({"role":"user","text":label})
            reply = chatbot_respond(prompt)
            st.session_state.chat_history.append({"role":"bot","text":reply})
            st.rerun()

    st.markdown("---")

    # Chat history display
    chat_html = '<div class="chat-wrap" id="chat-wrap">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "bot":
            chat_html += f'''<div class="chat-msg bot">
                <div class="chat-avatar bot">🤖</div>
                <div class="chat-bubble bot">{msg["text"].replace(chr(10), "<br>")}</div>
            </div>'''
        else:
            chat_html += f'''<div class="chat-msg user">
                <div class="chat-avatar user">👩🏾</div>
                <div class="chat-bubble user">{msg["text"]}</div>
            </div>'''
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Quick chip buttons
    st.markdown("**💬 Quick questions:**")
    chip_cols = st.columns(3)
    for i, chip in enumerate(QUICK_CHIPS):
        if chip_cols[i % 3].button(chip, key=f"chip_{i}", use_container_width=True):
            st.session_state.chat_history.append({"role":"user","text":chip})
            reply = chatbot_respond(chip)
            st.session_state.chat_history.append({"role":"bot","text":reply})
            st.rerun()

    st.markdown("---")

    # Text input
    col_inp, col_btn = st.columns([5, 1])
    user_input = col_inp.text_input(
        "Type your question…",
        placeholder="e.g. When should I refer a patient urgently?",
        label_visibility="collapsed",
        key="chat_input",
    )
    send = col_btn.button("Send ➤", use_container_width=True)

    if send and user_input.strip():
        q = user_input.strip()
        st.session_state.chat_history.append({"role":"user","text":q})
        reply = chatbot_respond(q)
        st.session_state.chat_history.append({"role":"bot","text":reply})
        st.rerun()

    # Clear chat button
    if st.button("🗑️ Clear conversation", use_container_width=False):
        st.session_state.chat_history = [
            {"role":"bot","text":"Chat cleared. How can I help you? Ask me about risk scores, referrals, screening, follow-up protocols, or how to use the app."}
        ]
        st.rerun()