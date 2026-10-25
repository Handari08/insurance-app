
import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Prediksi Biaya Asuransi Kesehatan",
    page_icon="🏥",
    layout="centered"
)

# Custom dark theme dan perbaikan kontras teks
st.markdown("""
<style>
/* Background utama */
.stApp {
    background-color: #111827;
    color: #F9FAFB;
}

/* Area konten */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 850px;
}

/* Judul */
.title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #60A5FA;
    margin-bottom: 8px;
}

/* Subjudul */
.subtitle {
    text-align: center;
    font-size: 16px;
    color: #D1D5DB;
    margin-bottom: 25px;
}

/* Semua label input */
.stApp label,
.stApp label p,
.stApp .stMarkdown p {
    color: #F9FAFB !important;
}

/* Input, selectbox, dan number input */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #1F2937;
    color: #FFFFFF;
    border: 1px solid #4B5563;
    border-radius: 8px;
}

.stNumberInput input {
    background-color: #1F2937 !important;
    color: #FFFFFF !important;
    border: 1px solid #4B5563 !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] {
    color: #60A5FA;
}

.stSlider [data-testid="stTickBar"] {
    background-color: #9CA3AF;
}

/* Tombol prediksi */
.stButton > button {
    background-color: #2563EB;
    color: #FFFFFF !important;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    border: 1px solid #93C5FD;
    color: #FFFFFF !important;
}

/* Hasil prediksi */
div[data-testid="stAlert"] {
    background-color: #064E3B;
    border: 1px solid #10B981;
    border-radius: 10px;
    color: #FFFFFF !important;
}

div[data-testid="stAlert"] p {
    color: #FFFFFF !important;
    font-size: 17px;
    font-weight: 600;
}

/* Garis pemisah */
hr {
    border-color: #374151;
}

/* Warna ikon dan teks tambahan */
.stApp small,
.stApp [data-testid="stCaptionContainer"] {
    color: #D1D5DB !important;
}

/* Fokus input */
.stSelectbox div[data-baseweb="select"]:focus-within,
.stNumberInput input:focus {
    border-color: #60A5FA !important;
    box-shadow: 0 0 0 2px #2563EB33;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    "<div class='title'>🏥 Prediksi Biaya Asuransi Kesehatan </div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Estimate your future medical insurance costs</div>",
    unsafe_allow_html=True
)

st.divider()

# Input data pengguna
age = st.slider(
    "Age",
    min_value=18,
    max_value=100,
    value=25
)

sex = st.selectbox(
    "Gender",
    ["male", "female"]
)

bmi = st.number_input(
    "BMI",
    min_value=10.0,
    max_value=60.0,
    value=25.0,
    step=0.1,
    format="%.1f"
)

children = st.number_input(
    "Number of Children",
    min_value=0,
    max_value=10,
    value=0,
    step=1
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

st.markdown("<br>", unsafe_allow_html=True)

# Tombol dan prediksi
if st.button("Predict Insurance Cost", use_container_width=True):
    payload = {
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": smoker,
        "region": region
    }

    try:
        with st.spinner("Calculating insurance cost..."):
            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=30
            )

        response.raise_for_status()
        result = response.json()

        estimated_charge = float(result["estimated_charge"])

        st.success(
            f"Estimated Cost: ${estimated_charge:,.2f}"
        )

    except requests.exceptions.RequestException as e:
        st.error(
            "Unable to connect to the prediction API. "
            "Please ensure the backend is running."
        )
        st.caption(f"Technical details: {e}")

    except (KeyError, ValueError, TypeError):
        st.error(
            "The API returned an invalid prediction result."
        )
