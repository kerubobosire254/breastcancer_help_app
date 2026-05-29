"""
BreastCare Kenya — Clinical Decision Support Platform
Streamlit App | 5 Modules:
  1. Quick Risk Assessment
  2. Screening Checklist
  3. Smart Follow-Up System
  4. Referral Intelligence
  5. Analytics Dashboard

Run: streamlit run breast_cancer_kap_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BreastCare Kenya",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0a2e 0%, #2d1054 60%, #4a1068 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * { color: #f0e6ff !important; }
section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 10px 14px;
    margin: 3px 0;
    display: block;
    transition: background 0.2s;
    cursor: pointer;
    font-weight: 500;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.14);
}

/* ── Main background ── */
.main { background: #faf7ff; }

/* ── Cards ── */
.kcard {
    background: white;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 16px rgba(74,16,104,0.08);
    margin-bottom: 1rem;
    border-left: 5px solid #9c27b0;
}
.kcard.red    { border-color: #e53935; background: #fff5f5; }
.kcard.orange { border-color: #f57c00; background: #fff8f0; }
.kcard.green  { border-color: #2e7d32; background: #f5fff5; }
.kcard.blue   { border-color: #1565c0; background: #f0f6ff; }
.kcard.purple { border-color: #6a1b9a; }

.kcard h3 { margin:0 0 .3rem 0; font-family:'DM Serif Display',serif; font-size:1.15rem; }
.kcard p  { margin:0; color:#555; font-size:0.9rem; }

/* ── Risk badge ── */
.risk-badge {
    display:inline-block; padding:8px 22px;
    border-radius:30px; font-weight:700;
    font-size:1.1rem; margin:10px 0;
    letter-spacing:.05em; text-transform:uppercase;
}
.risk-HIGH    { background:#e53935; color:white; }
.risk-MODERATE{ background:#f57c00; color:white; }
.risk-LOW     { background:#2e7d32; color:white; }

/* ── Section headers ── */
.section-head {
    font-family:'DM Serif Display',serif;
    font-size:1.8rem; color:#2d1054;
    border-bottom:3px solid #9c27b0;
    padding-bottom:.4rem; margin-bottom:1.2rem;
}
.section-sub { color:#6a1b9a; font-weight:600; font-size:.95rem; }

/* ── Checklist items ── */
.check-item {
    background:white; border-radius:10px;
    padding:.8rem 1.1rem; margin:.4rem 0;
    box-shadow:0 1px 6px rgba(0,0,0,0.06);
    border-left:4px solid #9c27b0;
    font-size:.93rem;
}
.check-item.flag { border-color:#e53935; background:#fff5f5; font-weight:600; }

/* ── Timeline ── */
.timeline-row {
    display:flex; gap:12px; align-items:flex-start;
    padding:10px 0; border-bottom:1px solid #f0e6ff;
}
.tl-dot {
    width:12px; height:12px; border-radius:50%;
    background:#9c27b0; margin-top:5px; flex-shrink:0;
}
.tl-dot.urgent { background:#e53935; }
.tl-dot.done   { background:#2e7d32; }

/* ── Referral cards ── */
.ref-card {
    border-radius:14px; padding:1.2rem 1.5rem;
    font-weight:600; font-size:1rem;
    text-align:center; margin:.5rem 0;
    cursor:default;
}
.ref-URGENT   { background:#e53935; color:white; }
.ref-ROUTINE  { background:#f57c00; color:white; }
.ref-IMAGING  { background:#1565c0; color:white; }
.ref-EDUCATION{ background:#2e7d32; color:white; }

/* ── Metric tiles ── */
.mtile {
    background:white; border-radius:14px;
    padding:1.2rem; text-align:center;
    box-shadow:0 2px 10px rgba(74,16,104,0.1);
    border-top:4px solid #9c27b0;
}
.mtile h2 { font-size:2.2rem; margin:0; color:#2d1054;
             font-family:'DM Serif Display',serif; }
.mtile p  { margin:0; color:#888; font-size:.85rem; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab"] {
    font-family:'DM Sans',sans-serif;
    font-weight:600; font-size:.95rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Session-state: patient registry & follow-up log ─────────────────────────
if "patients" not in st.session_state:
    # Seed with realistic demo data
    demo = [
        {"id":"PT-001","name":"Grace Wanjiku","age":42,"county":"Nairobi",
         "facility":"Kenyatta National Hospital","practitioner":"Nurse Achieng",
         "risk":"HIGH","referral":"Urgent","next_due": (datetime.today()-timedelta(days=3)).strftime("%Y-%m-%d"),
         "status":"Overdue","notes":"Palpable lump, nipple discharge"},
        {"id":"PT-002","name":"Fatuma Hassan","age":35,"county":"Mombasa",
         "facility":"Coast General Hospital","practitioner":"Dr. Mwenda",
         "risk":"MODERATE","referral":"Imaging","next_due":(datetime.today()+timedelta(days=2)).strftime("%Y-%m-%d"),
         "status":"Pending","notes":"Family history positive"},
        {"id":"PT-003","name":"Esther Chebet","age":28,"county":"Uasin Gishu",
         "facility":"Moi Teaching Hospital","practitioner":"Clinical Officer Ruto",
         "risk":"LOW","referral":"Education","next_due":(datetime.today()+timedelta(days=30)).strftime("%Y-%m-%d"),
         "status":"Scheduled","notes":"Routine screening"},
        {"id":"PT-004","name":"Mary Auma","age":55,"county":"Kisumu",
         "facility":"Kisumu County Hospital","practitioner":"Nurse Otieno",
         "risk":"HIGH","referral":"Urgent","next_due":(datetime.today()-timedelta(days=7)).strftime("%Y-%m-%d"),
         "status":"Overdue","notes":"Post-menopausal bleeding, skin changes"},
        {"id":"PT-005","name":"Jane Muthoni","age":48,"county":"Kiambu",
         "facility":"Thika Level 5","practitioner":"Dr. Kamau",
         "risk":"MODERATE","referral":"Routine","next_due":(datetime.today()+timedelta(days=14)).strftime("%Y-%m-%d"),
         "status":"Pending","notes":"Asymmetric density on self-exam"},
        {"id":"PT-006","name":"Rose Njeri","age":31,"county":"Nakuru",
         "facility":"Nakuru County Referral","practitioner":"Midwife Wambui",
         "risk":"LOW","referral":"Education","next_due":(datetime.today()-timedelta(days=1)).strftime("%Y-%m-%d"),
         "status":"Overdue","notes":"First visit, no symptoms"},
    ]
    st.session_state.patients = demo

if "screenings" not in st.session_state:
    # Demo screenings performed
    counties = ["Nairobi","Mombasa","Kisumu","Kiambu","Nakuru","Uasin Gishu","Homa Bay"]
    facilities = ["Public Hospital","Health Centre","Private Hospital","Dispensary","Community"]
    professions = ["Nurse","Clinical Officer","Doctor/Medical Officer","Midwife","Community Health Worker"]
    random.seed(42)
    rows = []
    for i in range(120):
        d = datetime.today() - timedelta(days=random.randint(0,89))
        rows.append({
            "date": d.strftime("%Y-%m-%d"),
            "month": d.strftime("%b %Y"),
            "county": random.choice(counties),
            "facility": random.choice(facilities),
            "profession": random.choice(professions),
            "risk": random.choices(["HIGH","MODERATE","LOW"], weights=[15,35,50])[0],
            "referral": random.choices(["Urgent","Imaging","Routine","Education"], weights=[12,20,30,38])[0],
            "followed_up": random.choices([True, False], weights=[55,45])[0],
        })
    st.session_state.screenings = pd.DataFrame(rows)


# ─── Sidebar navigation ───────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center;padding:1rem 0 .5rem;'>
  <div style='font-size:2.2rem'>🎗️</div>
  <div style='font-family:DM Serif Display,serif;font-size:1.3rem;font-weight:700;
              color:#f0e6ff;letter-spacing:.02em;'>BreastCare Kenya</div>
  <div style='font-size:.78rem;color:#c9a8e8;margin-top:.2rem;'>Clinical Decision Support</div>
</div>
<hr style='border-color:rgba(255,255,255,0.12);margin:.5rem 0 1rem;'>
""", unsafe_allow_html=True)

