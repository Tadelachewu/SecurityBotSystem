import subprocess
import platform
import socket
import psutil

def get_network_interfaces():
    interfaces = psutil.net_if_addrs()
    result = []
    for interface, addrs in interfaces.items():
        ips = [addr.address for addr in addrs if addr.family == socket.AF_INET]
        result.append(f"{interface}: {', '.join(ips)}")
    return result

def ping_google():
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        output = subprocess.check_output(["ping", param, "4", "8.8.8.8"], stderr=subprocess.STDOUT)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Ping failed:\n{e.output.decode('utf-8')}"

def get_active_connections():
    try:
        connections = psutil.net_connections(kind='inet')
        result = []
        for conn in connections[:10]:  # limit to 10 for brevity
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "?"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "?"
            result.append(f"{laddr} → {raddr} [{conn.status}]")
        return result
    except Exception as e:
        return [f"Error fetching connections: {e}"]

def collect_network_data():
    try:
        interfaces = get_network_interfaces()
        ping_result = ping_google()
        connections = get_active_connections()

        report = (
            "🌐 Network Interfaces:\n" + "\n".join(interfaces) +
            "\n\n📶 Ping to 8.8.8.8:\n" + ping_result +
            "\n\n🔗 Active Connections:\n" + "\n".join(connections)
        )
        return report
    except Exception as e:
        return f"❌ Network analysis error: {e}"
