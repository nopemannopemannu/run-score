import streamlit as st
st.set_page_config(page_title="Run Score", layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "input"
if "weather" not in st.session_state:
    st.session_state.weather = {}
def to_result():
    st.session_state.page = "result"
def to_input():
    st.session_state.page = "input"
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
if st.session_state.page == "input":
    st.markdown("## 🏃 Input Weather Conditions")
    temperature = st.number_input("🌡️ Temperature (°C)", value=25.0, step=0.5)
    humidity = st.number_input("💧 Humidity (%)", value=60.0, step=1.0)
    wind_speed = st.number_input("🌬️ Wind Speed (m/s)", value=2.0, step=0.1)
    rain = st.number_input("🌧️ Rain Intensity (mm/h)", value=0.0, step=0.1)
    uv_index = st.slider("🔆 UV Index", 0, 11, 3)
    if st.button("📊 Show Result"):
        st.session_state.weather = {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "rain": rain,
            "uv_index": uv_index
        }
        to_result()
elif st.session_state.page == "result":
    weather = st.session_state.weather
    st.markdown("## 📝 Run Weather Evaluation")
    score, logs = calc_score(weather)
    st.metric("🏅 Run Score", f"{score}/100")
    st.progress(score)
    st.markdown("### Breakdown:")
    for log in logs:
        st.write(log)
    st.markdown("---")
    if st.button("🔁 Re-enter Weather Data"):
        to_input()
