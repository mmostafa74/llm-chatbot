# utils.py
import openai
from config import config

openai.api_key = config.api.get("api_key")
openai.api_base = config.api.get("base_url")


def generate_llm_response(prompt: str, model: str, temperature: float = 0.7) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": config.app.get(
                        "system_prompt", "You are a helpful assistant."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=config.api.get("max_tokens", 1024),
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"
