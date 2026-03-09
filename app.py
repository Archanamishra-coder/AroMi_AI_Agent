import streamlit as st
import ui
import auth

# Initialize session state variables
if 'user' not in st.session_state:
    st.session_state['user'] = None

ui.render_header()
st.markdown("<div class='main-header'>AI Health Coach Platform</div>", unsafe_allow_html=True)

if st.session_state['user'] is not None:
    menu_choice = st.selectbox("Menu", ["Home", "Profile"])

    if menu_choice == "Home":
        st.success(f"Welcome back, {st.session_state['user']['name']}!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state['user']['role'] == 'patient':
                st.info("👈 Navigate to the User Dashboard from the sidebar")
            else:
                st.info("👈 Navigate to the Admin Dashboard from the sidebar")
        with col2:
            if st.button("Log Out"):
                st.session_state['user'] = None
                st.rerun()

    elif menu_choice == "Profile":
        st.subheader("Your Profile")
        
        # Profile Picture logic
        st.write("Upload a profile picture or take a real-time photo")
        
        photo_choice = st.radio("Choose Photo Source", ["Upload from Device", "Take a Photo"], horizontal=True)
        
        photo_data = None
        if photo_choice == "Upload from Device":
            photo_data = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        else:
            photo_data = st.camera_input("Take a Photo")
            
        if photo_data is not None:
            st.image(photo_data, caption="Profile Photo", width=200)
            
        # Display other profile details
        user_info = auth.get_user_profile(st.session_state['user']['uuid'])
        if user_info:
            st.write(f"**Name:** {user_info['name']}")
            st.write(f"**Email:** {user_info['email']}")
            st.write(f"**Role:** {user_info['role'].capitalize()}")
            if user_info.get('job_profession'):
                st.write(f"**Job:** {user_info['job_profession']}")
            if user_info.get('locality'):
                st.write(f"**Locality:** {user_info['locality']}")
            if user_info.get('health_condition'):
                st.write(f"**Health Conditions:** {user_info['health_condition']}")
                
        if st.button("Log Out"):
            st.session_state['user'] = None
            st.rerun()

else:
    # Hide sidebar when not logged in
    st.markdown("""
        <style>
            [data-testid="stSidebar"], [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

    auth_action = st.radio("Choose Action", ["Login", "Sign Up"], horizontal=True)

    if auth_action == "Login":
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                user = auth.login_user(email, password)
                if user:
                    st.session_state['user'] = user
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
                    
    elif auth_action == "Sign Up":
        st.subheader("Create a New Account")
        with st.form("signup_form"):
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            role_choice = st.selectbox("Role", ["User", "Admin"])
            # Map choice to db format
            role = "patient" if role_choice == "User" else "admin"
            
            st.write("Optional Details (for Users):")
            job = st.text_input("Job/Profession (e.g., Software Engineer)")
            locality = st.text_input("Locality (e.g., Urban, Suburban)")
            health_cond = st.text_input("Health Conditions (e.g., Pre-diabetic)")
            
            submitted = st.form_submit_button("Sign Up")
            
            if submitted:
                if new_name and new_email and new_password:
                    success, msg = auth.register_user(new_name, new_email, new_password, role, job, locality, health_cond)
                    if success:
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error(f"Error creating account: {msg}")
                else:
                    st.warning("Please fill in all required fields.")
