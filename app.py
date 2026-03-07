import streamlit as st
import auth
from ui import patient_dashboard, admin_dashboard

st.set_page_config(page_title="Personalized Health Coach", page_icon="🥗", layout="wide")

if "user" not in st.session_state:
    st.session_state["user"] = None

def main():
    if st.session_state["user"] is None:
        login_signup_view()
    else:
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
    st.title("AI-Powered Personalized Health Coach")
    st.markdown("Your highly personalized nutrition, activity, and lifestyle platform.")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user = auth.authenticate_user(email, password)
            if user:
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Invalid email or password.")
                
    with tab2:
        st.subheader("Create an Account")
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["patient", "admin", "expert"])
        
        if st.button("Sign Up"):
            if new_email and len(new_password) > 3:
                success, msg_or_uuid = auth.create_user(new_email, new_password, role, new_name)
                if success:
                    st.success("Account created successfully! Please login.")
                else:
                    st.error(f"Failed to create account: {msg_or_uuid}")
            else:
                st.error("Please fill in valid details.")

if __name__ == "__main__":
    main()
