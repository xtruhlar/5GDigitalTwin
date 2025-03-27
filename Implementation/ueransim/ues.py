from prometheus_client import start_http_server, Gauge
import re
import threading
import time

# === CONFIG ===
GNB_CONTAINER_NAME = "nr_gnb"
METRIC_PORT = 9000  # Port to expose Prometheus metric

# === PROMETHEUS METRIC ===
active_ues_metric = Gauge(
    "currently_active_ues",
    "Number of currently active UEs connected to gNB",
    ['gnb_id']
)

# === TRACKING STATE ===
connected_ues = set()
ue_connect_pattern = re.compile(r"RRC Setup for UE\[(\d+)\]")
ue_disconnect_pattern = re.compile(r"UE\[(\d+)\] signal lost")

# === FUNCTION TO PARSE LOG LINE ===
def process_log_line(line):
    connect_match = ue_connect_pattern.search(line)
    if connect_match:
        ue_id = connect_match.group(1)
        connected_ues.add(ue_id)
        print(f"📶 UE[{ue_id}] connected. Total: {len(connected_ues)}")
        return

    disconnect_match = ue_disconnect_pattern.search(line)
    if disconnect_match:
        ue_id = disconnect_match.group(1)
        connected_ues.discard(ue_id)
        print(f"❌ UE[{ue_id}] disconnected. Total: {len(connected_ues)}")

# === FUNCTION TO MONITOR LOGS ===
def monitor_gnb_logs():
    print(f"📡 Tail-following local log file /mnt/ueransim/gnb.log")
    with open("/mnt/ueransim/gnb.log", "r") as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            process_log_line(line)


# === METRIC UPDATER ===
def update_metrics_loop():
    while True:
        active_ues_metric.labels(gnb_id="ueransim-gnb").set(len(connected_ues))
        time.sleep(1)

# === MAIN ===
def main():
    print("🚀 Starting Prometheus metrics exporter...")
    start_http_server(METRIC_PORT)

    # Start background metric updater
    threading.Thread(target=update_metrics_loop, daemon=True).start()

    # Start log monitoring (blocking)
    monitor_gnb_logs()

# Run main if script is executed directly
if __name__ == "__main__":
    main()


