import streamlit as st
import pandas as pd
import math
from datetime import datetime, date, timedelta
import time

st.set_page_config(page_title="Run Tools", layout="wide", initial_sidebar_state="expanded")

# --- Theme toggle ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.sidebar.toggle("🌗 Dark Mode", value=st.session_state.dark_mode, key="dark_toggle") != st.session_state.dark_mode:
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

# --- Style ---
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    body, div, .stApp {
        background-color: #1e1e1e;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #2c2c2c;
    }
    div.block-container {
        padding: 0.5rem 1rem !important;
        font-size: 15px;
        max-width: 900px;
        margin: auto;
    }
    .metric-container {
        background-color: #333;
    }
    .stButton>button {
        color: white !important;
        background-color: #3a3a3a !important;
        border: 1px solid #666 !important;
        width: 100% !important;
        padding: 0.75rem 1.5rem !important;
    }
    .stCheckbox>div>label {
        color: white !important;
    }
    section[data-testid="collapsedControl"] svg {
        fill: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    div.block-container {
        padding: 0.5rem 1rem !important;
        font-size: 15px;
        max-width: 900px;
        margin: auto;
    }
    h1, h2, h3, h4 {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    hr {
        margin: 0.5rem 0;
    }
    .metric-container {
        padding: 0.5rem 1rem;
        border-radius: 0.75rem;
        background-color: #f3f4f6;
        margin-bottom: 0.5rem;
    }
    .sidebar-options {
        background-color: #eef2f7;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100% !important;
        padding: 0.75rem 1.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Navigation State ---
if "main_page" not in st.session_state:
    st.session_state.main_page = "home"

# --- Home Page ---
def show_home():
    st.title("🏁 Welcome to Run Tools")
    st.write("Choose a tool below:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📏 Running Pace Calculator"):
            st.session_state.main_page = "pace"
        if st.button("💧 Hydration Planner"):
            st.session_state.main_page = "hydration"
        if st.button("☁️ Run Readiness Score"):
            st.session_state.main_page = "score"
        if st.button("📅 Race Countdown"):
            st.session_state.main_page = "countdown"
    with col2:
        if st.button("👟 Shoe Mileage Tracker"):
            st.session_state.main_page = "shoes"
        if st.button("🧠 Mental Readiness Log"):
            st.session_state.main_page = "mental"
        if st.button("🛌 Sleep Quality Tracker"):
            st.session_state.main_page = "sleep"
        if st.button("🦵 Injury Tracker"):
            st.session_state.main_page = "injury"

# --- Functional Pages ---
def show_pace_calculator():
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.update({"main_page": "home"}))
    st.subheader("📏 Running Pace Calculator")
    goal_distance = st.number_input("Target Distance (km)", min_value=1.0, step=0.1)
    lap_length = st.number_input("Lap Length (km)", min_value=0.1, step=0.01)
    goal_time = st.time_input("Goal Time")
    if goal_distance and lap_length and goal_time:
        total_seconds = goal_time.hour * 3600 + goal_time.minute * 60 + goal_time.second
        pace_per_km = total_seconds / goal_distance
        num_full_laps = int(goal_distance // lap_length)
        leftover = goal_distance - (num_full_laps * lap_length)

        st.write("### Breakdown:")
        for lap in range(1, num_full_laps + 1):
            st.write(f"Lap {lap}: {lap_length:.2f} km @ {pace_per_km:.2f} sec/km = {pace_per_km * lap_length:.1f} sec")
        if leftover > 0:
            st.write(f"Lap {num_full_laps + 1}: {leftover:.2f} km @ {pace_per_km:.2f} sec/km = {pace_per_km * leftover:.1f} sec")

def show_hydration_planner():
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.update({"main_page": "home"}))
    st.subheader("💧 Hydration Planner")
    duration = st.slider("Run Duration (minutes)", 10, 180, 60)
    temperature = st.slider("Temperature (°C)", 10, 40, 25)
    intensity = st.selectbox("Intensity", ["Low", "Medium", "High"])

    multiplier = {"Low": 0.4, "Medium": 0.6, "High": 0.8}[intensity]
    water_needed = duration * multiplier * (1 + (temperature - 20) * 0.03)
    st.metric("Recommended Water Intake", f"{water_needed:.0f} ml")

def show_mental_log():
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.update({"main_page": "home"}))
    st.subheader("🧠 Mental Readiness Log")
    mood = st.slider("How motivated are you today?", 1, 10, 5)
    stress = st.slider("Stress level", 1, 10, 5)
    note = st.text_area("Mental Notes")
    if st.button("📝 Save Mental Log"):
        st.success("Mental state logged!")

def show_sleep_tracker():
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.update({"main_page": "home"}))
    st.subheader("🛌 Sleep Quality Tracker")
    hours = st.slider("Hours Slept", 0, 12, 7)
    quality = st.selectbox("Sleep Quality", ["Poor", "Fair", "Good", "Excellent"])
    if st.button("🛏️ Log Sleep"):
        st.success(f"Sleep logged: {hours}h - {quality}")

def show_race_countdown():
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.update({"main_page": "home"}))
    st.subheader("📅 Race Countdown")
    race_date = st.date_input("Select your race date:", value=date.today())
    race_time = st.time_input("Select race time:", value=datetime.now().time())
    race_datetime = datetime.combine(race_date, race_time)

    placeholder = st.empty()
    while True:
        now = datetime.now()
        delta = race_datetime - now
        if delta.total_seconds() < 0:
            placeholder.warning("⚠️ Race date is in the past.")
            break
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        placeholder.markdown(f"""
        <h1 style='text-align:center; font-size:3rem;'>🏁 {days} Days {hours:02d}:{minutes:02d}:{seconds:02d}</h1>
        """, unsafe_allow_html=True)
        time.sleep(1)

def show_injury_tracker():
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.update({"main_page": "home"}))
    st.subheader("🦵 Injury Tracker")
    injury_type = st.selectbox("Injury Type", ["None", "Knee", "Shin", "Ankle", "Hip", "Other"])
    severity = st.slider("Severity (1=minor, 10=severe)", 1, 10, 3)
    notes = st.text_area("Additional Notes")
    if st.button("📝 Save Injury Log"):
        st.success("Injury info saved!")

# --- Router ---
page_functions = {
    "home": show_home,
    "pace": show_pace_calculator,
    "hydration": show_hydration_planner,
    "score": lambda: st.write("☁️ Placeholder for Readiness Score"),
    "shoes": lambda: st.write("👟 Placeholder for Shoe Tracker"),
    "mental": show_mental_log,
    "sleep": show_sleep_tracker,
    "countdown": show_race_countdown,
    "injury": show_injury_tracker,
}

page_functions[st.session_state.main_page]()
