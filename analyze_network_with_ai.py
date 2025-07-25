import os
import json
import subprocess

def analyze_network_with_ai(log_text: str) -> str:
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "❌ Error: GEMINI_API_KEY not found."

        prompt = (
            "You are a professional network security analyst.\n"
            "You are given a block of raw network logs to review.\n\n"
            "Instructions:\n"
            "1. For each line in the log, write a clear and brief explanation in plain language.\n"
            "   - Mention what kind of traffic or event it is (e.g., ping, connection, DNS, etc).\n"
            "   - Specify if it seems normal or suspicious, and why.\n"
            "   - Avoid using technical jargon unless necessary, and explain it when used.\n"
            "2. After reviewing all lines, provide a structured final analysis with clearly numbered sections:\n"
            "   1. Summary of Key Observations\n"
            "   2. Potential Security Risks\n"
            "   3. Recommended Actions\n"
            "3. Do NOT use markdown or special symbols like asterisks, dashes, emojis, or code blocks.\n"
            "4. Keep the tone formal, clear, and concise. Avoid repetition.\n\n"
            f"Network Logs:\n{log_text}\n\n"
            "Begin your line-by-line explanation now, followed by the summary sections and a closing note."
        )

        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
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

        result = subprocess.run(curl_command, capture_output=True, text=True, timeout=20)

        if result.returncode != 0:
            return f"❌ AI API error: {result.stderr}"

        response_json = json.loads(result.stdout)
        ai_text = response_json["candidates"][0]["content"]["parts"][0]["text"]

        return ai_text.strip()

    except Exception as e:
        return f"❌ AI analysis error: {e}"
