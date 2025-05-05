# Standard libraries
import argparse
import glob
import json
import os
import re
import shutil
import threading
import time
from datetime import datetime

# Third-party libraries
import joblib
import nbformat
import numpy as np
import pandas as pd
import schedule
import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras import backend as K
from tensorflow.keras import initializers
from tensorflow.keras.models import load_model
from nbconvert.preprocessors import ExecutePreprocessor
from prometheus_client import Gauge, start_http_server
from pygtail import Pygtail
    
# Global variables
LOG_FILE = "/open5gs/install/var/log/open5gs/amf.log"
SEQUENCE_LENGTH = 60
LOOP_COUNTER = 0
OUTPUT_FILE = "./data/running_data.csv"

# Loading model and scaler
MODEL_PATH = "/app/data/Model/trained_models/lstm_attention_model.keras"
SCALER_PATH = "/app/data/Model/scaler/scaler.joblib"
FEATURES_PATH = "/app/data/Model/json/selected_features.json"

SCALER = joblib.load(SCALER_PATH)

# Loading selected metrics
with open(FEATURES_PATH, "r") as f:
    SELECTED_FEATURES = json.load(f)['features']

# Ensuring the backup directory exists
if not os.path.exists("./data/backup"):
    os.makedirs("./data/backup", exist_ok=True)


# 📐 Prometheus - Custom metrics (mainly serves as an example of how to combine different approaches for obtaining network data)
ue_reg_time_last = Gauge("ue_registration_duration_seconds_last", "Last registration duration")
ue_reg_time_avg = Gauge("ue_registration_duration_seconds_avg", "Average registration duration")
ue_reg_time_min = Gauge("ue_registration_duration_seconds_min", "Min registration duration")
ue_reg_time_max = Gauge("ue_registration_duration_seconds_max", "Max registration duration")
ue_sess_time_last = Gauge("ue_session_duration_seconds_last", "Last session duration")
ue_sess_time_avg = Gauge("ue_session_duration_seconds_avg", "Average session duration")
ue_sess_time_min = Gauge("ue_session_duration_seconds_min", "Min session duration")
ue_sess_time_max = Gauge("ue_session_duration_seconds_max", "Max session duration")
# 📐 Prometheus - Custom metrics for UC prediction
predicted_uc_metric = Gauge("classified_uc_class", "Classified current use case (UC) by LSTM model")
true_uc_metric = Gauge("true_uc_class", "True current use case (UC) from data")
model_loss = Gauge("model_loss", "Model loss during fine-tuning")
predicted_uc_confidence = Gauge("classified_uc_confidence", "Confidence score of predicted use case")


class AttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name='att_weight', shape=(input_shape[-1], 1),
                                 initializer='glorot_uniform', trainable=True)
        self.b = self.add_weight(name='att_bias', shape=(input_shape[1], 1),
                                 initializer='zeros', trainable=True)
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        e = K.tanh(K.dot(x, self.W) + self.b)  
        a = K.softmax(e, axis=1)              
        output = x * a                         
        return K.sum(output, axis=1)           

    def compute_output_shape(self, input_shape):
        return (input_shape[0], input_shape[-1])
    
MODEL = load_model(MODEL_PATH, custom_objects={"AttentionLayer": AttentionLayer}, compile=False)
MODEL.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


def truncate_running_data(csv_path, keep_last_n=SEQUENCE_LENGTH):

    """Truncate the given CSV file to keep only the last `keep_last_n` rows."""

    try:
        df = pd.read_csv(csv_path)
        if len(df) > keep_last_n:
            df = df.tail(keep_last_n)
            df.to_csv(csv_path, index=False)
            print(f"🧹 Truncated {csv_path} to last {keep_last_n} records.")
    except Exception as e:
        print(f"⚠️ Could not truncate {csv_path}: {e}")


def run_notebook_in_thread():

    """Run the main.ipynb notebook in a separate daemon thread."""

    thread = threading.Thread(target=run_main_notebook_with_backup)
    thread.daemon = True
    thread.start()


