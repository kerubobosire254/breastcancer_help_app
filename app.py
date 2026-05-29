"""
KAP Dashboard — Knowledge, Attitudes & Practices of Health Practitioners on Breast Cancer (Kenya)
Streamlit App | Synthetic Dataset (n=250)

Run with:
    streamlit run kap_oncology_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="KAP Oncology Dashboard — Kenya",
    page_icon="🎗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border-left: 5px solid;
        margin-bottom: 0.5rem;
    }
    .metric-card.knowledge { border-color: #2196F3; }
    .metric-card.attitude  { border-color: #4CAF50; }
    .metric-card.practice  { border-color: #FF9800; }
    .metric-card h2 { margin: 0; font-size: 2rem; font-weight: 700; }
    .metric-card p  { margin: 0; color: #666; font-size: 0.9rem; }
    section[data-testid="stSidebar"] { background-color: #1a1a2e; color: white; }
    section[data-testid="stSidebar"] .css-1d391kg { color: white; }
    h1, h2, h3 { color: #1a1a2e; }
    .stTabs [data-baseweb="tab"] { font-size: 1rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Colour palette ────────────────────────────────────────────────────────────
COLOURS = {
    "Nurse":                  "#2196F3",
    "Clinical Officer":       "#4CAF50",
    "Doctor/Medical Officer": "#9C27B0",
    "Midwife":                "#FF9800",
    "Community Health Worker":"#F44336",
}
KAP_COLOURS = {
    "Knowledge Score (%)": "#2196F3",
    "Attitude Score (%)":  "#4CAF50",
    "Practice Score (%)":  "#FF9800",
}

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """Build the dataset from embedded values (no file dependency)."""
    rows = [
        (1,"Nurse","Female",44,19,"Diploma","Nairobi","Health Centre","No",65,68,16,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (2,"Nurse","Male",34,8,"Degree","Homa Bay","Public Hospital","No",52,79,55,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (3,"Doctor/Medical Officer","Female",29,7,"Postgraduate","Kisumu","Private Hospital","Yes",46,81,57,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (4,"Clinical Officer","Male",39,14,"Degree","Uasin Gishu","Private Hospital","No",51,72,41,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (5,"Clinical Officer","Female",41,15,"Degree","Other","Health Centre","No",58,68,29,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (6,"Doctor/Medical Officer","Female",31,9,"Degree","Kiambu","Public Hospital","No",50,71,61,"Poor (<60%)","Positive (≥70%)","Active (≥60%)"),
        (7,"Nurse","Female",46,23,"Certificate","Kisumu","Dispensary","No",59,63,20,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (8,"Doctor/Medical Officer","Female",31,6,"Degree","Other","Public Hospital","No",77,76,37,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (9,"Doctor/Medical Officer","Female",39,16,"Postgraduate","Kiambu","Private Hospital","No",68,57,52,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (10,"Clinical Officer","Female",40,14,"Postgraduate","Uasin Gishu","Dispensary","No",62,66,41,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (11,"Nurse","Female",34,8,"Diploma","Uasin Gishu","Private Hospital","No",40,56,5,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (12,"Nurse","Female",46,21,"Diploma","Nairobi","Public Hospital","Yes",52,48,24,"Poor (<60%)","Negative (<50%)","Inactive (<40%)"),
        (13,"Nurse","Female",33,10,"Diploma","Nairobi","Private Hospital","No",51,73,22,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (14,"Nurse","Female",39,14,"Degree","Kisumu","Dispensary","No",47,74,49,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (15,"Midwife","Male",34,9,"Degree","Kiambu","Health Centre","No",51,55,36,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (16,"Nurse","Female",39,14,"Diploma","Other","Health Centre","No",39,62,30,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (17,"Clinical Officer","Female",24,0,"Certificate","Kisumu","Public Hospital","No",55,51,62,"Poor (<60%)","Neutral (50-69%)","Active (≥60%)"),
        (18,"Nurse","Female",35,10,"Diploma","Other","Dispensary","No",49,61,24,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (19,"Nurse","Female",40,15,"Certificate","Kiambu","Public Hospital","No",48,87,8,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (20,"Nurse","Female",24,1,"Diploma","Uasin Gishu","Public Hospital","Yes",42,52,16,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (21,"Doctor/Medical Officer","Female",45,21,"Degree","Nakuru","Public Hospital","No",62,62,46,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (22,"Community Health Worker","Male",35,11,"Certificate","Nairobi","Community","No",49,37,17,"Poor (<60%)","Negative (<50%)","Inactive (<40%)"),
        (23,"Nurse","Female",29,5,"Degree","Nairobi","Community","Yes",56,76,32,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (24,"Nurse","Female",37,11,"Diploma","Kiambu","Private Hospital","No",54,57,18,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (25,"Clinical Officer","Female",29,6,"Diploma","Mombasa","Public Hospital","No",49,71,42,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (26,"Midwife","Male",35,9,"Diploma","Nairobi","Public Hospital","No",54,54,12,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (27,"Nurse","Female",36,11,"Diploma","Kiambu","Private Hospital","No",58,60,12,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (28,"Nurse","Female",43,19,"Diploma","Nairobi","Public Hospital","No",47,71,25,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (29,"Doctor/Medical Officer","Female",42,17,"Degree","Uasin Gishu","Private Hospital","Yes",57,78,43,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (30,"Midwife","Female",41,17,"Diploma","Mombasa","Health Centre","No",51,77,15,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (31,"Nurse","Male",37,15,"Degree","Kisumu","Public Hospital","No",51,72,34,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (32,"Nurse","Female",28,2,"Diploma","Uasin Gishu","Public Hospital","No",51,58,11,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (33,"Nurse","Female",33,11,"Diploma","Nairobi","Dispensary","Yes",53,66,19,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (34,"Clinical Officer","Male",30,5,"Diploma","Homa Bay","Dispensary","No",38,69,20,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (35,"Community Health Worker","Male",34,12,"Certificate","Other","Private Hospital","No",41,60,5,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (36,"Doctor/Medical Officer","Female",39,13,"Degree","Nakuru","Private Hospital","No",68,84,28,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (37,"Nurse","Female",43,17,"Degree","Nairobi","Health Centre","No",71,44,22,"Moderate (60-79%)","Negative (<50%)","Inactive (<40%)"),
        (38,"Nurse","Female",43,20,"Certificate","Homa Bay","Public Hospital","No",52,69,29,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (39,"Nurse","Male",27,4,"Degree","Mombasa","Health Centre","No",54,79,24,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (40,"Doctor/Medical Officer","Female",31,7,"Postgraduate","Nairobi","Public Hospital","Yes",78,68,25,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (41,"Clinical Officer","Male",38,14,"Degree","Kiambu","Health Centre","No",58,56,31,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (42,"Nurse","Female",37,13,"Certificate","Kisumu","Dispensary","No",54,66,18,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (43,"Nurse","Male",22,0,"Certificate","Kiambu","Health Centre","No",50,64,30,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (44,"Nurse","Female",29,4,"Degree","Mombasa","Public Hospital","No",57,62,13,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (45,"Midwife","Female",38,13,"Degree","Uasin Gishu","Private Hospital","No",55,67,13,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (46,"Nurse","Female",39,17,"Degree","Kiambu","Public Hospital","No",40,86,16,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (47,"Clinical Officer","Female",26,3,"Diploma","Kiambu","Dispensary","No",47,80,18,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (48,"Clinical Officer","Female",25,2,"Diploma","Nairobi","Public Hospital","No",56,68,17,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (49,"Nurse","Female",31,8,"Diploma","Kiambu","Public Hospital","No",55,61,44,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (50,"Midwife","Female",43,18,"Diploma","Uasin Gishu","Public Hospital","No",64,42,26,"Moderate (60-79%)","Negative (<50%)","Inactive (<40%)"),
        (51,"Clinical Officer","Female",29,3,"Diploma","Kisumu","Dispensary","No",74,75,39,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (52,"Clinical Officer","Female",28,3,"Diploma","Other","Health Centre","No",45,62,41,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (53,"Clinical Officer","Female",25,2,"Degree","Mombasa","Health Centre","No",55,73,27,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (54,"Clinical Officer","Female",33,10,"Degree","Nairobi","Health Centre","No",66,63,53,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (55,"Nurse","Female",37,12,"Certificate","Kisumu","Community","No",66,52,14,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (56,"Nurse","Male",44,19,"Diploma","Other","Dispensary","No",68,72,26,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (57,"Community Health Worker","Female",22,0,"Certificate","Nairobi","Community","No",32,63,11,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (58,"Nurse","Female",35,13,"Diploma","Nairobi","Public Hospital","No",69,65,23,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (59,"Midwife","Female",37,11,"Diploma","Other","Public Hospital","No",52,57,20,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (60,"Nurse","Female",27,1,"Diploma","Kisumu","Public Hospital","No",44,59,22,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (61,"Nurse","Male",28,5,"Certificate","Nakuru","Public Hospital","No",70,66,43,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (62,"Clinical Officer","Female",36,11,"Degree","Homa Bay","Private Hospital","No",73,65,22,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (63,"Clinical Officer","Female",36,11,"Diploma","Other","Health Centre","No",54,81,54,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (64,"Clinical Officer","Female",34,10,"Degree","Nakuru","Public Hospital","No",71,72,6,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (65,"Midwife","Male",22,0,"Diploma","Mombasa","Private Hospital","No",53,70,26,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (66,"Nurse","Female",31,7,"Diploma","Nairobi","Health Centre","No",40,69,27,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (67,"Doctor/Medical Officer","Male",34,11,"Degree","Uasin Gishu","Health Centre","No",75,66,32,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (68,"Nurse","Female",46,23,"Degree","Nairobi","Health Centre","No",52,57,51,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (69,"Midwife","Female",33,8,"Certificate","Uasin Gishu","Health Centre","No",35,74,20,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (70,"Nurse","Female",22,0,"Degree","Uasin Gishu","Dispensary","No",46,54,41,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (71,"Clinical Officer","Female",26,1,"Degree","Nakuru","Public Hospital","No",52,79,22,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (72,"Clinical Officer","Female",34,8,"Diploma","Mombasa","Health Centre","No",66,65,27,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (73,"Doctor/Medical Officer","Male",30,5,"Postgraduate","Nakuru","Dispensary","No",78,69,42,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (74,"Nurse","Female",41,18,"Degree","Other","Private Hospital","No",49,79,31,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (75,"Clinical Officer","Male",37,15,"Degree","Other","Public Hospital","Yes",67,67,26,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (76,"Community Health Worker","Female",36,13,"Diploma","Nairobi","Community","No",21,40,25,"Poor (<60%)","Negative (<50%)","Inactive (<40%)"),
        (77,"Nurse","Male",46,20,"Certificate","Uasin Gishu","Public Hospital","Yes",36,56,30,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (78,"Midwife","Male",33,11,"Diploma","Homa Bay","Public Hospital","No",50,70,24,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (79,"Doctor/Medical Officer","Male",36,14,"Degree","Nairobi","Public Hospital","No",67,77,37,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (80,"Nurse","Female",37,11,"Diploma","Other","Community","Yes",28,64,48,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (81,"Nurse","Female",41,16,"Certificate","Kisumu","Public Hospital","No",58,57,43,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (82,"Nurse","Female",32,6,"Diploma","Nairobi","Public Hospital","No",50,78,18,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (83,"Clinical Officer","Male",24,1,"Diploma","Nairobi","Dispensary","No",52,51,20,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (84,"Nurse","Female",40,16,"Diploma","Nairobi","Public Hospital","No",39,74,24,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (85,"Doctor/Medical Officer","Female",41,18,"Degree","Kiambu","Public Hospital","No",70,69,58,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (86,"Community Health Worker","Female",24,2,"Degree","Kiambu","Community","No",45,64,5,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (87,"Nurse","Male",37,11,"Diploma","Mombasa","Dispensary","No",55,78,29,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (88,"Nurse","Male",25,0,"Certificate","Kiambu","Public Hospital","No",67,45,35,"Moderate (60-79%)","Negative (<50%)","Inactive (<40%)"),
        (89,"Nurse","Female",40,18,"Diploma","Kiambu","Public Hospital","No",59,78,24,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (90,"Doctor/Medical Officer","Female",39,14,"Degree","Kiambu","Health Centre","No",66,48,54,"Moderate (60-79%)","Negative (<50%)","Moderate (40-59%)"),
        (91,"Doctor/Medical Officer","Female",35,12,"Postgraduate","Nairobi","Private Hospital","Yes",70,61,45,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (92,"Doctor/Medical Officer","Female",37,11,"Degree","Nairobi","Private Hospital","Yes",56,78,35,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (93,"Nurse","Female",36,10,"Certificate","Kiambu","Health Centre","No",37,66,40,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (94,"Nurse","Female",40,15,"Diploma","Nakuru","Private Hospital","No",53,58,38,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (95,"Doctor/Medical Officer","Female",40,18,"Degree","Nairobi","Public Hospital","Yes",77,58,63,"Moderate (60-79%)","Neutral (50-69%)","Active (≥60%)"),
        (96,"Nurse","Female",30,5,"Certificate","Homa Bay","Health Centre","No",43,69,22,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (97,"Nurse","Female",41,18,"Diploma","Other","Dispensary","Yes",63,47,48,"Moderate (60-79%)","Negative (<50%)","Moderate (40-59%)"),
        (98,"Clinical Officer","Female",31,9,"Degree","Mombasa","Private Hospital","No",58,62,33,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (99,"Midwife","Female",37,13,"Diploma","Homa Bay","Health Centre","No",64,61,28,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (100,"Midwife","Male",34,8,"Diploma","Other","Health Centre","No",58,78,5,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (101,"Clinical Officer","Female",31,9,"Degree","Nakuru","Health Centre","No",44,55,27,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (102,"Clinical Officer","Female",34,10,"Degree","Kisumu","Dispensary","No",56,71,29,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (103,"Midwife","Male",36,14,"Diploma","Other","Private Hospital","No",41,57,10,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (104,"Midwife","Female",35,11,"Postgraduate","Kiambu","Public Hospital","No",44,65,30,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (105,"Community Health Worker","Female",33,9,"Certificate","Homa Bay","Dispensary","No",30,31,5,"Poor (<60%)","Negative (<50%)","Inactive (<40%)"),
        (106,"Nurse","Female",32,10,"Diploma","Kiambu","Dispensary","No",38,56,25,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (107,"Clinical Officer","Female",36,13,"Degree","Homa Bay","Health Centre","No",71,65,35,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (108,"Doctor/Medical Officer","Female",39,15,"Postgraduate","Kiambu","Health Centre","No",79,82,55,"Moderate (60-79%)","Positive (≥70%)","Moderate (40-59%)"),
        (109,"Clinical Officer","Female",28,4,"Certificate","Nairobi","Private Hospital","No",53,58,24,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (110,"Nurse","Female",34,10,"Degree","Other","Dispensary","No",53,59,35,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (111,"Midwife","Female",44,21,"Diploma","Kiambu","Health Centre","No",52,62,14,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (112,"Clinical Officer","Female",32,8,"Degree","Kisumu","Public Hospital","No",43,54,31,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (113,"Nurse","Female",33,8,"Degree","Kiambu","Health Centre","No",52,55,18,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (114,"Midwife","Male",26,1,"Degree","Nairobi","Public Hospital","No",34,70,27,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (115,"Midwife","Female",28,6,"Degree","Other","Public Hospital","Yes",50,77,36,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (116,"Community Health Worker","Female",33,11,"Diploma","Kiambu","Dispensary","No",44,66,5,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (117,"Community Health Worker","Female",34,12,"Certificate","Mombasa","Community","No",41,58,6,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (118,"Clinical Officer","Female",38,13,"Degree","Nairobi","Private Hospital","No",48,55,38,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (119,"Nurse","Female",47,21,"Degree","Kisumu","Health Centre","No",56,65,27,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (120,"Clinical Officer","Female",44,18,"Degree","Nairobi","Health Centre","No",58,73,33,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (121,"Clinical Officer","Female",38,13,"Certificate","Kisumu","Public Hospital","No",70,69,32,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (122,"Midwife","Male",47,21,"Diploma","Nairobi","Private Hospital","No",44,54,6,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (123,"Doctor/Medical Officer","Female",33,11,"Degree","Uasin Gishu","Private Hospital","Yes",54,74,51,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (124,"Doctor/Medical Officer","Male",30,6,"Degree","Nairobi","Health Centre","Yes",79,79,42,"Moderate (60-79%)","Positive (≥70%)","Moderate (40-59%)"),
        (125,"Clinical Officer","Male",25,3,"Degree","Mombasa","Public Hospital","Yes",43,71,17,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (126,"Nurse","Female",40,15,"Postgraduate","Nairobi","Health Centre","No",57,47,24,"Poor (<60%)","Negative (<50%)","Inactive (<40%)"),
        (127,"Midwife","Male",22,0,"Diploma","Other","Private Hospital","No",53,72,30,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (128,"Midwife","Male",38,13,"Diploma","Nakuru","Public Hospital","No",27,72,21,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (129,"Doctor/Medical Officer","Female",34,10,"Degree","Nakuru","Public Hospital","No",59,76,50,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (130,"Clinical Officer","Male",28,6,"Degree","Nakuru","Private Hospital","No",50,62,28,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (131,"Nurse","Male",38,13,"Diploma","Homa Bay","Community","No",41,53,45,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (132,"Clinical Officer","Female",32,10,"Diploma","Other","Dispensary","No",67,78,33,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (133,"Nurse","Female",36,11,"Degree","Homa Bay","Private Hospital","No",58,66,17,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (134,"Community Health Worker","Male",41,16,"Certificate","Other","Community","Yes",34,52,30,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (135,"Doctor/Medical Officer","Female",27,2,"Degree","Nairobi","Public Hospital","Yes",66,66,28,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (136,"Nurse","Female",22,0,"Degree","Nairobi","Public Hospital","No",44,35,40,"Poor (<60%)","Negative (<50%)","Moderate (40-59%)"),
        (137,"Doctor/Medical Officer","Female",23,0,"Postgraduate","Nakuru","Public Hospital","Yes",66,77,37,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (138,"Nurse","Male",35,11,"Diploma","Mombasa","Dispensary","Yes",63,77,43,"Moderate (60-79%)","Positive (≥70%)","Moderate (40-59%)"),
        (139,"Clinical Officer","Male",26,1,"Degree","Kiambu","Community","Yes",67,72,29,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (140,"Doctor/Medical Officer","Female",28,2,"Degree","Nairobi","Private Hospital","No",61,64,37,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (141,"Clinical Officer","Male",37,14,"Diploma","Mombasa","Dispensary","No",61,66,37,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (142,"Nurse","Female",36,10,"Diploma","Uasin Gishu","Public Hospital","No",44,64,35,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (143,"Nurse","Female",32,6,"Degree","Kiambu","Health Centre","No",44,56,22,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (144,"Clinical Officer","Female",37,11,"Diploma","Nakuru","Health Centre","No",59,66,48,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (145,"Nurse","Male",31,7,"Diploma","Nairobi","Public Hospital","No",73,69,12,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (146,"Nurse","Female",37,14,"Diploma","Kiambu","Public Hospital","No",55,66,15,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (147,"Midwife","Female",41,15,"Diploma","Kisumu","Public Hospital","No",59,63,9,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (148,"Doctor/Medical Officer","Male",41,15,"Degree","Nakuru","Health Centre","No",68,76,39,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (149,"Nurse","Male",38,12,"Diploma","Nakuru","Public Hospital","No",67,59,31,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (150,"Nurse","Female",43,21,"Certificate","Mombasa","Health Centre","No",43,71,29,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (151,"Midwife","Male",28,4,"Degree","Kisumu","Private Hospital","No",38,66,32,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (152,"Clinical Officer","Female",33,7,"Degree","Nairobi","Health Centre","No",52,65,28,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (153,"Nurse","Female",38,14,"Diploma","Kisumu","Health Centre","Yes",48,62,38,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (154,"Doctor/Medical Officer","Female",37,12,"Degree","Uasin Gishu","Public Hospital","No",66,73,60,"Moderate (60-79%)","Positive (≥70%)","Active (≥60%)"),
        (155,"Clinical Officer","Female",40,16,"Degree","Homa Bay","Health Centre","No",66,65,19,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (156,"Doctor/Medical Officer","Female",35,13,"Postgraduate","Nakuru","Health Centre","No",58,68,53,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (157,"Community Health Worker","Female",37,11,"Certificate","Nairobi","Health Centre","No",37,56,5,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (158,"Clinical Officer","Male",31,8,"Certificate","Other","Public Hospital","Yes",48,59,36,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (159,"Nurse","Male",27,1,"Degree","Homa Bay","Public Hospital","No",50,70,23,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (160,"Clinical Officer","Male",43,17,"Diploma","Kisumu","Health Centre","No",62,73,24,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (161,"Nurse","Female",26,2,"Diploma","Kisumu","Health Centre","No",38,61,40,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (162,"Nurse","Female",40,17,"Degree","Nairobi","Health Centre","No",56,89,25,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (163,"Nurse","Male",43,17,"Diploma","Nairobi","Community","No",67,59,24,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (164,"Nurse","Female",45,21,"Degree","Nairobi","Public Hospital","No",55,58,24,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (165,"Nurse","Female",32,10,"Diploma","Nakuru","Health Centre","No",56,59,19,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (166,"Nurse","Male",36,11,"Diploma","Other","Health Centre","Yes",38,63,40,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (167,"Nurse","Male",28,3,"Degree","Nairobi","Public Hospital","No",61,61,51,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (168,"Clinical Officer","Female",30,8,"Degree","Nakuru","Public Hospital","No",74,74,27,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (169,"Clinical Officer","Female",39,15,"Degree","Nakuru","Public Hospital","No",88,53,21,"Good (≥80%)","Neutral (50-69%)","Inactive (<40%)"),
        (170,"Midwife","Female",33,8,"Degree","Mombasa","Public Hospital","No",58,63,40,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (171,"Doctor/Medical Officer","Female",24,1,"Diploma","Nakuru","Private Hospital","Yes",71,64,40,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (172,"Nurse","Female",29,4,"Diploma","Homa Bay","Public Hospital","No",57,77,20,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (173,"Community Health Worker","Female",39,16,"Certificate","Uasin Gishu","Community","No",44,64,15,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (174,"Doctor/Medical Officer","Female",38,16,"Degree","Kiambu","Dispensary","No",61,69,36,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (175,"Nurse","Female",25,1,"Diploma","Homa Bay","Private Hospital","No",65,55,22,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (176,"Nurse","Male",42,17,"Degree","Homa Bay","Health Centre","No",23,73,15,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (177,"Doctor/Medical Officer","Female",26,0,"Postgraduate","Nakuru","Public Hospital","No",62,61,45,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (178,"Doctor/Medical Officer","Female",32,8,"Postgraduate","Nairobi","Health Centre","No",57,69,36,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (179,"Nurse","Female",35,12,"Diploma","Nairobi","Private Hospital","Yes",31,66,24,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (180,"Nurse","Female",42,19,"Diploma","Kiambu","Public Hospital","No",58,51,10,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (181,"Clinical Officer","Female",41,19,"Diploma","Other","Health Centre","Yes",81,67,57,"Good (≥80%)","Neutral (50-69%)","Moderate (40-59%)"),
        (182,"Nurse","Male",44,19,"Degree","Nairobi","Health Centre","No",49,42,10,"Poor (<60%)","Negative (<50%)","Inactive (<40%)"),
        (183,"Clinical Officer","Female",29,6,"Postgraduate","Homa Bay","Community","Yes",51,58,26,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (184,"Clinical Officer","Female",33,7,"Diploma","Uasin Gishu","Health Centre","No",67,55,45,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (185,"Nurse","Female",26,4,"Degree","Kisumu","Dispensary","No",56,70,42,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (186,"Clinical Officer","Male",35,9,"Degree","Nakuru","Public Hospital","No",65,69,35,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (187,"Nurse","Female",22,0,"Diploma","Uasin Gishu","Health Centre","No",40,69,29,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (188,"Nurse","Male",29,5,"Degree","Other","Private Hospital","No",46,76,23,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (189,"Nurse","Female",28,5,"Diploma","Kiambu","Community","No",50,76,12,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (190,"Clinical Officer","Female",28,3,"Diploma","Mombasa","Health Centre","No",72,63,34,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (191,"Clinical Officer","Female",31,6,"Degree","Kiambu","Health Centre","No",58,74,36,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (192,"Doctor/Medical Officer","Female",44,19,"Postgraduate","Mombasa","Public Hospital","No",73,77,47,"Moderate (60-79%)","Positive (≥70%)","Moderate (40-59%)"),
        (193,"Nurse","Female",25,2,"Degree","Nairobi","Public Hospital","No",50,78,9,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (194,"Nurse","Male",48,25,"Degree","Mombasa","Community","Yes",58,84,19,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (195,"Midwife","Male",31,8,"Diploma","Homa Bay","Health Centre","No",43,65,19,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (196,"Nurse","Female",33,11,"Degree","Other","Public Hospital","No",47,70,14,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (197,"Nurse","Female",38,15,"Certificate","Mombasa","Health Centre","No",55,72,51,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (198,"Nurse","Female",43,20,"Diploma","Nairobi","Public Hospital","No",50,71,30,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (199,"Nurse","Female",28,5,"Degree","Mombasa","Private Hospital","Yes",63,44,19,"Moderate (60-79%)","Negative (<50%)","Inactive (<40%)"),
        (200,"Midwife","Male",33,7,"Certificate","Mombasa","Health Centre","No",58,81,55,"Poor (<60%)","Positive (≥70%)","Moderate (40-59%)"),
        (201,"Community Health Worker","Female",30,7,"Certificate","Other","Community","No",39,49,20,"Poor (<60%)","Negative (<50%)","Inactive (<40%)"),
        (202,"Nurse","Female",35,13,"Diploma","Nairobi","Health Centre","Yes",45,54,14,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (203,"Doctor/Medical Officer","Male",34,9,"Postgraduate","Kiambu","Public Hospital","Yes",60,70,23,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (204,"Midwife","Female",32,8,"Degree","Uasin Gishu","Health Centre","No",54,69,5,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (205,"Nurse","Male",46,24,"Degree","Nairobi","Public Hospital","No",53,79,21,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (206,"Midwife","Male",34,11,"Certificate","Nairobi","Private Hospital","No",41,72,27,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (207,"Nurse","Male",24,1,"Diploma","Nakuru","Private Hospital","No",79,62,49,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (208,"Midwife","Female",27,1,"Diploma","Kisumu","Public Hospital","No",54,65,48,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (209,"Doctor/Medical Officer","Female",22,0,"Degree","Nairobi","Health Centre","No",69,77,52,"Moderate (60-79%)","Positive (≥70%)","Moderate (40-59%)"),
        (210,"Nurse","Male",42,20,"Diploma","Other","Private Hospital","Yes",46,55,13,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (211,"Midwife","Female",22,0,"Degree","Nakuru","Dispensary","No",55,57,29,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (212,"Doctor/Medical Officer","Female",32,9,"Postgraduate","Other","Private Hospital","Yes",61,74,31,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (213,"Nurse","Female",36,13,"Degree","Mombasa","Public Hospital","Yes",57,51,34,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (214,"Midwife","Female",38,15,"Diploma","Nairobi","Public Hospital","No",47,72,24,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (215,"Nurse","Female",27,2,"Certificate","Other","Health Centre","No",63,71,11,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (216,"Clinical Officer","Female",42,17,"Diploma","Mombasa","Public Hospital","No",29,58,33,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (217,"Clinical Officer","Female",46,22,"Diploma","Kiambu","Health Centre","No",62,74,26,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (218,"Nurse","Female",50,26,"Degree","Nairobi","Private Hospital","No",54,69,18,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (219,"Nurse","Male",26,2,"Diploma","Other","Public Hospital","No",35,72,19,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (220,"Community Health Worker","Male",44,19,"Degree","Nairobi","Health Centre","No",64,53,10,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (221,"Doctor/Medical Officer","Male",32,6,"Degree","Mombasa","Health Centre","Yes",70,64,49,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (222,"Doctor/Medical Officer","Male",22,0,"Postgraduate","Nakuru","Private Hospital","No",74,70,49,"Moderate (60-79%)","Positive (≥70%)","Moderate (40-59%)"),
        (223,"Doctor/Medical Officer","Male",25,0,"Degree","Other","Private Hospital","No",63,67,32,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (224,"Nurse","Male",26,2,"Degree","Nairobi","Dispensary","No",30,64,23,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (225,"Clinical Officer","Male",30,4,"Certificate","Kiambu","Private Hospital","No",64,72,28,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (226,"Community Health Worker","Female",34,10,"Certificate","Nairobi","Community","No",38,35,13,"Poor (<60%)","Negative (<50%)","Inactive (<40%)"),
        (227,"Clinical Officer","Male",36,10,"Diploma","Other","Public Hospital","No",60,77,14,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (228,"Clinical Officer","Female",24,0,"Diploma","Homa Bay","Health Centre","No",62,66,41,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (229,"Nurse","Female",28,4,"Certificate","Kiambu","Public Hospital","Yes",41,66,25,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (230,"Nurse","Female",29,3,"Diploma","Other","Community","No",66,75,46,"Moderate (60-79%)","Positive (≥70%)","Moderate (40-59%)"),
        (231,"Nurse","Female",43,18,"Diploma","Mombasa","Private Hospital","No",53,74,35,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (232,"Nurse","Male",40,18,"Diploma","Nairobi","Private Hospital","No",51,65,30,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (233,"Nurse","Female",27,3,"Diploma","Nairobi","Public Hospital","No",54,69,21,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (234,"Nurse","Female",24,0,"Degree","Kisumu","Public Hospital","No",60,55,35,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (235,"Clinical Officer","Female",37,12,"Diploma","Kisumu","Public Hospital","No",58,72,27,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (236,"Nurse","Female",22,0,"Diploma","Kisumu","Dispensary","No",42,55,5,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (237,"Clinical Officer","Male",32,9,"Degree","Nairobi","Health Centre","No",43,56,45,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (238,"Midwife","Male",27,5,"Diploma","Uasin Gishu","Public Hospital","No",46,55,32,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (239,"Community Health Worker","Female",25,0,"Certificate","Other","Community","Yes",39,65,18,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (240,"Doctor/Medical Officer","Male",32,7,"Degree","Mombasa","Health Centre","Yes",72,64,44,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (241,"Nurse","Female",34,10,"Degree","Mombasa","Public Hospital","No",52,57,41,"Poor (<60%)","Neutral (50-69%)","Moderate (40-59%)"),
        (242,"Doctor/Medical Officer","Female",23,0,"Degree","Mombasa","Public Hospital","Yes",71,66,41,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (243,"Nurse","Male",39,13,"Diploma","Kiambu","Health Centre","No",53,68,22,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (244,"Nurse","Male",26,3,"Degree","Mombasa","Community","No",63,62,46,"Moderate (60-79%)","Neutral (50-69%)","Moderate (40-59%)"),
        (245,"Nurse","Male",30,6,"Degree","Kisumu","Private Hospital","No",55,62,34,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (246,"Nurse","Female",38,16,"Diploma","Other","Dispensary","No",45,62,17,"Poor (<60%)","Neutral (50-69%)","Inactive (<40%)"),
        (247,"Doctor/Medical Officer","Female",27,5,"Postgraduate","Nairobi","Public Hospital","No",57,75,21,"Poor (<60%)","Positive (≥70%)","Inactive (<40%)"),
        (248,"Nurse","Female",41,18,"Diploma","Nairobi","Private Hospital","No",63,69,31,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
        (249,"Nurse","Female",22,0,"Certificate","Mombasa","Public Hospital","No",65,78,34,"Moderate (60-79%)","Positive (≥70%)","Inactive (<40%)"),
        (250,"Clinical Officer","Female",40,15,"Diploma","Homa Bay","Health Centre","Yes",63,66,5,"Moderate (60-79%)","Neutral (50-69%)","Inactive (<40%)"),
    ]
    cols = ["ID","Profession","Sex","Age","Years of Experience","Education Level",
            "County","Facility Setting","Received BC Training",
            "Knowledge Score (%)","Attitude Score (%)","Practice Score (%)",
            "Knowledge Category","Attitude Category","Practice Category"]
    return pd.DataFrame(rows, columns=cols)


df_full = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.markdown("## 🎗️ KAP Oncology Dashboard")
st.sidebar.markdown("**Kenya · Breast Cancer · n=250**")
st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

professions  = ["All"] + sorted(df_full["Profession"].unique())
counties     = ["All"] + sorted(df_full["County"].unique())
facilities   = ["All"] + sorted(df_full["Facility Setting"].unique())
sexes        = ["All"] + sorted(df_full["Sex"].unique())
training_opt = ["All", "Yes", "No"]

sel_prof     = st.sidebar.multiselect("Profession", professions[1:], default=professions[1:])
sel_county   = st.sidebar.selectbox("County", counties)
sel_facility = st.sidebar.selectbox("Facility Setting", facilities)
sel_sex      = st.sidebar.selectbox("Sex", sexes)
sel_training = st.sidebar.selectbox("Received BC Training", training_opt)

# Apply filters
df = df_full.copy()
if sel_prof:
    df = df[df["Profession"].isin(sel_prof)]
if sel_county != "All":
    df = df[df["County"] == sel_county]
if sel_facility != "All":
    df = df[df["Facility Setting"] == sel_facility]
if sel_sex != "All":
    df = df[df["Sex"] == sel_sex]
if sel_training != "All":
    df = df[df["Received BC Training"] == sel_training]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Showing {len(df)} of {len(df_full)} respondents**")
st.sidebar.markdown("---")
st.sidebar.markdown("*Synthetic dataset calibrated from published Kenya KAP literature (2013–2024)*")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🎗️ KAP Dashboard — Oncology (Breast Cancer)")
st.markdown("#### Knowledge, Attitudes & Practices of Health Practitioners · Kenya")
st.markdown("---")

# ── KPI cards ─────────────────────────────────────────────────────────────────
k_mean = df["Knowledge Score (%)"].mean()
a_mean = df["Attitude Score (%)"].mean()
p_mean = df["Practice Score (%)"].mean()
n      = len(df)

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"""<div class="metric-card knowledge">
  <p>Respondents</p><h2>{n}</h2></div>""", unsafe_allow_html=True)
c2.markdown(f"""<div class="metric-card knowledge">
  <p>Mean Knowledge Score</p><h2>{k_mean:.1f}%</h2></div>""", unsafe_allow_html=True)
c3.markdown(f"""<div class="metric-card attitude">
  <p>Mean Attitude Score</p><h2>{a_mean:.1f}%</h2></div>""", unsafe_allow_html=True)
c4.markdown(f"""<div class="metric-card practice">
  <p>Mean Practice Score</p><h2>{p_mean:.1f}%</h2></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["📊 Overview", "👥 Demographics", "🧠 Knowledge",
                "💬 Attitudes", "🏥 Practices", "🔗 KAP Relationships", "📋 Data Table"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    st.subheader("KAP Score Overview by Profession")

    prof_summary = (df.groupby("Profession")[
        ["Knowledge Score (%)","Attitude Score (%)","Practice Score (%)"]]
        .mean().round(1).reset_index())

    fig_bar = px.bar(
        prof_summary.melt(id_vars="Profession", var_name="Domain", value_name="Mean Score (%)"),
        x="Profession", y="Mean Score (%)", color="Domain", barmode="group",
        color_discrete_map={
            "Knowledge Score (%)": "#2196F3",
            "Attitude Score (%)":  "#4CAF50",
            "Practice Score (%)":  "#FF9800",
        },
        template="plotly_white",
        title="Mean KAP Scores by Profession"
    )
    fig_bar.update_layout(xaxis_tickangle=-20, legend_title_text="Domain")
    st.plotly_chart(fig_bar, use_container_width=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("**Score Distribution (Box Plot)**")
        fig_box = go.Figure()
        for domain, colour in KAP_COLOURS.items():
            fig_box.add_trace(go.Box(
                y=df[domain], name=domain.replace(" (%)", ""),
                marker_color=colour, boxmean=True
            ))
        fig_box.update_layout(template="plotly_white", showlegend=False,
                              yaxis_title="Score (%)")
        st.plotly_chart(fig_box, use_container_width=True)

    with col_r:
        st.markdown("**Category Breakdown — Knowledge**")
        kcat = df["Knowledge Category"].value_counts().reset_index()
        kcat.columns = ["Category", "Count"]
        order = ["Poor (<60%)", "Moderate (60-79%)", "Good (≥80%)"]
        kcat["Category"] = pd.Categorical(kcat["Category"], categories=order, ordered=True)
        kcat = kcat.sort_values("Category")
        fig_pie = px.pie(kcat, names="Category", values="Count",
                         color_discrete_sequence=["#ef5350","#FFA726","#66BB6A"],
                         template="plotly_white")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("**Summary Statistics**")
    summary = df[["Knowledge Score (%)","Attitude Score (%)","Practice Score (%)"]].describe().T
    summary.index = ["Knowledge","Attitude","Practice"]
    summary = summary[["mean","std","min","25%","50%","75%","max"]].round(1)
    st.dataframe(summary, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — DEMOGRAPHICS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.subheader("Respondent Demographics")
    col1, col2 = st.columns(2)

    with col1:
        prof_counts = df["Profession"].value_counts().reset_index()
        prof_counts.columns = ["Profession", "Count"]
        fig_prof = px.bar(prof_counts, x="Count", y="Profession", orientation="h",
                          color="Profession",
                          color_discrete_map=COLOURS,
                          template="plotly_white", title="Respondents by Profession")
        fig_prof.update_layout(showlegend=False)
        st.plotly_chart(fig_prof, use_container_width=True)

    with col2:
        sex_counts = df["Sex"].value_counts().reset_index()
        sex_counts.columns = ["Sex","Count"]
        fig_sex = px.pie(sex_counts, names="Sex", values="Count",
                         color_discrete_sequence=["#7E57C2","#EC407A"],
                         template="plotly_white", title="Sex Distribution")
        st.plotly_chart(fig_sex, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig_age = px.histogram(df, x="Age", nbins=15, color_discrete_sequence=["#26C6DA"],
                               template="plotly_white", title="Age Distribution",
                               labels={"Age":"Age (years)"})
        fig_age.update_layout(bargap=0.05)
        st.plotly_chart(fig_age, use_container_width=True)

    with col4:
        edu_order = ["Certificate","Diploma","Degree","Postgraduate"]
        edu_counts = (df["Education Level"].value_counts()
                      .reindex(edu_order, fill_value=0).reset_index())
        edu_counts.columns = ["Education Level","Count"]
        fig_edu = px.bar(edu_counts, x="Education Level", y="Count",
                         color="Education Level",
                         color_discrete_sequence=px.colors.qualitative.Set2,
                         template="plotly_white", title="Education Level")
        fig_edu.update_layout(showlegend=False)
        st.plotly_chart(fig_edu, use_container_width=True)

    col5, col6 = st.columns(2)

    with col5:
        county_counts = df["County"].value_counts().reset_index()
        county_counts.columns = ["County","Count"]
        fig_county = px.bar(county_counts, x="County", y="Count",
                            color_discrete_sequence=["#42A5F5"],
                            template="plotly_white", title="Respondents by County")
        fig_county.update_layout(xaxis_tickangle=-30)
        st.plotly_chart(fig_county, use_container_width=True)

    with col6:
        fac_counts = df["Facility Setting"].value_counts().reset_index()
        fac_counts.columns = ["Facility Setting","Count"]
        fig_fac = px.pie(fac_counts, names="Facility Setting", values="Count",
                         template="plotly_white", title="Facility Settings",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_fac, use_container_width=True)

    st.markdown("**Training Status by Profession**")
    train_prof = (df.groupby(["Profession","Received BC Training"])
                  .size().reset_index(name="Count"))
    fig_train = px.bar(train_prof, x="Profession", y="Count",
                       color="Received BC Training",
                       color_discrete_map={"Yes":"#66BB6A","No":"#EF5350"},
                       barmode="group", template="plotly_white",
                       title="BC Training Received by Profession")
    fig_train.update_layout(xaxis_tickangle=-20)
    st.plotly_chart(fig_train, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — KNOWLEDGE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.subheader("Knowledge Scores")
    col1, col2 = st.columns(2)

    with col1:
        fig_khist = px.histogram(df, x="Knowledge Score (%)", nbins=20,
                                 color_discrete_sequence=["#2196F3"],
                                 template="plotly_white",
                                 title="Knowledge Score Distribution")
        fig_khist.add_vline(x=df["Knowledge Score (%)"].mean(), line_dash="dash",
                            line_color="red", annotation_text="Mean")
        st.plotly_chart(fig_khist, use_container_width=True)

    with col2:
        kbox = px.box(df, x="Profession", y="Knowledge Score (%)",
                      color="Profession", color_discrete_map=COLOURS,
                      template="plotly_white", title="Knowledge Score by Profession")
        kbox.update_layout(showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(kbox, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        k_by_edu = (df.groupby("Education Level")["Knowledge Score (%)"]
                    .mean().reindex(["Certificate","Diploma","Degree","Postgraduate"])
                    .reset_index())
        fig_kedu = px.bar(k_by_edu, x="Education Level", y="Knowledge Score (%)",
                          color_discrete_sequence=["#1565C0"],
                          template="plotly_white",
                          title="Mean Knowledge Score by Education Level")
        st.plotly_chart(fig_kedu, use_container_width=True)

    with col4:
        k_train = df.groupby("Received BC Training")["Knowledge Score (%)"].mean().reset_index()
        fig_ktrain = px.bar(k_train, x="Received BC Training", y="Knowledge Score (%)",
                            color="Received BC Training",
                            color_discrete_map={"Yes":"#66BB6A","No":"#EF5350"},
                            template="plotly_white",
                            title="Mean Knowledge Score: Trained vs Untrained")
        fig_ktrain.update_layout(showlegend=False)
        st.plotly_chart(fig_ktrain, use_container_width=True)

    st.markdown("**Knowledge Category Distribution by Profession**")
    kcat_prof = (df.groupby(["Profession","Knowledge Category"])
                 .size().reset_index(name="Count"))
    fig_kcat = px.bar(kcat_prof, x="Profession", y="Count",
                      color="Knowledge Category",
                      color_discrete_map={
                          "Poor (<60%)":       "#EF5350",
                          "Moderate (60-79%)": "#FFA726",
                          "Good (≥80%)":       "#66BB6A"
                      },
                      template="plotly_white",
                      title="Knowledge Category by Profession")
    fig_kcat.update_layout(xaxis_tickangle=-20)
    st.plotly_chart(fig_kcat, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — ATTITUDES
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    st.subheader("Attitude Scores")
    col1, col2 = st.columns(2)

    with col1:
        fig_ahist = px.histogram(df, x="Attitude Score (%)", nbins=20,
                                 color_discrete_sequence=["#4CAF50"],
                                 template="plotly_white",
                                 title="Attitude Score Distribution")
        fig_ahist.add_vline(x=df["Attitude Score (%)"].mean(), line_dash="dash",
                            line_color="red", annotation_text="Mean")
        st.plotly_chart(fig_ahist, use_container_width=True)

    with col2:
        abox = px.box(df, x="Profession", y="Attitude Score (%)",
                      color="Profession", color_discrete_map=COLOURS,
                      template="plotly_white", title="Attitude Score by Profession")
        abox.update_layout(showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(abox, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        acat_counts = df["Attitude Category"].value_counts().reset_index()
        acat_counts.columns = ["Category","Count"]
        fig_acat = px.pie(acat_counts, names="Category", values="Count",
                          color_discrete_map={
                              "Negative (<50%)":  "#EF5350",
                              "Neutral (50-69%)": "#FFA726",
                              "Positive (≥70%)":  "#66BB6A"
                          },
                          template="plotly_white", title="Attitude Category Distribution")
        st.plotly_chart(fig_acat, use_container_width=True)

    with col4:
        a_sex = df.groupby(["Sex","Attitude Category"]).size().reset_index(name="Count")
        fig_asex = px.bar(a_sex, x="Sex", y="Count", color="Attitude Category",
                          color_discrete_map={
                              "Negative (<50%)":  "#EF5350",
                              "Neutral (50-69%)": "#FFA726",
                              "Positive (≥70%)":  "#66BB6A"
                          },
                          template="plotly_white", title="Attitude Category by Sex")
        st.plotly_chart(fig_asex, use_container_width=True)

    st.markdown("**Mean Attitude Score by County**")
    a_county = df.groupby("County")["Attitude Score (%)"].mean().reset_index().sort_values("Attitude Score (%)", ascending=False)
    fig_acounty = px.bar(a_county, x="County", y="Attitude Score (%)",
                         color_discrete_sequence=["#388E3C"],
                         template="plotly_white", title="Mean Attitude Score by County")
    fig_acounty.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig_acounty, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — PRACTICES
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.subheader("Practice Scores")
    col1, col2 = st.columns(2)

    with col1:
        fig_phist = px.histogram(df, x="Practice Score (%)", nbins=20,
                                 color_discrete_sequence=["#FF9800"],
                                 template="plotly_white",
                                 title="Practice Score Distribution")
        fig_phist.add_vline(x=df["Practice Score (%)"].mean(), line_dash="dash",
                            line_color="red", annotation_text="Mean")
        st.plotly_chart(fig_phist, use_container_width=True)

    with col2:
        pbox = px.box(df, x="Profession", y="Practice Score (%)",
                      color="Profession", color_discrete_map=COLOURS,
                      template="plotly_white", title="Practice Score by Profession")
        pbox.update_layout(showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(pbox, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        pcat_counts = df["Practice Category"].value_counts().reset_index()
        pcat_counts.columns = ["Category","Count"]
        fig_pcat = px.pie(pcat_counts, names="Category", values="Count",
                          color_discrete_map={
                              "Inactive (<40%)":    "#EF5350",
                              "Moderate (40-59%)":  "#FFA726",
                              "Active (≥60%)":      "#66BB6A"
                          },
                          template="plotly_white", title="Practice Category Distribution")
        st.plotly_chart(fig_pcat, use_container_width=True)

    with col4:
        p_fac = df.groupby("Facility Setting")["Practice Score (%)"].mean().reset_index().sort_values("Practice Score (%)", ascending=False)
        fig_pfac = px.bar(p_fac, x="Facility Setting", y="Practice Score (%)",
                          color_discrete_sequence=["#E65100"],
                          template="plotly_white", title="Mean Practice Score by Facility")
        fig_pfac.update_layout(xaxis_tickangle=-20)
        st.plotly_chart(fig_pfac, use_container_width=True)

    st.markdown("**Practice Score vs Years of Experience**")
    fig_pexp = px.scatter(df, x="Years of Experience", y="Practice Score (%)",
                          color="Profession", color_discrete_map=COLOURS,
                          trendline="ols", template="plotly_white",
                          title="Practice Score vs Years of Experience",
                          hover_data=["Education Level","County"])
    st.plotly_chart(fig_pexp, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — KAP RELATIONSHIPS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.subheader("Relationships Between K, A & P")

    col1, col2 = st.columns(2)

    with col1:
        fig_kp = px.scatter(df, x="Knowledge Score (%)", y="Practice Score (%)",
                            color="Profession", color_discrete_map=COLOURS,
                            trendline="ols", template="plotly_white",
                            title="Knowledge vs Practice",
                            hover_data=["Sex","County","Education Level"])
        st.plotly_chart(fig_kp, use_container_width=True)

    with col2:
        fig_ap = px.scatter(df, x="Attitude Score (%)", y="Practice Score (%)",
                            color="Profession", color_discrete_map=COLOURS,
                            trendline="ols", template="plotly_white",
                            title="Attitude vs Practice",
                            hover_data=["Sex","County","Education Level"])
        st.plotly_chart(fig_ap, use_container_width=True)

    st.markdown("**Correlation Matrix**")
    corr = df[["Knowledge Score (%)","Attitude Score (%)","Practice Score (%)","Age","Years of Experience"]].corr().round(2)
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                         zmin=-1, zmax=1, template="plotly_white",
                         title="Pearson Correlation Matrix")
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("**KAP 3D Scatter**")
    fig_3d = px.scatter_3d(df, x="Knowledge Score (%)", y="Attitude Score (%)",
                           z="Practice Score (%)", color="Profession",
                           color_discrete_map=COLOURS, opacity=0.7,
                           template="plotly_white",
                           title="3D View: Knowledge × Attitude × Practice",
                           hover_data=["Sex","County"])
    fig_3d.update_traces(marker=dict(size=4))
    st.plotly_chart(fig_3d, use_container_width=True)

    st.markdown("**Impact of BC Training on KAP**")
    train_kap = (df.groupby("Received BC Training")[
        ["Knowledge Score (%)","Attitude Score (%)","Practice Score (%)"]]
        .mean().round(1).reset_index())
    fig_train = px.bar(
        train_kap.melt(id_vars="Received BC Training", var_name="Domain", value_name="Mean Score (%)"),
        x="Domain", y="Mean Score (%)", color="Received BC Training",
        color_discrete_map={"Yes":"#66BB6A","No":"#EF5350"},
        barmode="group", template="plotly_white",
        title="Mean KAP Scores: Trained vs Untrained"
    )
    st.plotly_chart(fig_train, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — DATA TABLE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    st.subheader("Filtered Dataset")
    st.markdown(f"Showing **{len(df)}** rows")
    st.dataframe(df.reset_index(drop=True), use_container_width=True, height=500)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download filtered data as CSV",
        data=csv,
        file_name="kap_filtered.csv",
        mime="text/csv"
    )