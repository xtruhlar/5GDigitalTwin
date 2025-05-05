import pandas as pd

# 📅 Define intervals for each Use Case (UC) based on experiment timestamps
uc1_interval = { "from": "2025-04-11 09:54:00", "to": "2025-04-11 10:05:00" }
uc2_interval = { "from": "2025-04-10 13:46:00", "to": "2025-04-10 13:57:20" }
uc3_interval = { "from": "2025-04-10 13:28:00", "to": "2025-04-10 13:41:20" }
uc4_interval = { "from": "2025-04-10 13:13:35", "to": "2025-04-10 13:23:33" }
uc5_interval = { "from": "2025-04-10 14:05:48", "to": "2025-04-10 14:06:30" }
uc6_interval = { "from": "2025-04-14 12:52:30", "to": "2025-04-14 12:56:30" }

def compare_intervals(row, interval):
    """
    Compare a timestamp from a row with a given time interval.

    Args
        - row (pd.Series): Row from the DataFrame with a 'timestamp' column.
        - interval (dict): Dictionary with "from" and "to" datetime strings.

    Returns
        - bool: True if timestamp is within interval, else False.
    """
    start = pd.to_datetime(interval["from"])
    end = pd.to_datetime(interval["to"])
    timestamp = pd.to_datetime(row['timestamp'])
    return start <= timestamp <= end

def apply_uc(row):
    """
    Assign a Use Case (UC) label to a row based on its timestamp.

    Args
        - row (pd.Series): A row with a 'timestamp' field.

    Returns
        - str: The UC label ('uc1' to 'uc6').
    """
    if compare_intervals(row, uc1_interval):
        return 'uc1'
    elif compare_intervals(row, uc2_interval):
        return 'uc2'
    elif compare_intervals(row, uc3_interval):
        return 'uc3'
    elif compare_intervals(row, uc4_interval):
        return 'uc4'
    elif compare_intervals(row, uc5_interval):
        return 'uc5'
    elif compare_intervals(row, uc6_interval):
        return 'uc6'
    else:
        return 'uc1'  # Default fallback label

def label_realnetwork_csv(input_path='../datasets/real_network_data_before_labeling.csv', output_path='../datasets/real_network_data_after_labeling.csv'):
    """
    Load the CSV, assign UC labels to each row, and save the updated file.

    Args
        - input_path (str): Path to the input CSV file.
        - output_path (str): Path to save the labeled CSV file.

    Returns
        None
    """
    raw_df = pd.read_csv(input_path)
    raw_df['current_uc'] = raw_df.apply(apply_uc, axis=1)
    raw_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    label_realnetwork_csv()
