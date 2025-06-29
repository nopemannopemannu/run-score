import streamlit as s
import pandas as p
import math as m
from datetime import datetime as d, date as dt, timedelta as td
import time as t

s.set_page_config(page_title="Run Tools", layout="wide", initial_sidebar_state="expanded")

if "dm" not in s.session_state:
    s.session_state.dm = False

if s.sidebar.toggle("🌗 Dark Mode", value=s.session_state.dm, key="dark_toggle") != s.session_state.dm:
    s.session_state.dm = not s.session_state.dm
    s.rerun()

if s.session_state.dm:
    s.markdown("""
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
    s.markdown("""
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

if "pg" not in s.session_state:
    s.session_state.pg = "home"

def h():
    s.title("🏁 Welcome to Run Tools")
    s.write("Choose a tool below:")
    c1, c2 = s.columns(2)
    with c1:
        s.button("📏 Running Pace Calculator", on_click=lambda: s.session_state.update({"pg": "pace"}))
        s.button("💧 Hydration Planner", on_click=lambda: s.session_state.update({"pg": "hydration"}))
        s.button("☁️ Run Readiness Score", on_click=lambda: s.session_state.update({"pg": "score"}))
        s.button("🗕️ Race Countdown", on_click=lambda: s.session_state.update({"pg": "countdown"}))
    with c2:
        s.button("👟 Shoe Mileage Tracker", on_click=lambda: s.session_state.update({"pg": "shoes"}))
        s.button("🧠 Mental Readiness Log", on_click=lambda: s.session_state.update({"pg": "mental"}))
        s.button("🛌 Sleep Quality Tracker", on_click=lambda: s.session_state.update({"pg": "sleep"}))
        s.button("🦵 Injury Tracker", on_click=lambda: s.session_state.update({"pg": "injury"}))
        s.button("📖 Logs", on_click=lambda: s.session_state.update({"pg": "shoelog"}))

def pace():
    s.button("⬅️ Back to Home", on_click=lambda: s.session_state.update({"pg": "home"}))
    s.subheader("📏 Running Pace Calculator")
    distance = s.number_input("Goal Distance (km):", min_value=0.5, value=5.0, step=0.1)
    time_min = s.number_input("Target Time (min):", min_value=1, value=30)
    lap_len = s.number_input("Track Lap Distance (km):", min_value=0.1, value=1.7)

    if s.button("📊 Calculate Pace"):
        target_sec = time_min * 60
        pace_sec = target_sec / distance
        splits = []
        total = 0.0
        while total + lap_len <= distance - 0.01:
            splits.append((lap_len, pace_sec * lap_len))
            total += lap_len
        final_lap = distance - total
        if final_lap > 0:
            splits.append((final_lap, pace_sec * final_lap))

        s.success(f"Target pace: {m.floor(pace_sec//60)}:{int(pace_sec%60):02d} per km")
        for i, (d_km, sec) in enumerate(splits):
            s.markdown(f"**Lap {i+1}:** {d_km:.2f} km → {m.floor(sec//60)}:{int(sec%60):02d}")

def mental():
    s.button("⬅️ Back to Home", on_click=lambda: s.session_state.update({"pg": "home"}))
    s.subheader("🧠 Mental Readiness Log")
    mood = s.slider("Mood Level (0-10)", 0, 10, 5)
    motivation = s.slider("Motivation Level (0-10)", 0, 10, 5)
    notes = s.text_area("Notes")
    if s.button("✉️ Submit Mental Log"):
        log = {"Date": str(d.today()), "Mood": mood, "Motivation": motivation, "Notes": notes}
        if "mental_logs" not in s.session_state:
            s.session_state.mental_logs = []
        s.session_state.mental_logs.append(log)
        s.success("Mental log saved.")

    if "mental_logs" in s.session_state and s.session_state.mental_logs:
        s.markdown("### 📘 Past Mental Logs")
        df = p.DataFrame(s.session_state.mental_logs)
        s.dataframe(df, use_container_width=True)

def sleep():
    s.button("⬅️ Back to Home", on_click=lambda: s.session_state.update({"pg": "home"}))
    s.subheader("🛌 Sleep Quality Tracker")
    hours = s.slider("Hours Slept", 0, 12, 7)
    quality = s.selectbox("Sleep Quality", ["Poor", "Fair", "Good", "Excellent"])
    dream = s.checkbox("Did you dream?")
    if s.button("✉️ Log Sleep"):
        log = {"Date": str(d.today()), "Hours": hours, "Quality": quality, "Dream": dream}
        if "sleep_logs" not in s.session_state:
            s.session_state.sleep_logs = []
        s.session_state.sleep_logs.append(log)
        s.success("Sleep log saved.")

    if "sleep_logs" in s.session_state and s.session_state.sleep_logs:
        s.markdown("### 📘 Sleep Log History")
        df = p.DataFrame(s.session_state.sleep_logs)
        s.dataframe(df, use_container_width=True)

def injury():
    s.button("⬅️ Back to Home", on_click=lambda: s.session_state.update({"pg": "home"}))
    s.subheader("🦵 Injury Tracker")
    body_part = s.text_input("Injured Body Part")
    severity = s.select_slider("Severity", options=["Mild", "Moderate", "Severe"])
    notes = s.text_area("Description")
    if s.button("✉️ Add Injury"):
        log = {"Date": str(d.today()), "Part": body_part, "Severity": severity, "Notes": notes}
        if "injury_logs" not in s.session_state:
            s.session_state.injury_logs = []
        s.session_state.injury_logs.append(log)
        s.success("Injury log added.")

    if "injury_logs" in s.session_state and s.session_state.injury_logs:
        s.markdown("### 📘 Injury Log Records")
        df = p.DataFrame(s.session_state.injury_logs)
        s.dataframe(df, use_container_width=True)

def hy():
    s.button("⬅️ Back to Home", on_click=lambda: s.session_state.update({"pg": "home"}))
    s.subheader("💧 Hydration Planner")
    weight = s.number_input("Your weight (kg):", min_value=30.0, max_value=200.0, value=60.0)
    duration = s.number_input("Run duration (minutes):", min_value=10, max_value=300, value=60)
    intensity = s.selectbox("Intensity Level:", ["Low", "Moderate", "High"])

    multiplier = {"Low": 0.03, "Moderate": 0.045, "High": 0.06}[intensity]
    required = round(weight * multiplier * duration / 60, 2)

    s.success(f"💧 Estimated water needed: {required} liters")

def score():
    s.button("⬅️ Back to Home", on_click=lambda: s.session_state.update({"pg": "home"}))
    s.subheader("☁️ Run Readiness Score")
    temp = s.slider("Temperature (°C)", -10, 45, 20)
    humid = s.slider("Humidity (%)", 0, 100, 50)
    wind = s.slider("Wind Speed (km/h)", 0, 50, 5)
    rain = s.slider("Rain Intensity (mm/h)", 0, 20, 0)

    score = max(0, 25 - abs(temp - 20)) + max(0, 25 - abs(humid - 50) // 2) + max(0, 25 - wind) + max(0, 25 - rain * 2)
    score = int(score)

    s.metric("Run Readiness Score", f"{score} / 100")
    if humid > 80:
        s.info("💧 High humidity — hydrate well!")
    if rain > 5:
        s.warning("☔ Heavy rain — consider staying dry!")

def countdown():
    s.button("⬅️ Back to Home", on_click=lambda: s.session_state.update({"pg": "home"}))
    s.subheader("📅 Race Countdown")
    race_date = s.date_input("Select your race day:", value=dt.today() + td(days=30))
    now = d.now()
    future = d.combine(race_date, d.min.time())
    diff = future - now

    days, secs = diff.days, diff.seconds
    hours = secs // 3600
    minutes = (secs % 3600) // 60
    seconds = secs % 60

    s.markdown(f"""
    <h1 style='text-align:center;font-size:3rem;'>⏳ {days}d {hours}h {minutes}m {seconds}s</h1>
    """, unsafe_allow_html=True)

def shoes():
    s.button("⬅️ Back to Home", on_click=lambda: s.session_state.update({"pg": "home"}))
    s.subheader("👟 Shoe Mileage Tracker")
    sh = s.text_input("Shoe Model")
    d1 = s.date_input("Start Date")
    km = s.number_input("Kilometers Run", min_value=0.0, step=0.1)
    limit = s.number_input("Estimated Max Mileage (km)", min_value=100.0, value=800.0)
    if s.button("➕ Log Shoe Mileage"):
        left = max(0.0, limit - km)
        new_entry = {"Date": str(d.today()), "Model": sh, "Start Date": str(d1), "Distance": km, "Limit": limit, "Left": left}
        if "shoe_logs" not in s.session_state:
            s.session_state.shoe_logs = []
        s.session_state.shoe_logs.append(new_entry)
        s.success(f"{sh} has {left:.1f} km left out of {limit:.0f} km.")

def shoelog():
    s.button("⬅️ Back to Home", on_click=lambda: s.session_state.update({"pg": "home"}))
    s.subheader("📖 All Logs")

    tabs = s.tabs(["👟 Shoes", "🧠 Mental", "🛌 Sleep", "🦵 Injury"])

    with tabs[0]:
        if "shoe_logs" in s.session_state and s.session_state.shoe_logs:
            df = p.DataFrame(s.session_state.shoe_logs)
            s.dataframe(df, use_container_width=True)
            import io
            buffer = io.BytesIO()
            with p.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            buffer.seek(0)
            s.download_button("📥 Download as Excel", buffer, file_name="shoe_logs.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            s.info("No shoe logs available yet.")

    with tabs[1]:
        if "mental_logs" in s.session_state and s.session_state.mental_logs:
            df = p.DataFrame(s.session_state.mental_logs)
            s.dataframe(df, use_container_width=True)
            import io
            buffer = io.BytesIO()
            with p.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            buffer.seek(0)
            s.download_button("📥 Download as Excel", buffer, file_name="mental_logs.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            s.info("No mental logs available yet.")

    with tabs[2]:
        if "sleep_logs" in s.session_state and s.session_state.sleep_logs:
            df = p.DataFrame(s.session_state.sleep_logs)
            s.dataframe(df, use_container_width=True)
            import io
            buffer = io.BytesIO()
            with p.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            buffer.seek(0)
            s.download_button("📥 Download as Excel", buffer, file_name="sleep_logs.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            s.info("No sleep logs available yet.")

    with tabs[3]:
        if "injury_logs" in s.session_state and s.session_state.injury_logs:
            df = p.DataFrame(s.session_state.injury_logs)
            s.dataframe(df, use_container_width=True)
            import io
            buffer = io.BytesIO()
            with p.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            buffer.seek(0)
            s.download_button("📥 Download as Excel", buffer, file_name="injury_logs.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            s.info("No injury logs available yet.")

pgs = {
    "home": h,
    "pace": pace,
    "hydration": hy,
    "score": score,
    "shoes": shoes,
    "shoelog": shoelog,
    "mental": mental,
    "sleep": sleep,
    "countdown": countdown,
    "injury": injury,
}

pgs[s.session_state.pg]()
