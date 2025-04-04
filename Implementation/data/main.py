# %%
import pandas as pd
from prometheus_api_client import PrometheusConnect, MetricSnapshotDataFrame
from datetime import datetime, timedelta, timezone
import os
import re

# %%
start = datetime.now()

# %%
# Create a connection to prometheus
try:
    prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)
    print("Connected to Prometheus")
except Exception as e:
    print(f"Error connecting to Prometheus: {e}")

# %%
current_time = datetime.now()

# Set start_time as the last processed time (or now - 10 seconds for a buffer)
start_time = (current_time - timedelta(seconds=50)).strftime("%Y-%m-%dT%H:%M:%SZ")
end_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")

step = "50ms"

start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")

# %%
print(f"Start time: {start_time}")
print(f"End time: {end_time}")

# %%
# Labels
device="br-02c136a167f8",                                               # Device name for network metrics (Based on the device name in the Prometheus metrics)
cgroup_name="b48f9356ec91",                                             # Cgroup name for CPU metrics (Based on the cgroup name in the Prometheus metrics)

# %%
# List of important metrics
metrics = [
    # Open5GS metrics
    "amf_session",                                                          # AMF Sessions (Gauge)
    # "bearers_active",                                                       # Active Bearers (Gauge)                                                                     
    # "enb",                                                                  # eNodeBs (Gauge)
    # "enb_ue",                                                               # Number of UEs connected to eNodeBs (Gauge)

    # FiveGS metrics
    ## AMF
    "fivegs_amffunction_amf_authreject",                                    # Number of authentication rejections sent by the AMF (Counter)
    "fivegs_amffunction_amf_authreq",                                       # Number of authentication requests sent by the AMF (Counter)
    "fivegs_amffunction_mm_confupdate",                                     # Number of UE Configuration Update commands requested by the AMF (Counter)
    "fivegs_amffunction_mm_confupdatesucc",                                 # Number of UE Configuration Update complete messages received by the AMF (Counter)
    "fivegs_amffunction_mm_paging5greq",                                    # Number of 5G paging procedures initiated at the AMF (Counter)
    "fivegs_amffunction_mm_paging5gsucc",                                   # Number of successful 5G paging procedures initiated at the AMF (Counter)
    "fivegs_amffunction_rm_regemergreq",                                    # Number of emergency registration requests received by the AMF (Counter)
    "fivegs_amffunction_rm_regemergsucc",                                   # Number of successful emergency registrations at the AMF (Counter)
    "fivegs_amffunction_rm_reginitreq",                                     # Number of initial registration requests received by the AMF (Counter)
    "fivegs_amffunction_rm_reginitsucc",                                    # Number of successful initial registrations at the AMF (Counter)
    "fivegs_amffunction_rm_registeredsubnbr",                               # Number of registered subscribers at the AMF (Gauge)
    "fivegs_amffunction_rm_regmobreq",                                      # Number of mobility registration update requests received by the AMF (Counter)
    "fivegs_amffunction_rm_regmobsucc",                                     # Number of successful mobility registration updates at the AMF (Counter)
    "fivegs_amffunction_rm_regperiodreq",                                   # Number of periodic registration update requests received by the AMF (Counter)
    "fivegs_amffunction_rm_regperiodsucc",                                  # Number of successful periodic registration update requests at the AMF (Counter)

    ## EP_N3_GTP
    "fivegs_ep_n3_gtp_indatapktn3upf",                                      # Number of incoming GTP data packets on the N3 interface (Counter)
    "fivegs_ep_n3_gtp_outdatapktn3upf",                                     # Number of outgoing GTP data packets on the N3 interface (Counter)

    ## SMF
    "fivegs_smffunction_sm_n4sessionestabreq",                              # Number of requested N4 session establishments evidented by SMF (Counter)
    "fivegs_smffunction_sm_n4sessionreport",                                # Number of requested N4 session reports evidented by SMF (Counter)
    "fivegs_smffunction_sm_n4sessionreportsucc",                            # Number of successful N4 session reports evidented by SMF (Counter)
    "fivegs_smffunction_sm_pdusessioncreationreq",                          # Number of PDU sessions requested to be created by the SMF (Counter)
    "fivegs_smffunction_sm_pdusessioncreationsucc",                         # Number of PDU sessions successfully created by the SMF (Counter)
    "fivegs_smffunction_sm_qos_flow_nbr",                                   # Number of QoS flows at the SMF (Gauge)
    "fivegs_smffunction_sm_sessionnbr",                                     # Active Sessions (Gauge)

    ## UPF
    "fivegs_upffunction_sm_n4sessionestabreq",                              # Number of requested N4 session establishments (Counter)
    "fivegs_upffunction_sm_n4sessionreport",                                # Number of requested N4 session reports (Counter)
    "fivegs_upffunction_sm_n4sessionreportsucc",                            # Number of successful N4 session reports (Counter)
    "fivegs_upffunction_upf_qosflows",                                      # Number of QoS flows of UPF (Gauge)
    "fivegs_upffunction_upf_sessionnbr",                                    # Active Sessions (Gauge)

    ## PCF
    "fivegs_pcffunction_pa_policyamassoreq",                                # Number of Policy Association Requests sent by the PCF (Counter)
    "fivegs_pcffunction_pa_policyamassosucc",                               # Number of Policy Association Successes sent by the PCF (Counter)
    "fivegs_pcffunction_pa_policysmassoreq",                                # Number of Policy Session Association Requests sent by the PCF (Counter)
    "fivegs_pcffunction_pa_policysmassosucc",                               # Number of Policy Session Association Successes sent by the PCF (Counter)
    "fivegs_pcffunction_pa_sessionnbr",                                     # Active Sessions (Gauge)

    ## GN RX
    "gn_rx_createpdpcontextreq",                                            # Received GTPv1C CreatePDPContextRequest messages (Counter)
    "gn_rx_deletepdpcontextreq",                                            # Received GTPv1C DeletePDPContextRequest messages (Counter)
    "gn_rx_parse_failed",                                                   # Received GTPv1C messages discarded due to parsing failure (Counter)

    ## GNB
    "gnb",                                                                  # gNodeBs (Gauge) [Real time active gNodeBs]

    ## GTP
    "gtp1_pdpctxs_active",                                                  # Active GTPv1 PDP Contexts (GGSN) (Gauge)
    "gtp2_sessions_active",                                                 # Active GTPv2 Sessions (PGW) (Gauge)
    "gtp_new_node_failed",                                                  # Unable to allocate new GTP (peer) Node (Counter)
    "gtp_peers_active",                                                     # Active GTP peers (Gauge)

    ## MME
    # "mme_session",                                                          # MME Sessions (Gauge)

    ## S5C RX
    "s5c_rx_createsession",                                                 # Received GTPv2C CreateSessionRequest messages (Counter)
    "s5c_rx_parse_failed",                                                  # Received GTPv2C messages discarded due to parsing failure (Counter)

    ## Prometheus metrics scrape
    # "scrape_duration_seconds",                                              # Prometheus scrape duration (Gauge)
    # "scrape_samples_post_metric_relabeling",                                # Prometheus scrape samples post metric relabeling (Gauge)
    # "scrape_samples_scraped",                                               # Prometheus scrape samples scraped (Gauge)
    # "scrape_series_added",                                                  # Prometheus scrape series added (Gauge)

    ## UES
    # "ues_active",                                                           # Active User Equipments (Gauge) [Not real time active UEs but the total number of UEs that have been connected to the network]
    # "ran_ue",                                                               # RAN UEs (Gauge) [Real time active UEs]
    
    ## Up
    "up",                                                                     # 0 = Down, 1 = Up (Gauge)

    ## Process metrics
    # "process_cpu_seconds_total",                                            # Total user and system CPU time spent in seconds (Counter)
    # "process_max_fds",                                                      # Maximum number of open file descriptors (Gauge)
    # "process_open_fds",                                                     # Number of open file descriptors (Gauge)
    # "process_resident_memory_bytes",                                        # Resident memory size in bytes (Gauge)
    # "process_start_time_seconds",                                           # Start time of the process since unix epoch in seconds (Gauge)
    # "process_virtual_memory_bytes",                                         # Virtual memory size in bytes (Gauge)
    # "process_virtual_memory_max_bytes",                                     # Maximum amount of virtual memory available in bytes (Gauge)

    ## NetData metrics for network traffic
    f'netdata_net_net_kilobits_persec_average{{device="{device[0]}", dimension="received"}}',                              # Bandwidth received (Kbps)
    f'netdata_net_net_kilobits_persec_average{{device="{device[0]}", dimension="sent"}}',                                  # Bandwidth sent (Kbps)
    f'netdata_net_packets_packets_persec_average{{device="{device[0]}", dimension="received"}}',                           # Packets received per second
    f'netdata_net_packets_packets_persec_average{{device="{device[0]}", dimension="sent"}}',                               # Packets sent per second

    f'netdata_cgroup_cpu_percentage_average{{cgroup_name="{cgroup_name[0]}"}}',                                            # CPU usage percentage

    f'netdata_cgroup_memory_bytes_average{{cgroup_name="{cgroup_name[0]}"}}',                                              # Memory usage in bytes

    ## Custom metrics
    "currently_active_ues",                                                     # Currently active UEs (Gauge)
    ]

