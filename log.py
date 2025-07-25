import platform
import subprocess
import os
import sys

def read_log_tail(lines=100):
    system = platform.system()
    machine = platform.machine()
    try:
        # Desktop: Linux/macOS
        if system in ["Linux", "Darwin"]:
            log_paths = ["/var/log/syslog", "/var/log/messages", "/var/log/system.log"]
            for log_file in log_paths:
                if os.path.exists(log_file):
                    with open(log_file, "r") as file:
                        return f"📄 Log from {log_file}:\n" + "\n".join(file.readlines()[-lines:])
            return "❌ No standard log file found."

        # Windows
        elif system == "Windows":
            command = [
                "powershell",
                "-Command",
                f"Get-EventLog -LogName System -Newest {lines} | Format-Table -AutoSize"
            ]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            return f"📄 Windows Event Logs:\n{output}"

        # Android (Termux or rooted Python)
        elif "android" in platform.platform().lower() or "arm" in machine:
            try:
                output = subprocess.check_output(["logcat", "-d", f"-t {lines}"], stderr=subprocess.STDOUT, text=True)
                return f"📄 Android logcat output:\n{output}"
            except Exception as logcat_err:
                return f"⚠️ Android logcat error: {logcat_err}\nTry running in Termux with permissions."

        # iOS (not supported due to sandboxing)
        elif "ios" in system.lower() or "iphone" in machine.lower():
            return "❌ iOS logging access is restricted due to Apple's sandboxing."

        else:
            return f"❌ Unsupported or unknown platform: {system}, {machine}"

    except Exception as e:
        return f"❌ Error reading log: {e}"
