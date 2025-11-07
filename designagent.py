import requests
import config as config
import json

OPENROUTER_API_KEY = config.OPENROUTER_API_KEY
api_url = "https://openrouter.ai/api/v1/chat/completions"

def call_ai_api(messages, model="openai/gpt-oss-20b", temperature=0.7):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://alixer.io",
        "X-Title": "DesignAgent",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        message_content = result.get("choices", [{}])[0].get("message", {}).get("content")
        if not message_content:
            return None, "AI response was empty or malformed."
        return message_content.strip(), None

    except requests.exceptions.RequestException as e:
        return None, f"Failed to communicate with the AI service: {str(e)}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return None, f"Invalid response format from the AI service: {str(e)}"

def refine_prompt(user_input):
    system_prompt = (
        "You are a professional English prompt refiner. "
        "Your task is to take the user's raw message and rewrite it into a clear, "
        "grammatically correct, and well-structured prompt for a design generation agent. "
        "Do not include formatting symbols such as asterisks, hashtags, or markdown. "
        "Do not make any design or layout suggestions yourself. "
        "Simply transform the user's message into a polished, unambiguous prompt "
        "that the design agent can easily interpret."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    return call_ai_api(messages, temperature=0.7)

def generate_design(refined_prompt):
    system_prompt = (
        "You are a professional UI/UX designer and landing page expert. "
        "Your task is to analyze the refined prompt and create a detailed, "
        "visually appealing design plan that includes:\n"
        "1. Layout structure and composition\n"
        "2. Color palette with specific hex codes\n"
        "3. Typography choices and hierarchy\n"
        "4. Component styling and interactions\n"
        "5. Responsive design considerations\n"
        "6. Visual elements and imagery suggestions\n"
        "Format the response in a clear, structured manner that developers "
        "and designers can easily understand and implement."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": refined_prompt}
    ]

    return call_ai_api(messages, temperature=0.8)

def process_design_request(user_input):
    # Step 1: Refine the user's prompt
    refined_prompt, error = refine_prompt(user_input)
    if error:
        return None, error

    # Step 2: Generate design plan based on refined prompt
    design_plan, error = generate_design(refined_prompt)
    if error:
        return None, error

    # Return both the refined prompt and the design plan
    result = {
        "refined_prompt": refined_prompt,
        "design_plan": design_plan
    }
    
    return result, None