import streamlit as st
import ui
import ai
from db import get_connection

if 'user' not in st.session_state or st.session_state['user'] is None:
    st.warning("Please log in from the main page.")
    st.stop()

if st.session_state['user']['role'] != 'patient':
    st.error("You do not have access to this page.")
    st.stop()

st.title(f"{st.session_state['user']['name']}'s Dashboard")

# Get User Profile
import auth
profile = auth.get_user_profile(st.session_state['user']['uuid'])

tab1, tab2, tab3 = st.tabs(["Plan & Suggestions", "Log Food", "Upload Report"])

with tab1:
    st.subheader("Smart Suggestions")
    # Fetch recent logs count (mocked for now)
    suggestions = ai.generate_smart_suggestions(profile, recent_logs=[])
    for sug in suggestions:
        st.info(sug)
        
    st.subheader("My Nutrition & Activity Plan")
    st.markdown(ai.generate_nutrition_plan(profile, medical_history={}))
    
    st.subheader("Metrics")
    col1, col2, col3 = st.columns(3)
    with col1: ui.render_metric_card("Calories Today", "1,200", "kcal")
    with col2: ui.render_metric_card("Protein", "45", "g")
    with col3: ui.render_metric_card("Sedentary Time", "4.5", "hrs")

with tab2:
    st.subheader("Log a Meal")
    log_type = st.radio("Log via", ["Manual Entry", "Image Scan", "Voice Input"])
    
    if log_type == "Manual Entry":
        food_name = st.text_input("Food Item")
        cal = st.number_input("Calories", min_value=0)
        if st.button("Log Food"):
            st.success(f"Logged: {food_name} ({cal} kcal)")
            
    elif log_type == "Image Scan":
        uploaded_file = st.file_uploader("Upload food image", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            if st.button("Analyze with AI"):
                with st.spinner("Analyzing..."):
                    result = ai.analyze_food_image(uploaded_file.read())
                    st.success(f"Looks like {result['name']}! ({result['calories']} kcal)")
                    # Would save to db here

    elif log_type == "Voice Input":
        st.info("🎤 Voice input is simulated in this browser prototype.")
        st.button("Start Recording")
        if st.button("Mock Transcription: 'I had avocado toast for breakfast'"):
            st.success("Parsed: Avocado Toast (350 kcal). Logged!")

with tab3:
    st.subheader("Upload Medical Report")
    report_file = st.file_uploader("Upload PDF or Image", type=["pdf", "jpg", "png"])
    if report_file:
        if st.button("Extract Data"):
            with st.spinner("Running OCR & LLM Extraction..."):
                metadata = ai.parse_medical_report(report_file)
                st.json(metadata)
                st.success("Successfully updated your medical profile!")