def run_main_notebook_with_backup():

    """Execute the main.ipynb notebook, log its execution, truncate CSV, and periodically create CSV backups."""

    global LOOP_COUNTER
    print("📓 main.ipynb loop...")

    start_time = time.time()

    try:
        with open("./data/main.ipynb", "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
        ep.preprocess(notebook)

        with open("./data/log_execution.log", "a") as log:
            log.write(f"{datetime.now()}: ✅ Notebook was executed successfully.\n")

        truncate_running_data(OUTPUT_FILE, keep_last_n=SEQUENCE_LENGTH)

        if os.path.exists(OUTPUT_FILE) and LOOP_COUNTER % 600 == 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join("./data/backup" , f"backup_{timestamp}.csv")
            shutil.copy(OUTPUT_FILE, backup_file)
            with open("./data/log_execution.log" , "a") as log:
                log.write(f"{datetime.now()}: 🔒 Backup created: {backup_file}\n")

    except Exception as e:
        error_message = f"{datetime.now()}: ❌ Error while executing notebook: {e}"
        print(error_message)
        with open("./data/log_execution.log", "a") as log:
            log.write(error_message + "\n")
        time.sleep(3)

    end_time = time.time()
    print(f"⏱️ Notebook execution time: {end_time - start_time:.2f} seconds")

    LOOP_COUNTER += 1


def predict_current_uc(latest_window_df):

    """Predict the current use case (UC) using the loaded LSTM model based on the latest data window."""

    if len(latest_window_df) < SEQUENCE_LENGTH:
        return -1, -1.0

    # Select only the last SEQUENCE_LENGTH rows
    window = latest_window_df[SELECTED_FEATURES].tail(SEQUENCE_LENGTH)
    window_scaled = SCALER.transform(window)
    window_scaled = np.expand_dims(window_scaled, axis=0)

    prediction = MODEL.predict(window_scaled, verbose=0)
    predicted_uc = np.argmax(prediction)
    confidence = float(prediction[0][predicted_uc])

    return predicted_uc, confidence


def load_last_sequence(csv_path, selected_features, sequence_length=SEQUENCE_LENGTH):

    """Load the last sequence of records from CSV, ensuring all required features and labels are present."""

    try:
        df = pd.read_csv(csv_path)
        df = df.tail(sequence_length)

        # Check if all selected features are present in the DataFrame
        missing = [f for f in selected_features if f not in df.columns]
        if missing:
            raise ValueError(f"Missing features in input: {missing}")
        
        # Load the correct labels
        if "current_uc" not in df.columns:
            raise ValueError("Missing 'current_uc' column in input data.")
        else:
            correct_labels = df["current_uc"].copy()

        # Select only the required features
        df = df[selected_features].copy()
        df = df.ffill().fillna(0)

        return df, correct_labels
    
    except Exception as e:
        print(f"❌ Failed to load sequence: {e}")

        return None, None


def remove_offset():

    """Remove the offset file used by Pygtail to start reading the log file from the beginning."""

    offset_file = f"{LOG_FILE}.offset"
    if os.path.exists(offset_file):
        os.remove(offset_file)
        print(f"Removed offset file: {offset_file}")
    else:
        print("No offset file found.")


def parse_amf(lines, previous_state):

    """
    Parse AMF log lines to extract UE registration and deregistration events, 
    update UE states, and compute registration/session durations.
    """

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
            full_time = f"{datetime.now().year}/{time_match.group(1)} {time_match.group(2)}"
            timestamp = datetime.strptime(full_time, "%Y/%m/%d %H:%M:%S.%f")

        # Initial Registration
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
        if "Registration complete" in line and current_reg.get("imsi") and current_reg.get("start_time"):
            imsi = current_reg["imsi"]
            ue = ue_details.get(imsi, {
                "suci": current_reg.get("suci", "unknown"),
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

        # Last SUCI
        if match := re.search(r'SUCI\[(suci-[^\]]+)\]', line):
            last_seen_suci = match.group(1)

        # Last IMSI
        if match := re.search(r'imsi-(\d+)', line):
            current_imsi = match.group(1)

        # Deregistration
        if "UE Context Release" in line or "Implicit De-registered" in line or "De-register UE" in line:
            dereg_block.append(line)

        if dereg_block and "SUCI" in line:
            imsi_match = re.search(r'imsi-(\d+)', line)
            suci_match = re.search(r'SUCI\[(suci-[^\]]+)\]', line)
            dereg_time = timestamp

            imsi = imsi_match.group(1) if imsi_match else current_imsi
            suci = suci_match.group(1) if suci_match else last_seen_suci

            # SUCI to IMSI conversion
            if suci and len(suci) == 33:
                sufix = suci[-10:]
                tac = suci[7:10]
                nci = suci[11:13]
                imsi = f"{tac}{nci}{sufix}"

            # First, we look for IMSI
            if imsi and imsi in ue_details:
                ue = ue_details[imsi]
            # If IMSI is not found, we look for SUCI
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


def save_model_with_date(model, path_prefix="/app/data/Model/Model_bn_"):

    """Save the current model to disk with the current date as part of the filename."""

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{path_prefix}{today}.keras"
    model.save(filename)
    print(f"💾 Model saved as {filename}")
    clean_old_models()


def clean_old_models(directory="/app/data/Model", keep_last_n=7, pattern="Model_bn_*.keras"):

    """Keep only the last `keep_last_n` saved model files and delete older ones."""

    files = sorted(glob.glob(os.path.join(directory, pattern)), key=os.path.getmtime, reverse=True)
    if len(files) > keep_last_n:
        for file in files[keep_last_n:]:
            try:
                os.remove(file)
                print(f"🗑️ Model deleted: {file}")
            except Exception as e:
                print(f"⚠️ Failed to delete {file}: {e}")


def main_loop(interval=1, prometheus_port=9000):

    """Main loop that monitors UE activity, parses logs, updates Prometheus metrics, and fine-tunes the model in real-time."""
    
    print(f"📡 Tracking UEs every {interval}s and exporting to Prometheus on port {prometheus_port}...\n")
    start_http_server(prometheus_port)

    previous_state = {
        "ue_details": {},
        "reg_durations": [],
        "session_durations": [],
        "connected_ue_history": [],
        "max_connected_ue_count": 0
    }

    schedule.every(1).seconds.do(run_notebook_in_thread)

    try:
        while True:
            lines = list(Pygtail(LOG_FILE, offset_file=f"{LOG_FILE}.offset", encoding="latin-1"))
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

            # 📨 Export to Prometheus
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

            current_df, correct_labels = load_last_sequence("/app/data/running_data.csv", SELECTED_FEATURES, SEQUENCE_LENGTH)
            if current_df is not None:
                predicted_uc, confidence = predict_current_uc(current_df)
                predicted_uc_metric.set(predicted_uc)
                predicted_uc_confidence.set(confidence)
                X_finetune = SCALER.transform(current_df[SELECTED_FEATURES])
                X_finetune = np.expand_dims(X_finetune, axis=0)

                y_finetune = np.array([correct_labels.iloc[-1]])
                y_finetune_cat = tf.keras.utils.to_categorical([y_finetune], num_classes=MODEL.output_shape[-1])

                # Fine-tuning the model
                history = MODEL.fit(X_finetune, y_finetune_cat, epochs=3, verbose=0)
                model_loss.set(float(history.history['loss'][-1]))
                print(f"✅ Fine-tuned on UC {y_finetune}")

                # Prediction after fine-tuning
                prediction = MODEL.predict(X_finetune, verbose=0)
                predicted_uc = np.argmax(prediction)
                confidence = float(prediction[0][predicted_uc])
                predicted_uc_metric.set(predicted_uc)
                predicted_uc_confidence.set(confidence)
                if correct_labels is not None:
                    true_uc_metric.set(correct_labels.iloc[-1])
                else:
                    true_uc_metric.set(-1)
                print(f"🔮 Predicted UC after fine-tuning: {predicted_uc}")

            else:
                print("❌ Failed to load current sequence for prediction.")
                continue

            if len(current_df) != SEQUENCE_LENGTH:
                print("❌ Current DataFrame length is not equal to SEQUENCE_LENGTH.")
                continue

            # 🖥️  Output to terminal
            print("\033[H\033[J", end="")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"🕒 Timestamp:       {timestamp}")
            print(f"📓 Notebook:        main.ipynb running ✅")
            print(f"🧹 CSV Truncate:    {OUTPUT_FILE} → last {SEQUENCE_LENGTH} rows\n")

            print("📈 Connected UEs")
            print(f"   ├ current        : {connected_now}")
            print(f"   ├ predicted UC   : {predicted_uc_metric._value.get()}")
            print(f"   ├ real UC        : {correct_labels.iloc[-1]}")
            print(f"   ├ max connected  : {previous_state['max_connected_ue_count']}")
            print(f"   ├ avg connected  : {sum(ue_counts) / len(ue_counts):.2f}")
            print(f"   └ active IMSIs   : {', '.join(active_imsis) if active_imsis else 'None'}\n")

            if reg_times:
                print("⏱️  Registration Time")
                print(f"   ├ last           : {reg_times[-1]:.3f}")
                print(f"   ├ min            : {min(reg_times):.3f}")
                print(f"   ├ max            : {max(reg_times):.3f}")
                print(f"   └ avg            : {sum(reg_times) / len(reg_times):.3f}")
            else:
                print("⏱️  Registration Time\n   └ no data yet")

            if sess_times:
                print("\n📉 Session Duration")
                print(f"   ├ last           : {sess_times[-1]:.3f}")
                print(f"   ├ min            : {min(sess_times):.3f}")
                print(f"   ├ max            : {max(sess_times):.3f}")
                print(f"   └ avg            : {sum(sess_times) / len(sess_times):.3f}")
            else:
                print("\n📉 Session Duration\n   └ no data yet")

            print("\n🔮 Prediction")
            print(f"   ├ Before tuning  : {predicted_uc}")
            print(f"   ├ After tuning   : {predicted_uc_metric._value.get()}")
            print(f"   └ Confidence     : {predicted_uc_confidence._value.get():.3f}")

            print("\n📉 Fine-tuning")
            print(f"   ├ Real UC        : [{correct_labels.iloc[-1]}]")
            print(f"   ├ Loss history   : {history.history['loss']}")
            print(f"   └ Last loss      : {history.history['loss'][-1]:.3f}")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


            schedule.every().day.at("04:00").do(save_model_with_date, model=MODEL)
            schedule.run_pending()
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