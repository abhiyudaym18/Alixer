import requests
import config
import json

OPENROUTER_API_KEY = config.OPENROUTER_API_KEY
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def design_prompt(messages):
    """
    Sends a refined prompt to OpenRouter and returns design variations.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://alixer.io",  # Required by OpenRouter
        "X-Title": "DesignAgent",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": messages,
        "temperature": 0.7,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        message_content = (
            result.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not message_content:
            return None, "AI response was empty or malformed."

        return message_content, None

    except requests.exceptions.RequestException as e:
        return None, f"Failed to communicate with the AI service: {str(e)}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return None, f"Invalid response format from the AI service: {str(e)}"


def generate_designs(refined_prompt: str):
    """
    Takes a refined prompt from PromptAgent and generates
    4 detailed design variation suggestions.
    """

    system_prompt = (
        "You are a professional web designer. "
        "Your task is to create visually appealing and user-friendly website designs. "
        "Generate 4 distinct design variations based on the refined prompt. "
        "Focus on layout, color scheme, typography, and user experience. "
        "Each variation should be described in detail and clearly separated."
        "Do not include formatting symbols such as asterisks, hashtags, or markdown."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": refined_prompt},
    ]

    design_response, error = design_prompt(messages)

    print("Design Response:", design_response)
    if error:
        return None, f"DesignAgent Error: {error}"

    return design_response, None


# Optional: Allow local testing
if __name__ == "__main__":
    refined = input("Enter a refined prompt (from PromptAgent): ").strip()
    response, err = generate_designs(refined)
    if err:
        print("❌ Error:", err)
    else:
        print("\n🎨 Design Variations:\n")
        print(response)
