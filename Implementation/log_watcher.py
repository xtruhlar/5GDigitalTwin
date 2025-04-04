import os
import re
import time
import argparse
from datetime import datetime
from collections import defaultdict
from pygtail import Pygtail
from prometheus_client import Gauge, start_http_server

CURRENT_YEAR = datetime.now().year
LOG_FILE = "./log/amf.log"

# Prometheus metrics
ue_connected = Gauge("ue_connected_total", "Currently connected UEs")

ue_reg_time_last = Gauge("ue_registration_duration_seconds_last", "Last registration duration")
ue_reg_time_avg = Gauge("ue_registration_duration_seconds_avg", "Average registration duration")
ue_reg_time_min = Gauge("ue_registration_duration_seconds_min", "Min registration duration")
ue_reg_time_max = Gauge("ue_registration_duration_seconds_max", "Max registration duration")
ue_sess_time_last = Gauge("ue_session_duration_seconds_last", "Last session duration")
ue_sess_time_avg = Gauge("ue_session_duration_seconds_avg", "Average session duration")
ue_sess_time_min = Gauge("ue_session_duration_seconds_min", "Min session duration")
ue_sess_time_max = Gauge("ue_session_duration_seconds_max", "Max session duration")

def remove_offset():
    offset_file = f"{LOG_FILE}.offset"
    if os.path.exists(offset_file):
        os.remove(offset_file)
        print(f"Removed offset file: {offset_file}")
    else:
        print("No offset file found.")

def parse_amf(lines, previous_state):
    ue_details = previous_state["ue_details"]
    new_reg_durations = []
    new_session_durations = []

    registration_block = []
    dereg_block = []
    current_reg = {
        "start_time": None,
        "suci": None,
        "imsi": None
    }

    current_imsi = None
    last_seen_suci = None 

    for line in lines:
        timestamp = None
        time_match = re.match(r'(\d{2}/\d{2}) (\d{2}:\d{2}:\d{2}\.\d{3})', line)
        if time_match:
            full_time = f"{CURRENT_YEAR}/{time_match.group(1)} {time_match.group(2)}"
            timestamp = datetime.strptime(full_time, "%Y/%m/%d %H:%M:%S.%f")

        # Start of registration
        if "InitialUEMessage" in line:
            current_reg = {
                "start_time": timestamp,
                "suci": None,
                "imsi": None
            }
            registration_block = []

        registration_block.append(line)

        # SUCI
        if match := re.search(r'\[(suci-[^\]]+)\]', line):
            current_reg["suci"] = match.group(1)

        # IMSI
        if match := re.search(r'imsi-(\d+)', line):
            current_reg["imsi"] = match.group(1)

        # Registration complete
        if "Registration complete" in line and current_reg["imsi"]:
            imsi = current_reg["imsi"]
            ue = ue_details.get(imsi, {
                "suci": current_reg["suci"],
                "imsi": imsi,
                "reg_start": current_reg["start_time"],
                "reg_end": None,
                "reg_duration": None,
                "deregistered_at": None,
                "session_duration": None,
                "status": "UNKNOWN"
            })
            ue["reg_end"] = timestamp
            ue["status"] = "REGISTERED"

            # Calculate registration duration
            if ue["reg_start"] and ue["reg_end"] and not ue["reg_duration"]:
                ue["reg_duration"] = (ue["reg_end"] - ue["reg_start"]).total_seconds()
                new_reg_durations.append(ue["reg_duration"])

            ue_details[imsi] = ue
            current_reg = {}

        # Track last seen SUCI
        if match := re.search(r'SUCI\[(suci-[^\]]+)\]', line):
            last_seen_suci = match.group(1)

        # Track last seen IMSI (always)
        if match := re.search(r'imsi-(\d+)', line):
            current_imsi = match.group(1)

        # Deregistration by SUCI or IMSI
        # 04/04 21:18:41.076: [amf] INFO: UE Context Release [Action:2] (../src/amf/ngap-handler.c:1733)
        # 04/04 21:18:41.076: [amf] INFO:     RAN_UE_NGAP_ID[153] AMF_UE_NGAP_ID[268] (../src/amf/ngap-handler.c:1734)
        # 04/04 21:18:41.076: [amf] INFO:     SUCI[suci-0-001-01-0000-0-0-1234567810] (../src/amf/ngap-handler.c:1738)
        # 04/04 21:18:41.076: [amf] INFO: [Removed] Number of gNB-UEs is now 0 (../src/amf/context.c:2685)

        # If 2 lines before this line contain "UE Context Release" or "Implicit De-registered" or "De-register UE"
        # and the line contains "SUCI" or "imsi-" or suci, then it's a deregistration

        if "UE Context Release" in line or "Implicit De-registered" in line or "De-register UE" in line:
            dereg_block.append(line)

        if dereg_block and "SUCI" in line:
            imsi_match = re.search(r'imsi-(\d+)', line)
            suci_match = re.search(r'SUCI\[(suci-[^\]]+)\]', line)
            dereg_time = timestamp

            imsi = imsi_match.group(1) if imsi_match else current_imsi
            suci = suci_match.group(1) if suci_match else last_seen_suci

            #suci to imsi conversion
            # imsi-001011234567803
            # suci-0-001-01-0000-0-0-1234567803
            # The last 10 digits of the SUCI are the IMSI

            if suci and len(suci) == 33:
                sufix = suci[-10:]
                tac = suci[7:10]
                nci = suci[11:13]
                imsi = f"{tac}{nci}{sufix}"

            # Try matching IMSI first
            if imsi and imsi in ue_details:
                ue = ue_details[imsi]
            # Fallback to SUCI if IMSI is missing
            elif suci:
                ue = next((u for u in ue_details.values() if u["suci"] == suci and u["status"] == "REGISTERED"), None)
            else:
                ue = None

            if ue:
                ue["deregistered_at"] = dereg_time
                ue["status"] = "DEREGISTERED"
                if ue.get("reg_end") and ue["deregistered_at"] and not ue["session_duration"]:
                    duration = (ue["deregistered_at"] - ue["reg_end"]).total_seconds()
                    ue["session_duration"] = duration
                    new_session_durations.append(duration)


    return ue_details, new_reg_durations, new_session_durations

