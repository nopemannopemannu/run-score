import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Run Score", layout="wide")

# Custom style for padding and spacing
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
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "input"

def save_log(weather, score):
    log = pd.DataFrame([{
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        **weather,
        "score": score
    }])
    log.to_csv("run_scores_log.csv", mode='a', header=False, index=False)

def calc_score(w):
    score = 100
    logs = []

    if 10 <= w["temperature"] <= 20:
        logs.append("✅ Ideal temperature.")
    else:
        diff = abs(w["temperature"] - 15)
        penalty = min(30, diff * 2)
        score -= penalty
        logs.append(f"⚠️ Temp penalty: -{penalty} (Temp: {w['temperature']}°C)")

    if 30 <= w["humidity"] <= 60:
        logs.append("✅ Humidity optimal.")
    else:
        penalty = min(20, abs(w["humidity"] - 45) * 0.5)
        score -= penalty
        logs.append(f"⚠️ Humidity penalty: -{penalty:.1f} (Humidity: {w['humidity']}%)")

    if w["wind_speed"] <= 5:
        logs.append("✅ Wind is fine.")
    else:
        penalty = min(20, (w["wind_speed"] - 5) * 2)
        score -= penalty
        logs.append(f"⚠️ Wind penalty: -{penalty} (Wind: {w['wind_speed']} m/s)")

    if w["rain"] == 0:
        logs.append("✅ No rain.")
    else:
        penalty = min(20, w["rain"] * 10)
        score -= penalty
        logs.append(f"⚠️ Rain penalty: -{penalty} (Rain: {w['rain']} mm/h)")

    if w["uv_index"] <= 5:
        logs.append("✅ UV safe.")
    else:
        penalty = (w["uv_index"] - 5) * 2
        score -= penalty
        logs.append(f"⚠️ UV penalty: -{penalty} (UV: {w['uv_index']})")

    return max(0, int(score)), logs

def verdict_text(score):
    if score >= 80:
        return "🟢 Great weather to run!", "success"
    elif score >= 60:
        return "🟡 Moderate — stay cautious.", "warning"
    else:
        return "🔴 Not recommended for running.", "error"

if st.session_state.page == "input":
    st.title("🏃 Run Readiness Evaluator")
    st.subheader("Input Current Weather Conditions")

    with st.form(key="weather_form"):
        col1, col2 = st.columns(2)
        with col1:
            temperature = st.number_input("🌡️ Temperature (°C)", value=25.0, step=0.5)
            humidity = st.number_input("💧 Humidity (%)", value=60.0, step=1.0)
            rain = st.number_input("🌧️ Rain Intensity (mm/h)", value=0.0, step=0.1)
        with col2:
            wind_speed = st.number_input("🌬️ Wind Speed (m/s)", value=2.0, step=0.1)
            uv_index = st.slider("🔆 UV Index", 0, 11, 3)

        submitted = st.form_submit_button("📊 Show Result")
        if submitted:
            st.session_state.weather = {
                "temperature": temperature,
                "humidity": humidity,
                "wind_speed": wind_speed,
                "rain": rain,
                "uv_index": uv_index
            }
            st.session_state.score, st.session_state.logs = calc_score(st.session_state.weather)
            st.session_state.verdict, st.session_state.status = verdict_text(st.session_state.score)
            save_log(st.session_state.weather, st.session_state.score)
            st.session_state.page = "result"
            st.rerun()

elif st.session_state.page == "result":
    w = st.session_state.weather
    score = st.session_state.score
    logs = st.session_state.logs
    verdict = st.session_state.verdict
    status = st.session_state.status

    st.title("📝 Run Weather Evaluation")
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={'font': {'size': 26}},
            title={'text': "Run Score", 'font': {'size': 14}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "green" if score >= 80 else "orange" if score >= 60 else "red"}
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"<div class='metric-container'>", unsafe_allow_html=True)
        getattr(st, status)(verdict)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("**Breakdown**")
        for log in logs:
            st.markdown(f"- {log}")

        st.markdown("**🧠 Smart Tips**")
        tips = []

        if w["temperature"] > 30:
            tips.append("🥵 It's hot — hydrate well and consider running early.")
        elif w["temperature"] < 10:
            tips.append("🧥 It's cold — wear warm gear to stay comfortable.")

        if w["humidity"] > 70:
            tips.append("💧 High humidity — wear breathable clothing.")
        elif w["humidity"] < 30:
            tips.append("🌵 Low humidity — consider hydrating more.")

        if w["uv_index"] > 7:
            tips.append("🧴 High UV — wear sunscreen or run in shaded areas.")
        elif w["uv_index"] <= 2:
            tips.append("🌤️ Low UV — great time for outdoor activity!")

        if tips:
            for tip in tips:
                st.write(tip)
        else:
            st.write("✅ No special tips — enjoy your run!")

        if st.button("🔁 Re-enter Weather Data"):
            st.session_state.page = "input"
            st.rerun()
