import re
import pandas as pd

# Load the dataset
df = pd.read_csv("netdata_metrics_list.csv")
df.head()

# Helper dictionaries to map parts to readable explanations
scope_map = {
    "app": "the application",
    "user": "the user",
    "usergroup": "the user group",
    "system": "the system",
    "cgroup": "the control group (cgroup)",
    "docker": "Docker containers",
    "netdata": "Netdata service",
    "mongodb": "MongoDB instance",
    "disk": "the disk",
    "net": "the network interface",
    "ipv4": "IPv4 network stack",
    "ipv6": "IPv6 network stack",
    "ip": "IP layer",
    "ipvs": "IPVS layer",
    "nfsd": "NFS daemon",
    "sctp": "SCTP layer",
    "mem": "memory subsystem",
}

subsystem_map = {
    "cpu": "CPU usage",
    "mem": "memory usage",
    "vmem": "virtual memory usage",
    "fds": "file descriptors",
    "threads": "threads",
    "uptime": "uptime",
    "processes": "running processes",
    "disk": "disk I/O",
    "io": "I/O operations",
    "net": "network bandwidth",
    "packets": "network packets",
    "latency": "latency",
    "errors": "error events",
    "page_faults": "page faults",
    "swap": "swap usage",
    "utilization": "utilization",
    "pressure": "resource pressure",
    "connections": "network connections",
    "requests": "requests",
}

unit_map = {
    "MiB": "MiB",
    "KiB": "KiB",
    "bytes": "bytes",
    "seconds": "seconds",
    "milliseconds": "milliseconds",
    "microseconds": "microseconds",
    "percentage": "percentage",
    "operations": "operations",
    "packets": "packets",
    "samples": "samples",
    "clients": "clients",
    "sockets": "sockets",
    "events": "events",
    "connections": "connections",
}

def parse_metric_name(metric):
    parts = metric.split("_")
    description = []

    # Extract components
    try:
        if parts[0] == "netdata":
            scope = parts[1]
            subsystem = parts[2] if len(parts) > 2 else ""
        else:
            scope = parts[0]
            subsystem = parts[1] if len(parts) > 1 else ""

        scope_desc = scope_map.get(scope, scope)
        subsystem_desc = subsystem_map.get(subsystem, subsystem.replace("_", " "))

        # Try to extract a unit
        unit_match = re.search(r'_(bytes|MiB|KiB|percentage|seconds|milliseconds|microseconds|operations|packets|samples|clients|sockets|events|connections)', metric)
        unit = unit_match.group(1) if unit_match else None
        unit_text = unit_map.get(unit, unit) if unit else "unit"

        # Determine aggregation (e.g., average, per second)
        if "_persec_" in metric:
            agg = "per second"
        elif "_average" in metric:
            agg = "average"
        else:
            agg = "value"

        description = f"{subsystem_desc.capitalize()} of {scope_desc} in {unit_text} ({agg})"
    except Exception:
        description = "Metric description could not be generated"

    return f'{metric},  # {description}'

# Apply parsing and generate improved descriptions
df["smart_description"] = df["Metric Name"].apply(parse_metric_name)

# Show a few improved descriptions full length not ...
print("\n".join(df["smart_description"].head(1)))

# Save only smart descriptions to a new CSV file
# Remove the first column
df = df.drop(columns=["Metric Name"])
# Save to CSV
df[["smart_description"]].to_csv("netdata_metrics_list_smart.csv", index=False)