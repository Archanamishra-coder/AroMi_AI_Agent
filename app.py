import streamlit as st
import auth
from ui import patient_dashboard, admin_dashboard

st.set_page_config(page_title="Personalized Health Coach", page_icon="🥗", layout="wide")

if "user" not in st.session_state:
    st.session_state["user"] = None

def make_header(text, bg_color):
    st.markdown(f'<div style="background-color: {bg_color}; padding: 10px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);"><h2>{text}</h2></div>', unsafe_allow_html=True)

def set_bg(is_login):
    if is_login:
        bg_url = "https://images.unsplash.com/photo-1490818387583-1baba5e638af?q=80&w=2000&auto=format&fit=crop"
    else:
        bg_url = "https://images.unsplash.com/photo-1505506874110-6a7a4c989773?q=80&w=2000&auto=format&fit=crop"
        
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stApp > header {{
            background-color: transparent;
        }}
        div[data-testid="stAppViewBlockContainer"] {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            color: #333;
        }}
        /* Make all text easily visible */
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText {{
            color: #2c3e50 !important;
        }}
        .stButton>button {{
            border-radius: 20px;
            font-weight: bold;
            border: 2px solid #FF4B4B;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    if st.session_state["user"] is None:
        set_bg(is_login=True)
        login_signup_view()
    else:
        set_bg(is_login=False)
        # Top bar
        cols = st.columns([8, 1])
        with cols[1]:
            if st.button("Logout"):
                st.session_state["user"] = None
                st.rerun()
                
        if st.session_state["user"]['role'] == "patient":
            patient_dashboard()
        elif st.session_state["user"]['role'] in ["admin", "expert"]:
            admin_dashboard()
        else:
            st.error("Unknown user role.")

def login_signup_view():
    st.markdown('<div style="background: linear-gradient(90deg, #FF4B4B, #FF904F); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 25px; box-shadow: 2px 2px 10px rgba(0,0,0,0.2);"><h1>AI-Powered Personalized Health Coach</h1><p style="font-size: 1.2rem; margin: 0;">Your highly personalized nutrition, activity, and lifestyle platform.</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="background-color: rgba(255,255,255,0.85); padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
    
    action = st.radio("Welcome! Choose to Login, Sign Up or Continue as Guest:", ["Login", "Sign Up", "Continue as Guest"], horizontal=True)
    
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    if action == "Login":
        make_header("Login", "#4A90E2")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user = auth.authenticate_user(email, password)
            if user:
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Invalid email or password.")
                
    elif action == "Sign Up":
        make_header("Create an Account", "#50E3C2")
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["patient", "admin", "expert"])
        
        if st.button("Sign Up"):
            if new_email and len(new_password) > 3:
                success, msg_or_uuid = auth.create_user(new_email, new_password, role, new_name)
                if success:
                    st.success("Account created successfully! Please switch to Login.")
                else:
                    st.error(f"Failed to create account: {msg_or_uuid}")
            else:
                st.error("Please fill in valid details.")

    elif action == "Continue as Guest":
        make_header("Guest Access", "#B8B8B8")
        st.info("Experience the app without an account. Some features may not stick.")
        if st.button("Enter as Guest"):
            st.session_state["user"] = {"uuid": "guest-uuid-123", "role": "patient", "name": "Guest User"}
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