module = st.sidebar.radio("", [
    "🩺  Risk Assessment",
    "✅  Screening Checklist",
    "🔔  Follow-Up Tracker",
    "🔀  Referral Intelligence",
    "📊  Analytics Dashboard",
])

st.sidebar.markdown("""
<hr style='border-color:rgba(255,255,255,0.12);margin:1rem 0;'>
<div style='font-size:.75rem;color:#c9a8e8;text-align:center;line-height:1.6;'>
  Calibrated from Kenya KAP literature<br>2013–2024 · Synthetic demo data<br>
  <em>Not a substitute for clinical judgement</em>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — QUICK RISK ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════
if "Risk Assessment" in module:
    st.markdown('<div class="section-head">🩺 Quick Breast Cancer Risk Assessment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Complete the form below to calculate patient risk level and recommended action</div><br>', unsafe_allow_html=True)

    with st.form("risk_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("**Patient Information**")
            p_name    = st.text_input("Patient Name", placeholder="e.g. Grace Wanjiku")
            p_age     = st.number_input("Age (years)", 18, 90, 40)
            p_county  = st.selectbox("County", ["Nairobi","Mombasa","Kisumu","Kiambu","Nakuru","Uasin Gishu","Homa Bay","Other"])
            p_facility= st.selectbox("Facility", ["Public Hospital","Health Centre","Private Hospital","Dispensary","Community"])
            practitioner = st.text_input("Practitioner Name", placeholder="Your name")

        with c2:
            st.markdown("**Symptoms & Signs**")
            lump          = st.checkbox("Palpable breast lump")
            nipple_dc     = st.checkbox("Nipple discharge (non-milk)")
            skin_changes  = st.checkbox("Skin changes (peau d'orange, dimpling)")
            nipple_invert = st.checkbox("Nipple inversion / retraction")
            axillary      = st.checkbox("Axillary lymph node enlargement")
            breast_pain   = st.checkbox("Persistent unexplained breast pain")
            ulceration    = st.checkbox("Ulceration / open wound on breast")

        with c3:
            st.markdown("**Risk Factors**")
            fam_hist = st.selectbox("Family history of breast/ovarian cancer",
                                    ["None","1st-degree relative","2+ relatives or BRCA known"])
            menarche = st.selectbox("Age at first period",
                                    ["≥13 years (normal)", "<13 years (early)"])
            menopause= st.selectbox("Menopausal status",
                                    ["Pre-menopausal","Post-menopausal (<5 yrs)","Post-menopausal (>5 yrs)"])
            parity   = st.selectbox("Parity",
                                    ["Parous, first child <30","Nulliparous or first child ≥30"])
            breastfed= st.checkbox("Breastfed for ≥1 year (protective)")
            hrt      = st.checkbox("Current HRT / oral contraceptive use (>5 yrs)")
            prev_biopsy = st.checkbox("Previous abnormal breast biopsy")
            obesity  = st.checkbox("BMI ≥30 / obesity")

        submitted = st.form_submit_button("🔍  Calculate Risk & Recommend Action", use_container_width=True)

    if submitted:
        # ── Score calculation ──────────────────────────────────────────────
        score = 0

        # Symptoms (most heavily weighted — these are clinical red flags)
        if ulceration:    score += 40
        if axillary:      score += 30
        if skin_changes:  score += 25
        if nipple_invert: score += 20
        if lump:          score += 20
        if nipple_dc:     score += 15
        if breast_pain:   score += 5

        # Family history
        if fam_hist == "2+ relatives or BRCA known": score += 25
        elif fam_hist == "1st-degree relative":      score += 15

        # Reproductive / hormonal
        if menopause == "Post-menopausal (>5 yrs)":  score += 15
        elif menopause == "Post-menopausal (<5 yrs)": score += 8
        if menarche == "<13 years (early)":           score += 8
        if parity == "Nulliparous or first child ≥30":score += 8
        if hrt:          score += 8
        if prev_biopsy:  score += 10
        if obesity:      score += 5
        if breastfed:    score -= 8  # protective

        # Age
        if p_age >= 50:   score += 15
        elif p_age >= 40: score += 8
        elif p_age >= 35: score += 4

        # Determine risk level
        if score >= 50 or ulceration or (lump and axillary) or (lump and skin_changes):
            risk = "HIGH"
        elif score >= 25:
            risk = "MODERATE"
        else:
            risk = "LOW"

        # Determine referral
        if risk == "HIGH":
            referral = "Urgent"
            ref_action = "Refer IMMEDIATELY to oncology/surgical unit. Do not delay. Document and call ahead."
            ref_class = "red"
        elif risk == "MODERATE":
            if lump or axillary:
                referral = "Imaging"
                ref_action = "Order mammogram/ultrasound within 2 weeks. Follow up with patient directly."
            else:
                referral = "Routine"
                ref_action = "Schedule follow-up within 4–6 weeks. Educate on BSE. Review at next visit."
            ref_class = "orange"
        else:
            referral = "Education"
            ref_action = "Provide breast self-examination (BSE) education. Schedule annual screening."
            ref_class = "green"

        # Red flags present?
        red_flags = [s for s, v in {
            "Palpable lump":lump, "Nipple discharge":nipple_dc,
            "Skin changes":skin_changes,"Nipple inversion":nipple_invert,
            "Axillary nodes":axillary,"Ulceration":ulceration
        }.items() if v]

        # ── Display results ────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📋 Assessment Result")

        rc1, rc2 = st.columns([1, 2])
        with rc1:
            badge_class = f"risk-{risk}"
            st.markdown(f"""
            <div class="kcard {ref_class}">
              <h3>{p_name or 'Patient'} · Age {p_age}</h3>
              <p>{p_county} · {p_facility}</p>
              <br>
              <div style='font-size:.85rem;color:#888;'>Risk Score</div>
              <div style='font-size:2.5rem;font-weight:800;color:{"#e53935" if risk=="HIGH" else "#f57c00" if risk=="MODERATE" else "#2e7d32"};'>
                {min(score, 100)}
              </div>
              <span class='risk-badge {badge_class}'>{risk} RISK</span>
              <br><br>
              <div style='font-size:.85rem;color:#888;'>Referral Decision</div>
              <div class='ref-card ref-{referral}' style='margin-top:.4rem;'>
                {'🚨' if referral=='Urgent' else '🖼️' if referral=='Imaging' else '📅' if referral=='Routine' else '📚'} {referral} Referral
              </div>
            </div>
            """, unsafe_allow_html=True)

        with rc2:
            st.markdown(f"""
            <div class="kcard blue">
              <h3>Recommended Action</h3>
              <p style='font-size:1rem;color:#1a237e;font-weight:600;'>{ref_action}</p>
            </div>
            """, unsafe_allow_html=True)

            if red_flags:
                flags_html = "".join([f"<li style='margin:.3rem 0;'>⚠️ {f}</li>" for f in red_flags])
                st.markdown(f"""
                <div class="kcard red">
                  <h3>🚩 Red Flags Detected</h3>
                  <ul style='margin:.5rem 0 0;padding-left:1.2rem;'>{flags_html}</ul>
                </div>
                """, unsafe_allow_html=True)

            next_due = (datetime.today() + timedelta(days=1 if risk=="HIGH" else 14 if risk=="MODERATE" else 365)).strftime("%Y-%m-%d")
            st.markdown(f"""
            <div class="kcard purple">
              <h3>📅 Follow-Up Due</h3>
              <p style='font-size:1rem;font-weight:600;color:#4a148c;'>{next_due}</p>
              <p>Practitioner: {practitioner or 'Not recorded'}</p>
            </div>
            """, unsafe_allow_html=True)

        # Save to registry
        if p_name:
            new_patient = {
                "id": f"PT-{len(st.session_state.patients)+1:03d}",
                "name": p_name, "age": p_age, "county": p_county,
                "facility": p_facility, "practitioner": practitioner,
                "risk": risk, "referral": referral, "next_due": next_due,
                "status": "Pending" if risk != "HIGH" else "Urgent",
                "notes": ", ".join(red_flags) if red_flags else "No red flags"
            }
            st.session_state.patients.append(new_patient)
            # Add to screenings
            new_s = pd.DataFrame([{
                "date": datetime.today().strftime("%Y-%m-%d"),
                "month": datetime.today().strftime("%b %Y"),
                "county": p_county, "facility": p_facility,
                "profession": "Unknown", "risk": risk,
                "referral": referral, "followed_up": False
            }])
            st.session_state.screenings = pd.concat(
                [st.session_state.screenings, new_s], ignore_index=True)
            st.success(f"✅ Patient **{p_name}** saved to follow-up registry.")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — SCREENING CHECKLIST
# ══════════════════════════════════════════════════════════════════════════════
elif "Screening Checklist" in module:
    st.markdown('<div class="section-head">✅ Guided Screening Checklist</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Step-by-step examination workflow · Red flags auto-detected</div><br>', unsafe_allow_html=True)

    step = st.session_state.get("checklist_step", 1)

    steps = {
        1: ("📋 History Taking", [
            ("Chief complaint documented", False),
            ("Duration of symptoms recorded", False),
            ("Previous breast conditions / biopsies noted", False),
            ("Menstrual & reproductive history taken", False),
            ("Family history (1st & 2nd degree) documented", False),
            ("Medication history (HRT, OCP) reviewed", False),
            ("Alcohol / smoking history noted", False),
        ]),
        2: ("👁️ Visual Inspection (patient seated, arms at sides)", [
            ("Breast symmetry assessed — note asymmetry", False),
            ("Skin surface checked: peau d'orange, dimpling", False),
            ("Nipple position & symmetry checked", False),
            ("Areola colour changes noted", False),
            ("Visible lump or contour change observed", False),
            ("Arms raised — repeat inspection", False),
            ("Hands on hips (pectoral contraction) — repeat", False),
        ]),
        3: ("🖐️ Palpation — Breast (patient supine)", [
            ("Systematic pattern chosen (spiral / radial / grid)", False),
            ("All 4 quadrants palpated with 3-finger technique", False),
            ("Tail of Spence (axillary extension) palpated", False),
            ("Areola & nipple gently compressed", False),
            ("Nipple discharge — colour & consistency noted", False),
            ("Lump characteristics recorded: size, shape, mobility, tenderness", False),
        ]),
        4: ("🔍 Lymph Node Examination", [
            ("Axillary nodes palpated — anterior, posterior, medial", False),
            ("Supraclavicular nodes palpated", False),
            ("Infraclavicular nodes palpated", False),
            ("Node size, consistency, mobility noted", False),
            ("Bilateral comparison performed", False),
        ]),
        5: ("🚩 Red Flag Detection & Decision", [
            ("Hard, irregular, fixed lump present?", False),
            ("Skin tethering or dimpling present?", False),
            ("Bloody or spontaneous nipple discharge?", False),
            ("Nipple retraction (new)?", False),
            ("Axillary nodes enlarged / fixed?", False),
            ("Ulceration or skin breakdown?", False),
            ("Post-menopausal patient with any lump?", False),
        ]),
    }

    # Step navigation
    col_prev, col_step, col_next = st.columns([1, 4, 1])
    with col_prev:
        if st.button("← Back") and step > 1:
            st.session_state.checklist_step = step - 1
            st.rerun()
    with col_step:
        st.progress(step / len(steps))
        title, items = steps[step]
        st.markdown(f"**Step {step} of {len(steps)}: {title}**")
    with col_next:
        if st.button("Next →") and step < len(steps):
            st.session_state.checklist_step = step + 1
            st.rerun()

    title, items = steps[step]
    st.markdown(f"### {title}")

    checked = []
    for i, (item, _) in enumerate(items):
        is_flag = step == 5  # Red flag step
        checked_val = st.checkbox(item, key=f"chk_{step}_{i}")
        css_class = "check-item flag" if (is_flag and checked_val) else "check-item"
        prefix = "🚩" if (is_flag and checked_val) else "✔️" if checked_val else "○"
        st.markdown(f'<div class="{css_class}">{prefix} {item}</div>', unsafe_allow_html=True)
        checked.append(checked_val)

    done_count = sum(checked)
    st.markdown(f"<br>**{done_count}/{len(items)} items completed**", unsafe_allow_html=True)

    if step == 5:
        red_flag_count = sum(checked)
        if red_flag_count >= 3:
            st.error(f"🚨 **{red_flag_count} red flags detected — URGENT REFERRAL required.**")
        elif red_flag_count >= 1:
            st.warning(f"⚠️ **{red_flag_count} red flag(s) detected — refer for imaging within 2 weeks.**")
        else:
            st.success("✅ **No red flags detected — educate on BSE and schedule annual follow-up.**")

    if step == 1:
        st.info("💡 **Tip:** Ensure patient privacy and explain each step before proceeding.")
    elif step == 2:
        st.info("💡 **Tip:** Adequate lighting is essential. Ask patient to disrobe to waist for full inspection.")
    elif step == 3:
        st.info("💡 **Tip:** Use the pads of fingers (not tips). Apply light, medium, and firm pressure at each point.")
    elif step == 4:
        st.info("💡 **Tip:** Stand on the same side as the axilla being examined. Support the patient's arm.")
    elif step == 5:
        st.info("💡 **Red flags must be documented and acted on immediately. Never dismiss a patient concern.**")

    if st.button("🔄 Restart Checklist"):
        st.session_state.checklist_step = 1
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3 — SMART FOLLOW-UP TRACKER
# ══════════════════════════════════════════════════════════════════════════════
elif "Follow-Up" in module:
    st.markdown('<div class="section-head">🔔 Smart Follow-Up Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Track pending screenings · Flag missed follow-ups · Manage patient timelines</div><br>', unsafe_allow_html=True)

    df_p = pd.DataFrame(st.session_state.patients)
    today = datetime.today().strftime("%Y-%m-%d")

    # Auto-update overdue status
    def get_status(row):
        if row["next_due"] < today and row["status"] != "Done":
            return "Overdue"
        return row["status"]
    df_p["status"] = df_p.apply(get_status, axis=1)

    # Summary tiles
    n_total   = len(df_p)
    n_overdue = len(df_p[df_p["status"] == "Overdue"])
    n_urgent  = len(df_p[df_p["risk"] == "HIGH"])
    n_pending = len(df_p[df_p["status"] == "Pending"])

    t1, t2, t3, t4 = st.columns(4)
    for col, val, label, colour in [
        (t1, n_total,   "Total Patients",   "#6a1b9a"),
        (t2, n_overdue, "Overdue",          "#e53935"),
        (t3, n_urgent,  "High Risk",        "#f57c00"),
        (t4, n_pending, "Pending Follow-Up","#1565c0"),
    ]:
        col.markdown(f"""
        <div class="mtile" style="border-top-color:{colour};">
          <h2 style="color:{colour};">{val}</h2>
          <p>{label}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter
    fc1, fc2 = st.columns(2)
    filter_status = fc1.selectbox("Filter by Status", ["All","Overdue","Pending","Scheduled","Urgent","Done"])
    filter_risk   = fc2.selectbox("Filter by Risk", ["All","HIGH","MODERATE","LOW"])

    df_view = df_p.copy()
    if filter_status != "All": df_view = df_view[df_view["status"] == filter_status]
    if filter_risk   != "All": df_view = df_view[df_view["risk"]   == filter_risk]

    st.markdown(f"**Showing {len(df_view)} patients**")

    for _, row in df_view.iterrows():
        days_diff = (datetime.strptime(row["next_due"], "%Y-%m-%d") - datetime.today()).days
        overdue_txt = f"⚠️ {abs(days_diff)} days overdue" if days_diff < 0 else f"Due in {days_diff} days"
        status_colour = {"Overdue":"#e53935","Pending":"#f57c00","Scheduled":"#1565c0",
                         "Urgent":"#b71c1c","Done":"#2e7d32"}.get(row["status"],"#888")
        risk_colour   = {"HIGH":"#e53935","MODERATE":"#f57c00","LOW":"#2e7d32"}.get(row["risk"],"#888")

        with st.expander(f"**{row['id']}** · {row['name']} · {row['county']} · "
                         f"{'🔴' if row['risk']=='HIGH' else '🟡' if row['risk']=='MODERATE' else '🟢'} {row['risk']}"):
            ec1, ec2, ec3 = st.columns(3)
            ec1.markdown(f"**Age:** {row['age']}")
            ec1.markdown(f"**Facility:** {row['facility']}")
            ec2.markdown(f"**Practitioner:** {row['practitioner']}")
            ec2.markdown(f"**Referral:** {row['referral']}")
            ec3.markdown(f"**Next Due:** `{row['next_due']}`")
            ec3.markdown(f"**{overdue_txt}**")
            st.markdown(f"**Notes:** {row['notes']}")

            action_col1, action_col2, action_col3 = st.columns(3)
            if action_col1.button("✅ Mark Done", key=f"done_{row['id']}"):
                for i, p in enumerate(st.session_state.patients):
                    if p["id"] == row["id"]:
                        st.session_state.patients[i]["status"] = "Done"
                st.success("Marked as done!")
                st.rerun()
            if action_col2.button("📅 Reschedule +2 weeks", key=f"resched_{row['id']}"):
                new_date = (datetime.today() + timedelta(weeks=2)).strftime("%Y-%m-%d")
                for i, p in enumerate(st.session_state.patients):
                    if p["id"] == row["id"]:
                        st.session_state.patients[i]["next_due"] = new_date
                        st.session_state.patients[i]["status"] = "Scheduled"
                st.info(f"Rescheduled to {new_date}")
                st.rerun()
            if action_col3.button("🚨 Flag Urgent", key=f"urg_{row['id']}"):
                for i, p in enumerate(st.session_state.patients):
                    if p["id"] == row["id"]:
                        st.session_state.patients[i]["status"] = "Urgent"
                        st.session_state.patients[i]["risk"] = "HIGH"
                st.error("Flagged as urgent!")
                st.rerun()

    # Add new patient manually
    st.markdown("---")
    st.markdown("### ➕ Add Patient to Tracker")
    with st.form("add_patient"):
        nc1, nc2, nc3 = st.columns(3)
        np_name  = nc1.text_input("Patient Name")
        np_age   = nc1.number_input("Age", 18, 90, 35)
        np_county= nc2.selectbox("County", ["Nairobi","Mombasa","Kisumu","Kiambu","Nakuru","Uasin Gishu","Homa Bay","Other"])
        np_prac  = nc2.text_input("Practitioner")
        np_risk  = nc3.selectbox("Risk Level", ["LOW","MODERATE","HIGH"])
        np_ref   = nc3.selectbox("Referral", ["Education","Routine","Imaging","Urgent"])
        np_notes = st.text_area("Clinical Notes", height=70)
        np_due   = st.date_input("Next Follow-Up Date", datetime.today() + timedelta(days=14))

        if st.form_submit_button("➕ Add Patient", use_container_width=True):
            if np_name:
                st.session_state.patients.append({
                    "id": f"PT-{len(st.session_state.patients)+1:03d}",
                    "name": np_name, "age": np_age, "county": np_county,
                    "facility": "—", "practitioner": np_prac,
                    "risk": np_risk, "referral": np_ref,
                    "next_due": np_due.strftime("%Y-%m-%d"),
                    "status": "Scheduled", "notes": np_notes,
                })
                st.success(f"✅ {np_name} added to tracker!")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 4 — REFERRAL INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif "Referral" in module:
    st.markdown('<div class="section-head">🔀 Referral Intelligence Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Select patient symptoms · Receive evidence-based referral decision</div><br>', unsafe_allow_html=True)

    st.markdown("### Select presenting symptoms & signs")

    rc1, rc2 = st.columns(2)
    with rc1:
        st.markdown("**Clinical Signs**")
        s_lump     = st.checkbox("🔴 Palpable breast lump")
        s_axillary = st.checkbox("🔴 Axillary lymphadenopathy")
        s_skin     = st.checkbox("🟠 Skin changes / dimpling")
        s_nipple_i = st.checkbox("🟠 Nipple inversion (new)")
        s_nipple_d = st.checkbox("🟠 Nipple discharge (non-milk)")
        s_ulcer    = st.checkbox("🔴 Ulceration / wound on breast")
        s_pain     = st.checkbox("🟡 Breast pain (persistent, unexplained)")
        s_asymmetry= st.checkbox("🟡 Breast asymmetry (new)")

    with rc2:
        st.markdown("**Patient Context**")
        age_group = st.selectbox("Age group", ["<35 years","35–49 years","50+ years"])
        fhx       = st.selectbox("Family history", ["None","1st-degree relative","Strong / BRCA"])
        prev_ca   = st.checkbox("Personal history of any cancer")
        post_meno = st.checkbox("Post-menopausal")
        rapid_chg = st.checkbox("Rapid change in size / appearance")
        bilateral = st.checkbox("Bilateral symptoms")

    if st.button("🔀  Generate Referral Decision", use_container_width=True):
        # Score
        urgent_score  = 0
        imaging_score = 0
        routine_score = 0
        edu_score     = 0

        if s_lump:      urgent_score += 3; imaging_score += 2
        if s_axillary:  urgent_score += 4
        if s_ulcer:     urgent_score += 5
        if s_skin:      urgent_score += 3; imaging_score += 2
        if s_nipple_i:  urgent_score += 2; imaging_score += 2
        if s_nipple_d:  urgent_score += 1; imaging_score += 3
        if rapid_chg:   urgent_score += 2
        if prev_ca:     urgent_score += 3
        if fhx == "Strong / BRCA": urgent_score += 2; imaging_score += 2
        elif fhx == "1st-degree relative": imaging_score += 2; routine_score += 1
        if post_meno and s_lump: urgent_score += 2
        if age_group == "50+ years": imaging_score += 1
        if s_pain and not s_lump: routine_score += 2; edu_score += 1
        if s_asymmetry and not s_lump: imaging_score += 1; routine_score += 1
        if not any([s_lump, s_axillary, s_skin, s_nipple_i, s_nipple_d, s_ulcer]):
            edu_score += 3

        scores = {"Urgent": urgent_score, "Imaging": imaging_score,
                  "Routine": routine_score, "Education": edu_score}
        decision = max(scores, key=scores.get)

        ref_map = {
            "Urgent":    ("🚨", "#e53935",
                          "URGENT REFERRAL — Refer within 24 hours to oncology/surgical unit.",
                          ["Contact receiving facility before sending patient",
                           "Provide written referral letter with clinical findings",
                           "Ensure patient has transport support",
                           "Document in patient file and notify facility in-charge"]),
            "Imaging":   ("🖼️", "#1565c0",
                          "IMAGING REQUIRED — Mammogram and/or ultrasound within 2 weeks.",
                          ["Order bilateral mammogram if ≥40 years",
                           "Ultrasound preferred if <40 years or dense breasts",
                           "Provide patient with written imaging request",
                           "Book follow-up appointment to review results"]),
            "Routine":   ("📅", "#f57c00",
                          "ROUTINE FOLLOW-UP — Reassess within 4–6 weeks.",
                          ["Educate patient on breast self-examination (BSE)",
                           "Document current findings with measurements",
                           "Book firm follow-up appointment before patient leaves",
                           "Advise patient to return sooner if symptoms worsen"]),
            "Education": ("📚", "#2e7d32",
                          "EDUCATION & AWARENESS — No acute clinical concern identified.",
                          ["Demonstrate breast self-examination technique",
                           "Provide take-home BSE reminder card",
                           "Discuss screening schedule (annual clinical exam)",
                           "Advise on risk reduction: healthy weight, limit alcohol"]),
        }

        icon, colour, headline, actions = ref_map[decision]
        actions_html = "".join([f"<li style='margin:.4rem 0;'>{a}</li>" for a in actions])

        st.markdown("---")
        st.markdown(f"""
        <div style='background:{colour};color:white;border-radius:16px;
                    padding:1.5rem 2rem;margin-bottom:1rem;'>
          <div style='font-size:2rem;'>{icon}</div>
          <div style='font-family:DM Serif Display,serif;font-size:1.5rem;margin:.3rem 0;'>{decision} Referral</div>
          <div style='font-size:1rem;opacity:.92;'>{headline}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="kcard">
          <h3>📋 Action Steps</h3>
          <ul style='margin:.5rem 0;padding-left:1.3rem;color:#333;font-size:.95rem;'>
            {actions_html}
          </ul>
        </div>
        """, unsafe_allow_html=True)

        # Score breakdown bar
        st.markdown("**Decision score breakdown**")
        fig_scores = px.bar(
            x=list(scores.keys()), y=list(scores.values()),
            color=list(scores.keys()),
            color_discrete_map={"Urgent":"#e53935","Imaging":"#1565c0",
                                "Routine":"#f57c00","Education":"#2e7d32"},
            template="plotly_white", labels={"x":"Decision","y":"Score"},
            title="Evidence weighting behind recommendation"
        )
        fig_scores.update_layout(showlegend=False)
        st.plotly_chart(fig_scores, use_container_width=True)

        # Warning about knowledge gap
        if decision in ["Urgent","Imaging"]:
            st.warning("⚠️ **Practice gap alert:** Data shows Kenyan practitioners refer only 12–20% of cases that meet urgent criteria. This patient meets the threshold — please act on this recommendation.")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 5 — ANALYTICS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif "Analytics" in module:
    st.markdown('<div class="section-head">📊 Administrator Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Screenings performed · Referral patterns · Follow-up compliance · County & facility breakdown</div><br>', unsafe_allow_html=True)

    df_s = st.session_state.screenings.copy()
    df_p = pd.DataFrame(st.session_state.patients)

    # Filters
    fc1, fc2 = st.columns(2)
    county_filter = fc1.selectbox("Filter by County", ["All"] + sorted(df_s["county"].unique()))
    facility_filter = fc2.selectbox("Filter by Facility", ["All"] + sorted(df_s["facility"].unique()))
    if county_filter != "All":   df_s = df_s[df_s["county"]   == county_filter]
    if facility_filter != "All": df_s = df_s[df_s["facility"] == facility_filter]

    # KPI tiles
    n_screen    = len(df_s)
    n_urgent    = len(df_s[df_s["risk"]=="HIGH"])
    pct_followup= round(df_s["followed_up"].mean()*100, 1)
    n_overdue_p = len(df_p[df_p["status"]=="Overdue"])

    t1, t2, t3, t4 = st.columns(4)
    for col, val, lbl, col_ in [
        (t1, n_screen,    "Screenings (90 days)", "#6a1b9a"),
        (t2, n_urgent,    "High-Risk Cases",      "#e53935"),
        (t3, f"{pct_followup}%", "Follow-Up Rate","#f57c00"),
        (t4, n_overdue_p, "Overdue Follow-Ups",   "#1565c0"),
    ]:
        col.markdown(f"""<div class="mtile" style="border-top-color:{col_};">
          <h2 style="color:{col_};">{val}</h2><p>{lbl}</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Screenings over time
    trend = df_s.groupby("month").size().reset_index(name="Screenings")
    month_order = sorted(df_s["month"].unique(), key=lambda m: datetime.strptime(m, "%b %Y"))
    trend["month"] = pd.Categorical(trend["month"], categories=month_order, ordered=True)
    trend = trend.sort_values("month")

    fig_trend = px.line(trend, x="month", y="Screenings", markers=True,
                        template="plotly_white", title="📈 Screenings Performed Over Time",
                        color_discrete_sequence=["#6a1b9a"])
    fig_trend.update_traces(line_width=3, marker_size=8)
    st.plotly_chart(fig_trend, use_container_width=True)

    col_l, col_r = st.columns(2)

    with col_l:
        county_cnt = df_s.groupby("county").size().reset_index(name="Screenings").sort_values("Screenings", ascending=True)
        fig_county = px.bar(county_cnt, x="Screenings", y="county", orientation="h",
                            color_discrete_sequence=["#7b1fa2"],
                            template="plotly_white", title="🗺️ Screenings by County")
        st.plotly_chart(fig_county, use_container_width=True)

    with col_r:
        ref_cnt = df_s["referral"].value_counts().reset_index()
        ref_cnt.columns = ["Referral","Count"]
        fig_ref = px.pie(ref_cnt, names="Referral", values="Count",
                         color="Referral",
                         color_discrete_map={"Urgent":"#e53935","Imaging":"#1565c0",
                                             "Routine":"#f57c00","Education":"#2e7d32"},
                         template="plotly_white", title="🔀 Referral Breakdown")
        st.plotly_chart(fig_ref, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fac_cnt = df_s.groupby("facility").size().reset_index(name="Screenings")
        fig_fac = px.bar(fac_cnt, x="facility", y="Screenings",
                         color_discrete_sequence=["#1565c0"],
                         template="plotly_white", title="🏥 Screenings by Facility Type")
        fig_fac.update_layout(xaxis_tickangle=-20)
        st.plotly_chart(fig_fac, use_container_width=True)

    with col4:
        fu_data = df_s.groupby("county")["followed_up"].mean().mul(100).round(1).reset_index()
        fu_data.columns = ["County","Follow-Up Rate (%)"]
        fig_fu = px.bar(fu_data.sort_values("Follow-Up Rate (%)", ascending=True),
                        x="Follow-Up Rate (%)", y="County", orientation="h",
                        color="Follow-Up Rate (%)",
                        color_continuous_scale=["#e53935","#f57c00","#2e7d32"],
                        template="plotly_white",
                        title="📋 Follow-Up Compliance by County")
        fig_fu.add_vline(x=pct_followup, line_dash="dash", line_color="purple",
                         annotation_text="Overall avg")
        st.plotly_chart(fig_fu, use_container_width=True)

    # Risk distribution by profession
    risk_prof = df_s.groupby(["profession","risk"]).size().reset_index(name="Count")
    fig_rp = px.bar(risk_prof, x="profession", y="Count", color="risk",
                    color_discrete_map={"HIGH":"#e53935","MODERATE":"#f57c00","LOW":"#2e7d32"},
                    template="plotly_white", barmode="stack",
                    title="⚕️ Risk Distribution by Profession")
    fig_rp.update_layout(xaxis_tickangle=-20)
    st.plotly_chart(fig_rp, use_container_width=True)

    # Missed follow-ups alert table
    overdue = df_p[df_p["status"]=="Overdue"].sort_values("next_due")
    if not overdue.empty:
        st.markdown("### 🚨 Overdue Follow-Ups")
        st.error(f"**{len(overdue)} patient(s) have missed their follow-up date.** Immediate action required.")
        st.dataframe(overdue[["id","name","county","facility","risk","referral","next_due","practitioner","notes"]]
                     .reset_index(drop=True), use_container_width=True)
    else:
        st.success("✅ No overdue follow-ups at this time.")

    # Export
    st.markdown("---")
    csv = df_s.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export Screening Data (CSV)", data=csv,
                       file_name="breastcare_kenya_screenings.csv", mime="text/csv")