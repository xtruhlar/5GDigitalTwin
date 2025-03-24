# physical_network_simulator.py
import random
import pandas as pd
from datetime import datetime, timedelta

def simulate_ue_connections(duration_secs=120, interval_secs=5):
    now = datetime.utcnow()

    print(f"📈 Simulating UE connections for {duration_secs} seconds, every {interval_secs} seconds...")

    timestamps = [now - timedelta(seconds=i*interval_secs) for i in range(duration_secs)][::-1]
    active_ues = [random.randint(0, 3) for _ in timestamps]

    print(f"📈 Simulated {duration_secs} seconds of UE connections:")

    df = pd.DataFrame({"timestamp": timestamps, "Active UEs": active_ues})
    # Round timestamps to seconds
    df["timestamp"] = df["timestamp"].dt.round("1s")

    print(df)

    df.to_csv("./data/physical_simulated.csv", index=False)

simulate_ue_connections(120)
