import os
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_base64_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def parse_medical_report(image_file):
    """
    Simulates or calls actual LLM Vision model to extract medical history from an image.
    If no API key provided, returns mock data for demo purposes.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return {
            "summary": "Mock: Patient shows signs of mild hypertension and Vitamin D deficiency.",
            "conditions": ["Hypertension (Mild)", "Vitamin D Deficiency"],
            "allergies": ["Penicillin"]
        }
        
    base64_img = get_base64_image(image_file)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract the medical history, summary, existing conditions, and allergies from this medical report. Return the result strictly in JSON format with keys: 'summary', 'conditions' (list of strings), 'allergies' (list of strings)."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]
                }
            ],
            max_tokens=600,
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error parsing medical report: {e}")
        return None

def scan_food_image(image_file):
    """
    Extracts nutritional info from a food picture.
    """
    if not os.getenv("OPENAI_API_KEY"):
         return {
             "item_name": "Mock: Grilled Chicken Salad",
             "calories": 350,
             "protein": 30,
             "carbs": 15,
             "fat": 12
         }

    base64_img = get_base64_image(image_file)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this food image. Identify the dish and estimate its nutritional breakdown. Return strictly in JSON format with keys: 'item_name' (string), 'calories' (integer), 'protein' (integer, grams), 'carbs' (integer, grams), 'fat' (integer, grams)."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]
                }
            ],
            max_tokens=400,
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error scanning food: {e}")
        return None

def generate_personalized_plan(medical_profile_json, preferences=""):
    """
    Generates a personalized nutrition and activity plan based on medical profile.
    """
    if not os.getenv("OPENAI_API_KEY"):
         return "Mock Plan: Eat more leafy greens (Vitamin D), reduce sodium (Hypertension). Suggested Activity: 30 minutes brisk walking daily."
         
    prompt = f"""
    You are an expert AI Health Coach. 
    Based on the following medical profile: {json.dumps(medical_profile_json)}
    And user preferences: {preferences}
    
    Create a highly personalized 1-day sample nutrition plan and a weekly activity plan. 
    Format your response in Markdown, highlighting specific recipes, target metrics, and exercises.
    Consider allergies avoiding certain foods and conditions demanding specific diets.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert personalized health and lifestyle coach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating plan: {e}")
        return "Failed to generate plan due to an error."

def get_smart_suggestions(recent_logs):
    """
    Given an array of recent food logs, return a short smart suggestion.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return "Mock Suggestion: You've been eating well! Try adding a bit more protein to your next meal."
        
    prompt = f"Analyze these recent food logs: {recent_logs}. Give one short, actionable, friendly health tip (1-2 sentences) on what to eat next or how to adjust their diet."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a supportive, concise nutrition coach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating suggestion: {e}")
        return "Keep up the great work! Make sure to stay hydrated."
