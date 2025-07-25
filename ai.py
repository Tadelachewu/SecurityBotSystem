import os
import subprocess
import json
from dotenv import load_dotenv

load_dotenv()

# Set a reasonable token/text chunk size
MAX_CHUNK_SIZE = 4000  # ~4000 characters (adjust if Gemini still complains)

def chunk_text(text: str, chunk_size: int = MAX_CHUNK_SIZE) -> list:
    """Split large log text into chunks to fit within API limits."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def analyze_logs_with_ai(log_text: str) -> str:
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "❌ Error: GEMINI_API_KEY not found in .env file"

        log_chunks = chunk_text(log_text)
        responses = []

        for i, chunk in enumerate(log_chunks):
            prompt = f"""
You are a cybersecurity and system monitoring assistant.

Carefully analyze the following system/network logs for potential:
- security issues,
- suspicious activity,
- performance or health issues.

Be clear, concise, and accurate. Summarize your findings using plain English.
Avoid guessing or over-explaining. Only respond based on evidence from the logs.

Logs Chunk {i+1}:
{chunk}
"""


            data = {
                "contents": [
                    {
                        "parts": [{"text": prompt}]
                    }
                ]
            }

            curl_command = [
                "curl",
                "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                "-H", "Content-Type: application/json",
                "-H", f"X-goog-api-key: {api_key}",
                "-X", "POST",
                "-d", json.dumps(data)
            ]

            result = subprocess.run(curl_command, capture_output=True, text=True)

            if result.returncode != 0:
                responses.append(f"❌ Curl error on chunk {i+1}: {result.stderr}")
                continue

            try:
                response_json = json.loads(result.stdout)
                message = response_json["candidates"][0]["content"]["parts"][0]["text"]
                responses.append(f"🔍 Chunk {i+1} Analysis:\n{message.strip()}")
            except Exception as parse_err:
                responses.append(f"❌ Parse error on chunk {i+1}: {parse_err}")

        return "\n\n".join(responses)

    except Exception as e:
        return f"❌ AI analysis error: {e}"
