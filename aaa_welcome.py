import streamlit as st
import os

# --- Page Configuration ---
st.set_page_config(page_title="Plagiarism Checker", layout="centered")

# --- Professional Blue and White Styling ---
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #ffffff !important;
        color: #001f3f !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #001f3f !important;
        text-align: center !important;
    }
    .stButton > button {
        background-color: #ffffff !important;
        color: white !important;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2.5rem;
        border-radius: 40px;
        font-size: 1.1rem;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease-in-out;
        display: block;
        margin: 2.5rem auto;
    }
    .stButton > button:hover {
        background-color: #003366 !important;
        transform: translateY(-2px) scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

# --- Logo (Optional) ---
logo_path = "Users/Ansh/Desktop/DAA/pages/assets/logo.png"
if os.path.exists(logo_path):
    st.image("logo_path", width=100)

# --- Welcome Section ---
st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem;">
        <h1 style="font-size: 3rem;">📘 Plagiarism Checker</h1>
        <h3 style="font-weight: normal;">Your simple solution to detect text and code similarity</h3>
        <p style="font-size: 1.1rem; max-width: 600px; margin: 1rem auto;">
            Upload and compare files with ease. Identify overlapping content between documents and code with high precision.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- Call to Action ---
if st.button("Get Started ➤"):
    script_path = os.path.join(os.path.dirname(__file__), "pages/app.py")
    st.switch_page(script_path)
