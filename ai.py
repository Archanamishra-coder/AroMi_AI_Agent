import time
import json
import random

# In a real application, you would configure openai or google.generativeai here
# e.g., openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_medical_report(text_or_image_path):
    """
    Mock integration for OCR + LLM Parsing.
    In reality, this would send the image to an OCR engine or Vision LLM
    and extract structured JSON data.
    """
    time.sleep(1) # Simulate API call
    return {
        "blood_pressure": "120/80",
        "allergies": ["Peanuts", "Dust"],
        "key_conditions": ["Mild Hypertension Risk", "Vitamin D Deficiency"],
        "raw_text_summary": "Patient showed normal vital signs but has a family history of hypertension."
    }

def generate_nutrition_plan(user_profile, medical_history):
    """
    Mock LLM calling to generate a personalized plan based on context.
    """
    job = user_profile.get('job_profession', 'General Professional')
    health = user_profile.get('health_condition', 'Generally Healthy')
    locality = user_profile.get('locality', 'Urban Area')
    
    time.sleep(1.5) # Simulate LLM Generation
    
    plan = f"""
    ### 🍽️ Personalized Nutrition Plan
    **Context Identified:**
    - Job: {job}
    - Location: {locality}
    - Conditions to Monitor: {health}
    
    **Recommendations:**
    - 🗓️ **Breakfast:** High-protein oatmeal with local seasonal fruits from {locality}.
    - 🥙 **Lunch:** Quick salads or wrap suitable for a busy {job} schedule.
    - 🥦 **Dinner:** Lean protein (chicken or tofu) with steamed vegetables. Low sodium to manage health risks.
    """
    return plan

def generate_smart_suggestions(user_profile, recent_logs):
    """
    Mock context-aware suggestions (e.g. sedentary warnings).
    """
    job = user_profile.get('job_profession', 'General Professional').lower()
    
    suggestions = []
    if any(keyword in job for keyword in ['desk', 'software', 'it', 'manager', 'clerk', 'office']):
        suggestions.append("⚠️ **Sedentary Alert**: You have a desk job. Remember to stand up and stretch for 5 minutes every hour!")
    
    if len(recent_logs) < 2:
        suggestions.append("💡 **Suggestion**: You haven't logged many meals today. Want a quick recipe recommendation based on your plan?")
        
    if not suggestions:
        suggestions.append("✅ Great job staying active and eating healthy!")
        
    return suggestions

def analyze_food_image(image_bytes):
    """
    Mock Vision API for food scanning.
    """
    time.sleep(1)
    
    foods = [
        {"name": "Avocado Toast", "calories": 350, "protein": 10, "carbs": 30, "fats": 22},
        {"name": "Caesar Salad", "calories": 250, "protein": 8, "carbs": 12, "fats": 18},
        {"name": "Grilled Chicken", "calories": 400, "protein": 45, "carbs": 5, "fats": 15}
    ]
    return random.choice(foods)