# %%
# Create an empty DataFrame to store all metrics
df_list = []

# %%
import pytz  # For timezone conversion

# Define your local timezone (change this if necessary)
LOCAL_TZ = pytz.timezone("Europe/Bratislava")  # Change if needed

# Fetch metrics and transform timestamps
for metric in metrics:
    try:
        response = prom.custom_query_range(
            metric, start_time=start_time, end_time=end_time, step=step
        )

        # Ensure response is not empty
        if not response:
            print(f"⚠️ Warning: No data for metric {metric}")
            continue

        # Process each metric entry
        for entry in response:
            base_metric_name = entry["metric"]["__name__"]

            # Extract metadata if available
            dimension = entry["metric"].get("dimension", None)
            device = entry["metric"].get("device", None)
            cgroup_name = entry["metric"].get("cgroup_name", None)

            # Construct metric name properly
            metric_name = base_metric_name
            if device and dimension:
                metric_name = f"{base_metric_name}_{device}_{dimension}"
            elif device:
                metric_name = f"{base_metric_name}_{device}"
            elif cgroup_name:
                metric_name = f"{base_metric_name}_{cgroup_name}"

            # Extract and format values with timezone conversion
            if "values" in entry and isinstance(entry["values"], list):
                extracted_values = [
                   (datetime.utcfromtimestamp(int(ts)).replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ), float(val))
                    for ts, val in entry["values"]
                ]

                # Create DataFrame
                metric_df = pd.DataFrame(extracted_values, columns=["timestamp", "value"])
                metric_df["metric_name"] = metric_name

                # Append to list
                df_list.append(metric_df)
            else:
                print(f"⚠️ Warning: No valid values found for {metric}")

    except Exception as e:
        print(f"❌ Error fetching {metric}: {e}")


