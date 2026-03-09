import streamlit as st
import ui
import auth
from db import get_connection

if 'user' not in st.session_state or st.session_state['user'] is None:
    st.warning("Please log in from the main page.")
    st.stop()

if st.session_state['user']['role'] not in ['admin', 'expert']:
    st.error("Access denied. Admin or Expert privileges required.")
    st.stop()

st.title(f"Expert / Admin Dashboard")

tab1, tab2 = st.tabs(["Search Patients", "My Expert Profile"])

with tab1:
    st.subheader("Patient Lookup")
    search_query = st.text_input("Search by UUID, Name, or Email")
    if st.button("Search"):
        with st.spinner("Searching database..."):
            # Mock search logic
            conn = get_connection()
            c = conn.cursor()
            query = f"%{search_query}%"
            c.execute("SELECT uuid, name, email, job_profession, health_condition FROM Users WHERE role='patient' AND (name LIKE ? OR email LIKE ? OR uuid LIKE ?)", (query, query, query))
            results = c.fetchall()
            conn.close()
            
            if results:
                st.success(f"Found {len(results)} patient(s).")
                for r in results:
                    with st.expander(f"Patient: {r['name']} ({r['email']})"):
                        st.write(f"**UUID**: {r['uuid']}")
                        st.write(f"**Job/Profession**: {r['job_profession']}")
                        st.write(f"**Health Risk**: {r['health_condition']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.button(f"View Medical History", key=f"hist_{r['uuid']}")
                        with col2:
                            st.button(f"Leave Feedback", key=f"feed_{r['uuid']}")
            else:
                st.warning("No patients found.")

with tab2:
    st.subheader("Expert Profile Configuration")
    st.write(f"**Name**: {st.session_state['user']['name']}")
    st.write("**Specialty**: Nutritionist (Mock)")
    if st.button("Update Profile Details"):
        st.success("Profile updated.")
