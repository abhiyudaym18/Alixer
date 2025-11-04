import requests
import config as config
import json
import desginagent


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
        "model": "oqwen/qwen-2.5-coder-32b-instruct:free",
        "messages": messages,
        "temperature": 0.7
    }

system_prompt = (
    "you are a professional web developer. "
    )

messages = [
    {"role": "system", "content": system_prompt},
]

userask = input("Enter your prompt: ")
call_ai_api(userask)