def main_loop(interval=5, prometheus_port=9000):
    print(f"📡 Tracking UEs every {interval}s and exporting to Prometheus on port {prometheus_port}...\n")
    start_http_server(prometheus_port)

    previous_state = {
        "ue_details": {},
        "reg_durations": [],
        "session_durations": [],
        "connected_ue_history": [],
        "max_connected_ue_count": 0
    }

    try:
        while True:
            lines = list(Pygtail(LOG_FILE, offset_file=f"{LOG_FILE}.offset"))
            ue_details, new_regs, new_sessions = parse_amf(lines, previous_state)

            previous_state["ue_details"] = ue_details
            previous_state["reg_durations"].extend(new_regs)
            previous_state["session_durations"].extend(new_sessions)


            connected_now = sum(1 for ue in ue_details.values() if ue["status"] == "REGISTERED")
            active_imsis = [ue["imsi"] for ue in ue_details.values() if ue["status"] == "REGISTERED"]

            previous_state["connected_ue_history"].append(connected_now)
            if connected_now > previous_state["max_connected_ue_count"]:
                previous_state["max_connected_ue_count"] = connected_now

            reg_times = previous_state["reg_durations"]
            sess_times = previous_state["session_durations"]
            ue_counts = previous_state["connected_ue_history"]

            # Export to Prometheus
            ue_connected.set(connected_now)
            if reg_times:
                ue_reg_time_last.set(reg_times[-1])
                ue_reg_time_avg.set(sum(reg_times) / len(reg_times))
                ue_reg_time_min.set(min(reg_times))
                ue_reg_time_max.set(max(reg_times))
            if sess_times:
                ue_sess_time_last.set(sess_times[-1])
                ue_sess_time_avg.set(sum(sess_times) / len(sess_times))
                ue_sess_time_min.set(min(sess_times))
                ue_sess_time_max.set(max(sess_times))

            # Terminal output with overwrite
            print("\033[H\033[J", end="")  # Clear the terminal
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n🕒 {timestamp}")
            print(f"📈 Connected UEs:")
            print(f"   ├ current: {connected_now}")
            print(f"   ├ max:     {previous_state['max_connected_ue_count']}")
            print(f"   ├ list:    {', '.join(active_imsis) if active_imsis else 'None'}")
            print(f"   └ avg:     {sum(ue_counts) / len(ue_counts):.2f}")

            if reg_times:
                print(f"⏱️  Registration Time (s):\n   ├ last:    {reg_times[-1]:.3f}\n   ├ min:     {min(reg_times):.3f}\n   ├ max:     {max(reg_times):.3f}\n   └ avg:     {sum(reg_times) / len(reg_times):.3f}")
            else:
                print("⏱️  Registration Time: no data yet")

            if sess_times:
                print(f"📉 Session Duration (s):\n   ├ last:    {sess_times[-1]:.3f}\n   ├ min:     {min(sess_times):.3f}\n   ├ max:     {max(sess_times):.3f}\n   └ avg:     {sum(sess_times) / len(sess_times):.3f}")
            else:
                print("📉 Session Duration: no data yet")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n🛑 Stopped tracking.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UE log watcher + Prometheus exporter.")
    parser.add_argument("-r", "--remove-offset", action="store_true", help="Remove offset file.")
    parser.add_argument("--interval", type=int, default=5, help="Refresh interval in seconds.")
    parser.add_argument("--port", type=int, default=9000, help="Port to serve Prometheus metrics.")
    args = parser.parse_args()

    if args.remove_offset:
        remove_offset()
    else:
        main_loop(interval=args.interval, prometheus_port=args.port)


# python log_watcher.py --interval 1 --port 9000
