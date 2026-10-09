
from datetime import datetime
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent
EVENTS_FILE = BASE_DIR / "events.log"
ALERTS_FILE = BASE_DIR / "alerts.log"

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with EVENTS_FILE.open("a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")

def create_alert(message, severity="MEDIUM"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert = f"[{timestamp}] [{severity}] {message}"
    with ALERTS_FILE.open("a", encoding="utf-8") as file:
        file.write(alert + "\n")
    print(f"\n🚨 SECURITY ALERT: {severity}")
    print(message)

def analyze_logs():
    import subprocess

    print("\n[*] Analyzing SSH authentication logs...")

    try:
        result = subprocess.run(
            ["journalctl", "-u", "ssh", "--no-pager", "-n", "500"],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode != 0:
            result = subprocess.run(
                ["sudo", "journalctl", "-u", "ssh", "--no-pager", "-n", "500"],
                capture_output=True,
                text=True,
                timeout=15
            )

        if result.returncode != 0:
            print("[!] Could not read SSH logs.")
            print(result.stderr.strip())
            return

        content = result.stdout
        failed = re.findall(
            r"Failed password.*",
            content,
            re.IGNORECASE
        )

        print(f"[*] Failed login events found: {len(failed)}")

        ip_counts = {}

        for event in failed:
            match = re.search(r"\bfrom\s+([0-9a-fA-F:.]+)", event)

            if match:
                ip = match.group(1)
                ip_counts[ip] = ip_counts.get(ip, 0) + 1

            log_event(event)

        if not ip_counts:
            print("[+] No failed SSH login IPs detected in these logs.")

        for ip, count in ip_counts.items():
            if count >= 5:
                create_alert(
                    f"Possible brute-force activity from {ip} "
                    f"({count} failed attempts)",
                    "HIGH"
                )
            else:
                print(f"[*] {ip}: {count} failed attempt(s)")

    except subprocess.TimeoutExpired:
        print("[!] Reading logs timed out.")
    except Exception as error:
        print(f"[!] Error: {error}")

def demo_mode():
    print("\n[*] Running safe demonstration...")
    demo_ip = "192.0.2.10"
    create_alert(
        f"Demo: 5 simulated failed logins from {demo_ip}",
        "HIGH"
    )
    log_event(f"Demo security event from {demo_ip}")
    print("[+] Demo completed.")

def alert_summary():
    print("\n===== MINI SIEM ALERT SUMMARY =====")

    if not ALERTS_FILE.exists():
        print("No alerts recorded.")
        return

    alerts = ALERTS_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    if not alerts:
        print("No alerts recorded.")
        return

    high = sum("[HIGH]" in line for line in alerts)
    medium = sum("[MEDIUM]" in line for line in alerts)
    low = sum("[LOW]" in line for line in alerts)

    print(f"Total Alerts  : {len(alerts)}")
    print(f"HIGH Severity : {high}")
    print(f"MEDIUM Severity: {medium}")
    print(f"LOW Severity  : {low}")
    print("===================================")

def main():
    print("=" * 42)
    print("       MINI SIEM SECURITY MONITOR")
    print("=" * 42)
    print("1. Analyze system logs")
    print("2. Run safe demo")
    print("3. View recent alerts")
    print("4. Alert Summary")
    print("5. Exit")

    choice = input("\nSelect option: ").strip()

    if choice == "1":
        analyze_logs()
    elif choice == "2":
        demo_mode()
    elif choice == "3":
        if ALERTS_FILE.exists():
            print(ALERTS_FILE.read_text(encoding="utf-8") or "No alerts yet.")
        else:
            print("No alerts yet.")
    elif choice == "4":
            alert_summary()
    elif choice == "5":
            print("Exiting Mini SIEM.")
    else:
        print("Invalid choice. Run the program again.")

if __name__ == "__main__":
    main()
