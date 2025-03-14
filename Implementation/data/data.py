import re
from datetime import datetime

def parse_logs(log_files):
    """Parses Open5GS log files and extracts UE registration metrics."""

    registration_metrics = {
        "requested_registrations": 0,
        "failed_registrations": 0,
        "registration_timestamps": [],
        "failure_timestamps": [],
    }

    for log_file in log_files:
        with open(log_file, "r") as f:
            for line in f:
                # Successful registration pattern (adjust as needed)
                success_match = re.search(r"Registration request", line)
                if success_match:
                    registration_metrics["requested_registrations"] += 1
                    timestamp = extract_timestamp(line)
                    if timestamp:
                        registration_metrics["registration_timestamps"].append(timestamp)

                # Failed registration pattern (adjust as needed)
                failure_match = re.search(r"Registration reject", line) #or a specific error message
                if failure_match:
                    registration_metrics["failed_registrations"] += 1
                    timestamp = extract_timestamp(line)
                    if timestamp:
                        registration_metrics["failure_timestamps"].append(timestamp)

    return registration_metrics

def extract_timestamp(log_line):
    """Extracts timestamp from a log line."""
    timestamp_match = re.search(r"(\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3})", log_line)
    if timestamp_match:
        try:
            return datetime.strptime(timestamp_match.group(1), "%m/%d %H:%M:%S.%f")
        except ValueError:
            return None
    return None

if __name__ == "__main__":
    log_files = [
        "./log/amf.log",
        "./log/smf.log",
        "./log/ausf.log",
        # Add other log file names here
    ]

    metrics = parse_logs(log_files)
    print("UE Registration Metrics:")
    print(f"  Requested Registrations: {metrics['requested_registrations']}")
    print(f"  Failed Registrations: {metrics['failed_registrations']}")
    print("  Registration Timestamps:")
    for ts in metrics['registration_timestamps']:
        print(f"    {ts.strftime('%m/%d %H:%M:%S.%f')}")
    print("  Failure Timestamps:")
    for ts in metrics['failure_timestamps']:
        print(f"    {ts.strftime('%m/%d %H:%M:%S.%f')}")

    # You can save the metrics to a CSV file.
    import csv
    with open('registration_metrics.csv', 'w', newline='') as csvfile:
        fieldnames = ['Requested Registrations', 'Failed Registrations', 'Registration Timestamps', 'Failure Timestamps']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({
            'Requested Registrations': metrics['requested_registrations'],
            'Failed Registrations': metrics['failed_registrations'],
            'Registration Timestamps': [ts.strftime('%m/%d %H:%M:%S.%f') for ts in metrics['registration_timestamps']],
            'Failure Timestamps': [ts.strftime('%m/%d %H:%M:%S.%f') for ts in metrics['failure_timestamps']]
        })