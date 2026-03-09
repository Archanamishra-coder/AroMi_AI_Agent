import streamlit as st
import pandas as pd
from datetime import date
from db import get_db_connection
from ai import parse_medical_report, scan_food_image, generate_personalized_plan, get_smart_suggestions

def make_header(text, bg_color):
    st.markdown(f'<div style="background-color: {bg_color}; padding: 10px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);"><h2>{text}</h2></div>', unsafe_allow_html=True)

def patient_dashboard():
    st.markdown('<div style="background: linear-gradient(90deg, #4CAF50, #8BC34A); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px;"><h1>Patient Dashboard</h1></div>', unsafe_allow_html=True)
    user_uuid = st.session_state["user"]['uuid']
    name = st.session_state["user"]['name']
    
    st.write(f"Welcome back, **{name if name else 'Patient'}**!")
    
    menu_selection = st.sidebar.selectbox("≡ Menu", ["Profile & Medical History", "My Plans", "Food Tracker", "Smart Suggestions"])
    
    if menu_selection == "Profile & Medical History":
        make_header("My Profile", "#FF7043")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT dob, profession, location, profile_photo FROM users WHERE uuid=?", (user_uuid,))
        user_profile = c.fetchone()
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if user_profile and user_profile['profile_photo']:
                st.image(user_profile['profile_photo'], width=150)
            else:
                st.image("https://via.placeholder.com/150", width=150)
            
            new_photo = st.file_uploader("Update Photo", type=["png", "jpg", "jpeg"], key="photo_upload")
            if new_photo:
                photo_bytes = new_photo.read()
                c.execute("UPDATE users SET profile_photo=? WHERE uuid=?", (photo_bytes, user_uuid))
                conn.commit()
                st.success("Photo updated!")
                st.rerun()
                
        with col2:
            st.write(f"**Unique ID:** `{user_uuid}`")
            st.write(f"**Name:** {name}")
            
            with st.form("profile_form"):
                dob_val = user_profile['dob'] if user_profile and user_profile['dob'] else ""
                prof_val = user_profile['profession'] if user_profile and user_profile['profession'] else ""
                loc_val = user_profile['location'] if user_profile and user_profile['location'] else ""
                
                new_dob = st.date_input("Date of Birth", value=pd.to_datetime(dob_val).date() if dob_val else date(2000, 1, 1))
                new_prof = st.text_input("Profession", value=prof_val)
                new_loc = st.text_input("Location", value=loc_val)
                
                if st.form_submit_button("Save Profile"):
                    c.execute("UPDATE users SET dob=?, profession=?, location=? WHERE uuid=?", (new_dob, new_prof, new_loc, user_uuid))
                    conn.commit()
                    st.success("Profile saved!")
                    st.rerun()
        conn.close()
        st.divider()

        st.subheader("Medical History")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM medical_history WHERE patient_uuid = ? ORDER BY updated_at DESC LIMIT 1", (user_uuid,))
        history = c.fetchone()
        conn.close()
        
        if history:
            st.info(f"**Conditions:** {history['conditions']}")
            st.info(f"**Allergies:** {history['allergies']}")
            st.write(f"**Report Summary:** {history['report_summary']}")
        else:
            st.warning("No medical history found. Please upload a report to auto-fill.")
            
        st.markdown("### Upload Medical Report")
        uploaded_file = st.file_uploader("Upload PDF or Image (JPEG/PNG)", type=['png', 'jpg', 'jpeg'], key="med_upload")
        if uploaded_file is not None:
             if st.button("Parse Report with AI"):
                 with st.spinner("Analyzing..."):
                     extracted_data = parse_medical_report(uploaded_file)
                     if extracted_data:
                         summary = extracted_data.get("summary", "")
                         conditions = ", ".join(extracted_data.get("conditions", []))
                         allergies = ", ".join(extracted_data.get("allergies", []))
                         
                         conn = get_db_connection()
                         c = conn.cursor()
                         c.execute(
                             "INSERT INTO medical_history (patient_uuid, report_summary, conditions, allergies) VALUES (?, ?, ?, ?)",
                             (user_uuid, summary, conditions, allergies)
                         )
                         conn.commit()
                         conn.close()
                         st.success("Medical profile updated successfully!")
                         st.rerun()
                     else:
                         st.error("Failed to parse report.")
                         
        st.divider()
        st.subheader("Medical Progress")
        conn = get_db_connection()
        progress_df = pd.read_sql_query("SELECT date, calories FROM food_logs WHERE patient_uuid=? ORDER BY date", conn, params=(user_uuid,))
        conn.close()
        
        if not progress_df.empty:
            st.write("**Calorie Intake Over Time**")
            progress_df = progress_df.groupby('date').sum().reset_index()
            st.line_chart(data=progress_df, x='date', y='calories')
        else:
            st.info("Log some meals in the Food Tracker to see your medical progress graph.")

    elif menu_selection == "My Plans":
        make_header("Personalized Nutrition & Activity Plan", "#2196F3")
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM medical_history WHERE patient_uuid = ? ORDER BY updated_at DESC LIMIT 1", (user_uuid,))
        history = c.fetchone()
        conn.close()
        
        if history:
             if st.button("Generate New AI Plan"):
                 with st.spinner("Generating plan based on your latest medical data..."):
                     history_dict = dict(history)
                     plan = generate_personalized_plan(history_dict, "Budget friendly, mostly vegetarian")
                     st.session_state['latest_plan'] = plan
                     
             if 'latest_plan' in st.session_state:
                 st.markdown(st.session_state['latest_plan'])
             else:
                 st.info("Click the button above to generate your plan.")
        else:
            st.warning("Upload medical history first to generate personalized plans.")
            
    elif menu_selection == "Food Tracker":
        make_header("Food Tracker & Vision AI Scanner", "#FF9800")
        food_upload = st.file_uploader("Scan your meal", type=['png', 'jpg', 'jpeg'], key="food_upload")
        if food_upload is not None:
             if st.button("Scan Food"):
                 with st.spinner("Identifying food and calories..."):
                     food_data = scan_food_image(food_upload)
                     if food_data:
                         st.write(f"**Identified:** {food_data['item_name']}")
                         st.write(f"Calories: {food_data['calories']} | Protein: {food_data['protein']}g | Carbs: {food_data['carbs']}g | Fat: {food_data['fat']}g")
                         
                         # Log to DB
                         conn = get_db_connection()
                         c = conn.cursor()
                         c.execute(
                             "INSERT INTO food_logs (patient_uuid, date, food_item, calories, protein, carbs, fat) VALUES (?, ?, ?, ?, ?, ?, ?)",
                             (user_uuid, date.today(), food_data['item_name'], food_data['calories'], food_data['protein'], food_data['carbs'], food_data['fat'])
                         )
                         conn.commit()
                         conn.close()
                         st.success("Meal logged successfully!")
                     else:
                         st.error("Failed to scan food.")
                         
        st.subheader("Today's Log")
        conn = get_db_connection()
        logs_df = pd.read_sql_query("SELECT food_item, calories, protein, carbs, fat FROM food_logs WHERE patient_uuid=? AND date=?", conn, params=(user_uuid, date.today()))
        conn.close()
        if not logs_df.empty:
            st.dataframe(logs_df)
            st.metric("Total Calories", logs_df['calories'].sum())
        else:
            st.write("No meals logged today.")
            
    elif menu_selection == "Smart Suggestions":
         make_header("Smart Suggestions", "#00BCD4")
         conn = get_db_connection()
         logs_df = pd.read_sql_query("SELECT food_item, calories, protein, carbs, fat FROM food_logs WHERE patient_uuid=? AND date=?", conn, params=(user_uuid, date.today()))
         conn.close()
         if not logs_df.empty:
              if st.button("Get Coach Feedback"):
                  with st.spinner("Analyzing recent logs..."):
                       items = logs_df['food_item'].tolist()
                       suggestion = get_smart_suggestions(items)
                       st.success(suggestion)
         else:
              st.info("Log some meals to get smart suggestions on your diet.")
              
         st.divider()
         st.subheader("Location Aware Ingredient Search")
         st.write("*(Feature relying on local/Google Maps lookup)*")
         search_ing = st.text_input("Find fresh ingredient nearby:")
         if st.button("Search Local Stores"):
              # Mocking Google Maps response for MVP visually
              st.write(f"🏪 **Whole Foods Market** (0.8 miles) - In stock")
              st.write(f"🏪 **Trader Joe's** (1.2 miles) - In stock")
              st.write(f"🏪 **Local Farmer's Market** (2.0 miles) - Open Tomorrow")


