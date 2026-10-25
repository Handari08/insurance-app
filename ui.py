import os

import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Health Insurance Predictor",
    page_icon="🏥",
    layout="centered"
)

st.markdown("""
<style>

.main{
    background:#F5F7FB;
}

.block-container{
    padding-top:2rem;
}

.title{
    text-align:center;
    font-size:40px;
    font-weight:700;
    color:#2563EB;
}

.subtitle{
    text-align:center;
    color:#6b7280;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    "<div class='title'>🏥 Health Insurance Predictor</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Estimate your future medical insurance costs</div>",
    unsafe_allow_html=True
)

st.divider()

age = st.slider(
    "Age",
    18,
    100,
    25
)

sex = st.selectbox(
    "Gender",
    ["male", "female"]
)

bmi = st.number_input(
    "BMI",
    min_value=10.0,
    max_value=60.0,
    value=25.0
)

children = st.number_input(
    "Number of Children",
    min_value=0,
    max_value=10,
    value=0
)

smoker = st.selectbox(
    "Smoker Status",
    ["yes", "no"]
)

region = st.selectbox(
    "Region",
    [
        "southwest",
        "southeast",
        "northwest",
        "northeast"
    ]
)

if st.button(
    "Predict Insurance Cost",
    use_container_width=True
):

    payload = {
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": smoker,
        "region": region
    }

    response = requests.post(
        f"{API_URL}/predict",
        json=payload
    )

    result = response.json()

    st.success(
        f"Estimated Cost: ${result['estimated_charge']:,.2f}"
    )