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

# Updated navigation handler to use on_click callbacks

def go_to(page):
    def switch():
        s.session_state.pg = page
    return switch

def h():
    s.title("🏁 Welcome to Run Tools")
    s.write("Choose a tool below:")
    c1, c2 = s.columns(2)
    with c1:
        s.button("📏 Running Pace Calculator", on_click=go_to("pace"))
        s.button("💧 Hydration Planner", on_click=go_to("hydration"))
        s.button("☁️ Run Readiness Score", on_click=go_to("score"))
        s.button("📅 Race Countdown", on_click=go_to("countdown"))
    with c2:
        s.button("👟 Shoe Mileage Tracker", on_click=go_to("shoes"))
        s.button("🧠 Mental Readiness Log", on_click=go_to("mental"))
        s.button("🛌 Sleep Quality Tracker", on_click=go_to("sleep"))
        s.button("🦵 Injury Tracker", on_click=go_to("injury"))

def p():
    s.button("⬅️ Back to Home", on_click=go_to("home"))
    s.subheader("📏 Running Pace Calculator")
    gd = s.number_input("Target Distance (km)", min_value=1.0, step=0.1)
    ll = s.number_input("Lap Length (km)", min_value=0.1, step=0.01)
    gt = s.time_input("Goal Time")
    if gd and ll and gt:
        ts = gt.hour * 3600 + gt.minute * 60 + gt.second
        ppk = ts / gd
        nfl = int(gd // ll)
        lo = gd - (nfl * ll)

        s.write("### Breakdown:")
        for l in range(1, nfl + 1):
            s.write(f"Lap {l}: {ll:.2f} km @ {ppk:.2f} sec/km = {ppk * ll:.1f} sec")
        if lo > 0:
            s.write(f"Lap {nfl + 1}: {lo:.2f} km @ {ppk:.2f} sec/km = {ppk * lo:.1f} sec")

def hy():
    s.button("⬅️ Back to Home", on_click=go_to("home"))
    s.subheader("💧 Hydration Planner")
    dur = s.slider("Run Duration (minutes)", 10, 180, 60)
    temp = s.slider("Temperature (°C)", 10, 40, 25)
    inten = s.selectbox("Intensity", ["Low", "Medium", "High"])
    mul = {"Low": 0.4, "Medium": 0.6, "High": 0.8}[inten]
    wn = dur * mul * (1 + (temp - 20) * 0.03)
    s.metric("Recommended Water Intake", f"{wn:.0f} ml")

def mlog():
    s.button("⬅️ Back to Home", on_click=go_to("home"))
    s.subheader("🧠 Mental Readiness Log")
    m = s.slider("How motivated are you today?", 1, 10, 5)
    st = s.slider("Stress level", 1, 10, 5)
    note = s.text_area("Mental Notes")
    if s.button("📝 Save Mental Log"):
        s.success("Mental state logged!")

def sl():
    s.button("⬅️ Back to Home", on_click=go_to("home"))
    s.subheader("🛌 Sleep Quality Tracker")
    h = s.slider("Hours Slept", 0, 12, 7)
    q = s.selectbox("Sleep Quality", ["Poor", "Fair", "Good", "Excellent"])
    if s.button("🛏️ Log Sleep"):
        s.success(f"Sleep logged: {h}h - {q}")

def rc():
    s.button("⬅️ Back to Home", on_click=go_to("home"))
    s.subheader("📅 Race Countdown")
    rd = s.date_input("Select your race date:", value=dt.today())
    rt = s.time_input("Select race time:", value=d.now().time())
    rdt = d.combine(rd, rt)
    pl = s.empty()
    while True:
        nw = d.now()
        dl = rdt - nw
        if dl.total_seconds() < 0:
            pl.warning("⚠️ Race date is in the past.")
            break
        dy = dl.days
        h, r = divmod(dl.seconds, 3600)
        m, sc = divmod(r, 60)
        pl.markdown(f"""
        <h1 style='text-align:center; font-size:3rem;'>🏁 {dy} Days {h:02d}:{m:02d}:{sc:02d}</h1>
        """, unsafe_allow_html=True)
        t.sleep(1)

def inj():
    s.button("⬅️ Back to Home", on_click=go_to("home"))
    s.subheader("🦵 Injury Tracker")
    it = s.selectbox("Injury Type", ["None", "Knee", "Shin", "Ankle", "Hip", "Other"])
    sev = s.slider("Severity (1=minor, 10=severe)", 1, 10, 3)
    nts = s.text_area("Additional Notes")
    if s.button("📝 Save Injury Log"):
        s.success("Injury info saved!")

pgs = {
    "home": h,
    "pace": p,
    "hydration": hy,
    "score": lambda: s.write("☁️ Placeholder for Readiness Score"),
    "shoes": lambda: s.write("👟 Placeholder for Shoe Tracker"),
    "mental": mlog,
    "sleep": sl,
    "countdown": rc,
    "injury": inj,
}

pgs[s.session_state.pg]()
