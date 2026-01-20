import os
import requests
import config as config
import json

OPENROUTER_API_KEY = config.OPENROUTER_API_KEY
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def call_ai_api(messages, model="kwaipilot/kat-coder-pro:free", temperature=0.2):
    """Call the OpenRouter API and return (content, error)."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://alixer.io",
        "X-Title": "CodingAgent",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=data, timeout=120)
        resp.raise_for_status()
        result = resp.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content")
        if not content:
            return None, "AI response empty or malformed"
        return content.strip(), None
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {e}"
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return None, f"Invalid response format: {e}"


def generate_html_from_design(design_plan, output_dir="generated"):
    """Generate HTML file from the design plan."""

    system_prompt = (
        "You are a professional web developer and front-end engineer. "
        "Generate a single, complete, self-contained HTML document that implements the design plan provided by the user. "
        "Use only HTML, CSS and JavaScript. All CSS must be internal (inside a single <style> tag in the <head>) and all JavaScript must be internal (inside a single <script> tag before </body>). "
        "Do NOT include external stylesheets, CDN links, or external scripts. Do not reference external images — if imagery is suggested, use descriptive placeholders or data URIs. "
        "The output must be a valid HTML5 document, responsive, and accessible. Include minimal inline comments only if necessary. "
        "Output ONLY the HTML document (the full file contents) and nothing else."
    )

    user_message = (
        f"Design plan (implement exactly and faithfully):\n{design_plan}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    code_content, error = call_ai_api(messages, temperature=0.15)
    if error:
        return None, f"Code generation failed: {error}"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "index.html")

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(code_content)
        return out_path, None
    except OSError as e:
        return None, f"Failed to write output file: {e}"


# Optional CLI for testing
if __name__ == "__main__":
    import designagent

    user_prompt = input("Enter your design prompt: ").strip()
    if not user_prompt:
        print("Prompt cannot be empty")
        exit(1)

    # Get design plan from designagent
    result, error = designagent.process_design_request(user_prompt)
    if error:
        print("Design agent error:", error)
        exit(1)

    design_plan = result.get("design_plan", "")

    # Generate HTML from design plan
    output_path, error = generate_html_from_design(design_plan)
    if error:
        print(f"Error: {error}")
        exit(1)

    print(f"Generated HTML saved to: {output_path}")