# %%
if df_list:
    final_df = pd.concat(df_list, ignore_index=True)

# %%
# Remove +01:00 from the timestamp
final_df['timestamp'] = final_df['timestamp'].astype(str).str.replace(r'\+\d{2}:\d{2}', '', regex=True)

# %%
final_df.head()

# %%
log_dir = "../log/"

# Example:
# 03/19 11:20:11.151: [amf] INFO: ngap_server() [172.22.0.10]:38412 (../src/amf/ngap-sctp.c:61)
# 03/19 11:20:11.154: [sctp] INFO: AMF initialize...done (../src/amf/app.c:33)
# 03/19 11:20:11.174: [sbi] INFO: [bd5d91d4-04ab-41f0-8871-a9dc3c5ef804] NF registered [Heartbeat:10s] (../lib/sbi/nf-sm.c:208)
# 03/19 11:20:11.179: [sbi] INFO: NF EndPoint(addr) setup [172.22.0.12:7777] (../lib/sbi/nnrf-handler.c:949)


log_pattern = re.compile(r"(\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3}):\s+\[(\w+)\]\s+(\w+):\s*(.+)")

log_data = []

# %%
# Iterate over all log files in the directory
for log_file in os.listdir(log_dir):
    log_path = os.path.join(log_dir, log_file)
    
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = log_pattern.match(line)
            if match:
                timestamp_str, application, log_level, log_message = match.groups()

                # Convert timestamp to datetime (add missing year)
                log_timestamp = datetime.strptime(timestamp_str, "%m/%d %H:%M:%S.%f")
                log_timestamp = log_timestamp.replace(year=start_time.year)  # Assign correct year

                # 🔹 Remove milliseconds to match Prometheus format
                log_timestamp = log_timestamp.replace(tzinfo=None)
                log_timestamp = log_timestamp.replace(microsecond=0)


                # Check if the log timestamp later than the start time
                if log_timestamp > start_time:
                    log_data.append({
                        "timestamp": log_timestamp,
                        "application": application,
                        "log_level": log_level,
                        "log_message": log_message
                    })


# %%
log_data = pd.DataFrame(log_data)
log_data.head()

# %%
final_df["timestamp"] = pd.to_datetime(final_df["timestamp"])
final_df.head(1)

# %% [markdown]
# log_data and final_df
# ----------------------
# save()

# %%
log_data.to_csv("log_data.csv", index=False)
final_df.to_csv("metrics_data.csv", index=False)

# %%
# Load logs separately before merging
logs = log_data
metrics = final_df

# %%
# 🔹 Aggregate NetData metrics (choose appropriate aggregation: mean, sum, max, etc.)
netdata_aggregated = metrics.groupby(["timestamp", "metric_name"])["value"].mean().reset_index()

# Pivot NetData metrics so each metric has its own column
netdata_pivot = netdata_aggregated.pivot(index="timestamp", columns="metric_name", values="value")

# Flatten column names
netdata_pivot.columns = [f"{col}_value" for col in netdata_pivot.columns]

