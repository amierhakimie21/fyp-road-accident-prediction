# =====================================================
# ROAD ACCIDENT SEVERITY PREDICTION SYSTEM
# FINAL • STREAMLIT CLOUD READY • FYP SAFE
# =====================================================

import streamlit as st
import pandas as pd
import altair as alt
import os
import joblib

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="Road Accident Severity Prediction",
    layout="centered"
)

# -----------------------------------------------------
# THEME STYLE (MATCH WEBSITE CSS)
# -----------------------------------------------------
st.markdown(
    """
    <style>
    :root{
      --bg:#fafafa;
      --panel:#ffffff;
      --text:#111827;
      --muted:#6b7280;
      --accent:#e07a25;
      --accent-soft:#fde8d6;
      --radius:24px;
    }

    html, body{
      background:var(--bg);
      color:var(--text);
      font-family:Inter, system-ui, Arial;
    }

    .back-btn{
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:10px 18px;
      border-radius:999px;
      font-weight:600;
      font-size:14px;
      color:var(--text);
      text-decoration:none;
      background:var(--panel);
      border:1px solid #e5e7eb;
      transition:.25s ease;
    }

    .back-btn:hover{
      background:var(--accent-soft);
      color:var(--accent);
      transform:translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------
# BACK BUTTON (TOP, THEME STYLE)
# -----------------------------------------------------
st.markdown(
    """
    <div style="margin-bottom:28px;">
      <a href="https://accidentanalysis-da.vercel.app/predict.html"
         class="back-btn">
         ← Back to Prediction Page
      </a>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------
# TITLE
# -----------------------------------------------------
st.title("🚗 Road Accident Severity Prediction System")
st.write(
    "This system predicts **road accident severity** "
    "(Slight, Serious, Fatal) based on driving and "
    "environmental conditions."
)

st.divider()

# -----------------------------------------------------
# LOAD MODEL
# -----------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "accident_severity_model.pkl")

if not os.path.exists(MODEL_PATH):
    st.error("❌ Model file not found. Please check deployment files.")
    st.stop()

model = joblib.load(MODEL_PATH)

# -----------------------------------------------------
# USER INPUT
# -----------------------------------------------------
st.subheader("📝 Driving Conditions")

day_of_week = st.selectbox(
    "Day of Week",
    [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]
)

hour = st.slider("Time of Day (Hour)", 0, 23, 12)

weather_conditions = st.selectbox(
    "Weather Condition",
    ["Fine", "Rain", "Fog", "Snow"]
)

speed_limit = st.selectbox(
    "Speed Limit (km/h)",
    [30, 40, 50, 60, 70, 80, 90, 100, 110]
)

urban_or_rural_area = st.selectbox(
    "Road Environment",
    ["Urban", "Rural"]
)

st.divider()

# -----------------------------------------------------
# PREDICTION
# -----------------------------------------------------
if st.button("🔍 Predict Accident Severity"):

    light_conditions = "Darkness" if hour >= 18 or hour <= 5 else "Daylight"

    input_df = pd.DataFrame([{
        "year": 2024,
        "month": 6,
        "day_of_week": day_of_week,
        "hour": hour,
        "weather_conditions": weather_conditions,
        "light_conditions": light_conditions,
        "road_type": "Single carriageway",
        "speed_limit": speed_limit,
        "urban_or_rural_area": urban_or_rural_area,
        "road_surface_conditions": "Dry"
    }])

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    confidence = probabilities.max() * 100

    # -------------------------------------------------
    # RESULT
    # -------------------------------------------------
    st.subheader("📊 Prediction Result")

    if prediction == "Slight":
        st.success("🟢 SLIGHT Accident Severity")
    elif prediction == "Serious":
        st.warning("🟠 SERIOUS Accident Severity")
    else:
        st.error("🔴 FATAL Accident Severity")

    st.metric("Prediction Confidence", f"{confidence:.1f}%")

    # -------------------------------------------------
    # PROBABILITY CHART (THEME COLORS)
    # -------------------------------------------------
    prob_df = pd.DataFrame({
        "Severity Level": model.classes_,
        "Probability (%)": probabilities * 100
    })

    severity_colors = {
        "Slight": "#22c55e",
        "Serious": "#f59e0b",
        "Fatal": "#dc2626"
    }

    chart = alt.Chart(prob_df).mark_bar(
        stroke="black",
        strokeWidth=1
    ).encode(
        x=alt.X("Severity Level:N", title="Severity Level"),
        y=alt.Y("Probability (%):Q", title="Probability (%)"),
        color=alt.Color(
            "Severity Level:N",
            scale=alt.Scale(
                domain=list(severity_colors.keys()),
                range=list(severity_colors.values())
            ),
            legend=alt.Legend(title="Severity Level")
        ),
        tooltip=[
            alt.Tooltip("Severity Level:N"),
            alt.Tooltip("Probability (%):Q", format=".1f")
        ]
    ).properties(height=260)

    st.altair_chart(chart, use_container_width=True)

    # -------------------------------------------------
    # EXPLANATION
    # -------------------------------------------------
    st.subheader("❓ Why this result?")

    reasons = []

    if speed_limit >= 80:
        reasons.append("High driving speed")
    if hour >= 18 or hour <= 5:
        reasons.append("Night-time driving")
    if weather_conditions in ["Rain", "Fog", "Snow"]:
        reasons.append("Adverse weather conditions")
    if urban_or_rural_area == "Rural":
        reasons.append("Rural road environment")

    if reasons:
        for r in reasons:
            st.write(f"• {r}")
    else:
        st.write("• No major risk factors detected")

    # -------------------------------------------------
    # SAFETY RECOMMENDATIONS
    # -------------------------------------------------
    st.subheader("✅ Safety Recommendations")

    if prediction == "Slight":
        st.write("• Maintain safe driving behaviour")
        st.write("• Continue to follow traffic regulations")
    elif prediction == "Serious":
        st.write("• Reduce speed")
        st.write("• Increase attention while driving")
        st.write("• Maintain a safe distance from other vehicles")
    else:
        st.write("• Avoid unnecessary travel if possible")
        st.write("• Drive at reduced speed with extreme caution")
        st.write("• Follow all traffic safety guidelines")

    # -------------------------------------------------
    # DISCLAIMER
    # -------------------------------------------------
    st.caption(
        "⚠️ This system is intended for academic and decision-support purposes only "
        "and does not guarantee accident prevention."
    )
