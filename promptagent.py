import requests
import config as config
import json

OPENROUTER_API_KEY = config.OPENROUTER_API_KEY
api_url = "https://openrouter.ai/api/v1/chat/completions"


def call_ai_api(messages):
   
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://alixer.io",  # required by OpenRouter
        "X-Title": "PromptAgent",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": messages,
        "temperature": 0.7
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