# Reset index to bring timestamp back
netdata_pivot.reset_index(inplace=True)

print("✅ NetData metrics aggregated and pivoted successfully!")
netdata_pivot.head(3)

# %%
# Move the up_value to the second column after the timestamp
cols = list(netdata_pivot.columns)
cols.remove("up_value")
cols.insert(1, "up_value")
netdata_pivot = netdata_pivot[cols]

# %%
# Define function to classify log messages
def classify_log_message(message):
    if isinstance(message, str):  # Ensure it's a string before applying .lower()
        if "connect" in message.lower():
            return "connect"
        elif "request" in message.lower():
            return "request"
        elif "reject" in message.lower():
            return "reject"
        else:
            return "nothing"
    return "nothing"  # Handle missing or NaN values

# %%
# Ensure log_message column exists before applying classification
if "log_message" in logs.columns:
	logs["log_type"] = logs["log_message"].apply(classify_log_message)
else:
	print("Error: 'log_message' column not found in logs DataFrame")

# %%
logs.head(1)

# %%
# Check if logs DataFrame is not empty before selecting columns
if not logs.empty:
	# Keep only necessary columns from logs
	logs_short = logs[["timestamp", "application", "log_type"]]
else:
	# Create an empty DataFrame if logs is empty
	logs_short = pd.DataFrame(columns=["timestamp", "application", "log_type"])

# %%
logs_short.head(1)

# %%
# Ensure start_time is timezone-aware
start_time_tz_aware = start_time.replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ)

# Convert logs_short timestamp to datetime and ensure it is timezone-aware
logs_short["timestamp"] = pd.to_datetime(logs_short["timestamp"]).dt.tz_localize('UTC').dt.tz_convert(LOCAL_TZ)

# Remove logs before the start time
logs_short = logs_short[logs_short["timestamp"] >= start_time_tz_aware]


# %%
netdata_pivot.head(1)

# %%
# Convert logs_short timestamp to UTC
logs_short["timestamp"] = logs_short["timestamp"].dt.tz_convert("UTC").dt.tz_localize(None)

# Merge logs with NetData metrics
merged_data = pd.merge(netdata_pivot, logs_short, on="timestamp", how="outer")


# %%
merged_data.head()

# %%
# Define a mapping for renaming columns
column_rename_mapping = {
    "fivegs_amffunction_amf_authreject_value": "Auth Reject Count",
    "fivegs_amffunction_amf_authreq_value": "Auth Request Count",
    "fivegs_amffunction_rm_reginitsucc_value": "Registration Success",
    "fivegs_ep_n3_gtp_outdatapktn3upf_value": "Outgoing Data Packets",
    "fivegs_ep_n3_gtp_indatapktn3upf_value": "Incoming Data Packets",
    "fivegs_upffunction_upf_sessionnbr_value": "Session Number",

    # NetData metrics
    "netdata_cgroup_cpu_percentage_average_b48f9356ec91_value": "CPU Usage (Open5GS)",
    "netdata_net_net_kilobits_persec_average_br-02c136a167f8_received_value": "Network Traffic In (kbps)",
    "netdata_net_net_kilobits_persec_average_br-02c136a167f8_sent_value": "Network Traffic Out (kbps)",
    "netdata_net_packets_packets_persec_average_br-02c136a167f8_received_value": "Packets Received (pps)",
    "netdata_net_packets_packets_persec_average_br-02c136a167f8_sent_value": "Packets Sent (pps)",

    # UEs, gnBs and logs
    "ues_active_value": "Active UEs (Total)",
    "application": "Application Name",
    "log_type": "Log Type",
    "gnb_value": "Active gNodeBs",

    # Up status
    "up_value": "Status",

    # Custom metrics
    "currently_active_ues_value": "Currently Active UEs"

}

# Apply renaming
merged_data.rename(columns=column_rename_mapping, inplace=True)

# Print updated column names for verification
print("✅ Updated Column Names:", merged_data.columns)


# %%
csv_file = "merged_data.csv"

# Check if the file exists and is not empty
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    try:
        last_timestamp = pd.read_csv(csv_file, usecols=["timestamp"], nrows=1)["timestamp"].max()
        merged_data = merged_data[merged_data["timestamp"] > last_timestamp]  # Keep only new data
    except pd.errors.EmptyDataError:
        print("⚠️ CSV file is empty. Writing new data without filtering.")
else:
    print("⚠️ CSV file does not exist or is empty. Creating a new one.")

# If the file is empty or does not exist, write with a header
write_header = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0

# Append only new data with a header each time
if not merged_data.empty:
    merged_data.to_csv(csv_file, mode="a", index=False, header=write_header)


print("✅ Data appended efficiently!")



