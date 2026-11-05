
import requests
from django.conf import settings


def explain_topic(topic):
    api_key = settings.GROQ_API_KEY

    if not api_key:
        return "Groq API key is missing. Please check your .env file."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are EduMind, a friendly student tutor. "
                    "Explain topics in simple beginner-friendly language. "
                    "Use headings, examples and important points."
                )
            },
            {
                "role": "user",
                "content": f"Explain this topic: {topic}"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException:
        return "Unable to connect to Groq. Please check your internet connection and API settings."

    except (KeyError, IndexError, ValueError):
        return "Unexpected response from Groq. Please try again."