def admin_dashboard():
    st.markdown('<div style="background: linear-gradient(90deg, #673AB7, #9C27B0); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 25px;"><h1>Admin / Expert Dashboard</h1></div>', unsafe_allow_html=True)
    expert_uuid = st.session_state["user"]['uuid']
    name = st.session_state["user"]['name']
    
    st.write(f"Welcome, **{name if name else 'Expert'}**!")
    
    make_header("Patient Search & Monitoring", "#3F51B5")
    
    conn = get_db_connection()
    patients_df = pd.read_sql_query("SELECT uuid, name, email, created_at FROM users WHERE role='patient'", conn)
    conn.close()
    
    if patients_df.empty:
        st.write("No patients registered yet.")
        return
        
    patient_sel = st.selectbox("Select Patient to View", options=patients_df['uuid'], format_func=lambda x: f"{patients_df[patients_df['uuid']==x]['name'].values[0]} ({patients_df[patients_df['uuid']==x]['email'].values[0]})")
    
    if patient_sel:
        tab1, tab2, tab3 = st.tabs(["Medical Outline", "Diet Logs", "Provide Feedback"])
        
        with tab1:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM medical_history WHERE patient_uuid = ? ORDER BY updated_at DESC LIMIT 1", (patient_sel,))
            history = c.fetchone()
            conn.close()
            if history:
                st.write(f"**Conditions:** {history['conditions']}")
                st.write(f"**Allergies:** {history['allergies']}")
                st.write(f"**Report Summary:** {history['report_summary']}")
            else:
                st.write("No medical history uploaded.")
                
        with tab2:
            conn = get_db_connection()
            p_logs_df = pd.read_sql_query("SELECT date, food_item, calories FROM food_logs WHERE patient_uuid=? ORDER BY date DESC", conn, params=(patient_sel,))
            conn.close()
            if not p_logs_df.empty:
                st.dataframe(p_logs_df)
            else:
                st.write("No food logs for this patient.")
                
        with tab3:
            feedback = st.text_area("Write feedback / adjust plan recommendations:")
            if st.button("Send Feedback"):
                 conn = get_db_connection()
                 c = conn.cursor()
                 c.execute(
                     "INSERT INTO expert_feedback (patient_uuid, expert_uuid, feedback_text) VALUES (?, ?, ?)",
                     (patient_sel, expert_uuid, feedback)
                 )
                 conn.commit()
                 conn.close()
                 st.success("Feedback saved and sent to patient.")
