import pandas as pd
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import matplotlib
matplotlib.use("TkAgg")  # Use TkAgg backend to avoid conflicts with macOS
import matplotlib.pyplot as plt
import time
import multiprocessing

# File path
csv_file = "./merged_data.csv"

if not os.path.exists(csv_file):
    csv_file = "./data/merged_data.csv"

# Function to update and visualize data
def update_visualization():
    plt.close('all')

    plt.ion()
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    while True:
        try:
            # Load latest data
            df = pd.read_csv(csv_file)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # Select last 60 seconds of data
            last_n_seconds = 60000
            df = df[df["timestamp"] >= df["timestamp"].max() - pd.Timedelta(seconds=last_n_seconds)]

            # Clear and update plots
            axs[0, 0].clear()
            axs[0, 0].plot(df["timestamp"], df["Active UEs"], label="Active UEs", color="blue")
            axs[0, 0].set_title("Active UEs Over Time")

            axs[0, 1].clear()
            axs[0, 1].plot(df["timestamp"], df["Network Traffic In (kbps)"], label="Traffic In", color="green")
            axs[0, 1].plot(df["timestamp"], df["Network Traffic Out (kbps)"], label="Traffic Out", color="red")
            axs[0, 1].set_title("Network Throughput")

            axs[1, 0].clear()
            axs[1, 0].plot(df["timestamp"], df["Packets Received (pps)"], label="Packets Received", color="purple")
            axs[1, 0].plot(df["timestamp"], df["Packets Sent (pps)"], label="Packets Sent", color="orange")
            axs[1, 0].set_title("Packet Flow")

            axs[1, 1].clear()
            axs[1, 1].plot(df["timestamp"], df["CPU Usage (Open5GS)"], label="CPU Usage", color="brown")
            axs[1, 1].set_title("CPU Usage of Open5GS")

            plt.tight_layout()
            fig.canvas.draw()  # **Force the figure to render**
            fig.canvas.flush_events()  # **Force UI update**
            plt.pause(10)  # Refresh every 10 seconds
        except Exception as e:
            print(f"⚠️ Error updating visualization: {e}")

def run_visualization():
    p = multiprocessing.Process(target=update_visualization)
    p.start()
    p.join()

if __name__ == "__main__":
    run_visualization()