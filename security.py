import subprocess
import platform
import psutil
import socket
import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()

def check_open_ports():
    try:
        connections = psutil.net_connections(kind='inet')
        open_ports = set()
        for conn in connections:
            if conn.status == 'LISTEN':
                open_ports.add(conn.laddr.port)
        return sorted(list(open_ports))
    except Exception as e:
        return f"Error checking open ports: {e}"

def check_firewall_status():
    try:
        system = platform.system().lower()
        if system == 'windows':
            # Windows firewall status (simplified)
            cmd = ['netsh', 'advfirewall', 'show', 'allprofiles']
            output = subprocess.check_output(cmd, text=True)
            if "State ON" in output:
                return "Firewall is ON"
            else:
                return "Firewall is OFF"
        elif system == 'linux':
            # Check ufw (Uncomplicated Firewall) status on Linux
            try:
                output = subprocess.check_output(['ufw', 'status'], text=True)
                return output.strip()
            except Exception:
                return "Firewall status check not supported or ufw not installed"
        elif system == 'darwin':
            # macOS firewall status
            output = subprocess.check_output(['/usr/libexec/ApplicationFirewall/socketfilterfw', '--getglobalstate'], text=True)
            return output.strip()
        else:
            return "Unsupported OS for firewall check"
    except Exception as e:
        return f"Error checking firewall status: {e}"

def check_suspicious_processes():
    suspicious_keywords = ['netcat', 'nc', 'ncat', 'powershell', 'cmd.exe', 'bash', 'curl', 'wget']
    suspicious = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
            cmdline = " ".join(proc.info['cmdline']) if proc.info['cmdline'] else ""
            if any(keyword in cmdline.lower() for keyword in suspicious_keywords):
                suspicious.append(f"PID {proc.pid}: {proc.info['name']} ({proc.info['username']}) - Cmd: {cmdline}")
        if suspicious:
            return suspicious
        else:
            return ["No suspicious processes found."]
    except Exception as e:
        return [f"Error checking suspicious processes: {e}"]

def check_logged_in_users():
    try:
        users = psutil.users()
        user_list = [f"{user.name} (started: {user.started})" for user in users]
        if user_list:
            return user_list
        else:
            return ["No logged in users detected."]
    except Exception as e:
        return [f"Error fetching logged-in users: {e}"]


def perform_security_checks():
    report_lines = []
    open_ports = check_open_ports()
    firewall_status = check_firewall_status()
    suspicious_processes = check_suspicious_processes()
    logged_in_users = check_logged_in_users()

    report_lines.append("🔐 Security Module Report:\n")

    if isinstance(open_ports, list):
        report_lines.append(f"Open Listening Ports: {', '.join(str(p) for p in open_ports)}")
    else:
        report_lines.append(open_ports)

    report_lines.append(f"Firewall Status: {firewall_status}")

    report_lines.append("\nSuspicious Processes:")
    report_lines.extend(suspicious_processes)

    report_lines.append("\nLogged-in Users:")
    report_lines.extend(logged_in_users)

    # Compose full report text for AI analysis
    full_report = "\n".join(report_lines)

    # Call AI to analyze and generate recommendations
    ai_summary = analyze_security_with_ai(full_report)

    # Return combined report + AI summary
    return ai_summary
    # return full_report + "\n\n🧠 AI Analysis & Recommendations:\n" + ai_summary


def analyze_security_with_ai(text: str) -> str:
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "❌ Error: GEMINI_API_KEY not found."

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        prompt = (
            "You are a cybersecurity analyst. Analyze the following system-generated log or security report.\n"
            "Your task is to do the following:\n"
            "1. For each line in the report, explain clearly what is happening in human-readable terms.\n"
            "2. Translate any technical jargon or codes into simple explanations.\n"
            "3. If a log line indicates a threat or risk, mention it clearly.\n"
            "4. Provide a structured summary:\n"
            "   - 3 to 5 key observations\n"
            "   - Overall risk level\n"
            "   - Actionable recommendations\n"
            "Use clear, readable formatting. No markdown or code syntax.\n\n"
            f"Security Report Input:\n{text}\n"
        )

        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key
        }

        data = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code != 200:
            return f"❌ AI API error: HTTP {response.status_code} - {response.text}"

        ai_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return ai_text.strip()

    except Exception as e:
        return f"❌ AI analysis error: {e}"