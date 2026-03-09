import streamlit as st

def render_header():
    st.set_page_config(page_title="AROMI Health", layout="wide", page_icon="🌿")
    st.markdown("""
        <style>
        /* Soft, colorful, non-dominating background */
        .stApp {
            background: linear-gradient(135deg, #f6fffa 0%, #e3f2fd 100%);
        }
        .main-header {
            font-size: 2.5rem;
            color: #fff;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: linear-gradient(90deg, #2e7b5b 0%, #43a047 100%);
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(46, 123, 91, 0.2);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        .stButton button {
            background: linear-gradient(to right, #2e7b5b 0%, #43a047 100%);
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(46, 123, 91, 0.4);
            color: white;
            border: none;
        }
        /* Form styling to make it pop subtly */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            border: 1px solid rgba(255,255,255,0.8);
            backdrop-filter: blur(10px);
        }
        /* Radio button wrapper */
        div[role="radiogroup"] {
            background: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, unit=""):
    st.markdown(f"""
        <div style="background-color: #f0f7f4; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #2e7b5b; margin-bottom: 1rem;">
            <h4 style="color: #4a4a4a; margin: 0;">{title}</h4>
            <h2 style="color: #2e7b5b; margin: 0;">{value} {unit}</h2>
        </div>
    """, unsafe_allow_html=True)
