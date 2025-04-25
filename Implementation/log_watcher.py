import os
import re
import time
import argparse
from datetime import datetime
from pygtail import Pygtail
from prometheus_client import Gauge, start_http_server
import joblib
import json
import numpy as np
import pandas as pd
import schedule
import tensorflow as tf
import glob
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import shutil
    
# TODO: Automate the running_network scripts
# TODO: Write a script that was used to create both synthetic and real datasets

CURRENT_YEAR = datetime.now().year
LOG_FILE = "/open5gs/install/var/log/open5gs/amf.log"
MODEL = tf.keras.models.load_model("/app/data/Model/Model_bn.keras", compile=False)
MODEL.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
SCALER = joblib.load("/app/data/Model/scaler.joblib")
with open("/app/data/Model/selected_features.json", "r") as f:
    SELECTED_FEATURES = json.load(f)
SELECTED_FEATURES = SELECTED_FEATURES['features']
SEQUENCE_LENGTH = 60
DATA_PATH = "/app/data/running_data.csv"


# 📐 Prometheus
ue_reg_time_last = Gauge("ue_registration_duration_seconds_last", "Last registration duration")
ue_reg_time_avg = Gauge("ue_registration_duration_seconds_avg", "Average registration duration")
ue_reg_time_min = Gauge("ue_registration_duration_seconds_min", "Min registration duration")
ue_reg_time_max = Gauge("ue_registration_duration_seconds_max", "Max registration duration")

ue_sess_time_last = Gauge("ue_session_duration_seconds_last", "Last session duration")
ue_sess_time_avg = Gauge("ue_session_duration_seconds_avg", "Average session duration")
ue_sess_time_min = Gauge("ue_session_duration_seconds_min", "Min session duration")
ue_sess_time_max = Gauge("ue_session_duration_seconds_max", "Max session duration")

predicted_uc_metric = Gauge("classified_uc_class", "Classified current use case (UC) by LSTM model")
true_uc_metric = Gauge("true_uc_class", "True current use case (UC) from data")
model_loss = Gauge("model_loss", "Model loss during fine-tuning")
predicted_uc_confidence = Gauge("classified_uc_confidence", "Confidence score of predicted use case")

# Parametre
notebook_path = "./data/main.ipynb"                 # Cesta k .ipynb
log_path = "./data/log_execution.log"               # Súbor pre logovanie
csv_file = "./data/running_data.csv"                # Hlavný výstupný súbor
backup_dir = "./data/backup"                        # Priečinok na uloženie záloh
backup_interval = 600                               # Zálohovať každých 600 sekúnd (10 minút)
loop_counter = 0                                    # Počítadlo pre cyklus

# Zabezpečiť priečinok pre zálohy
os.makedirs(backup_dir, exist_ok=True)

def truncate_running_data(csv_path, keep_last_n=60):
    try:
        df = pd.read_csv(csv_path)
        if len(df) > keep_last_n:
            df = df.tail(keep_last_n)
            df.to_csv(csv_path, index=False)
            print(f"🧹 Truncated {csv_path} to last {keep_last_n} records.")
    except Exception as e:
        print(f"⚠️ Could not truncate {csv_path}: {e}")


def run_main_notebook_with_backup():
    global loop_counter
    print("📓 Spúšťam main.ipynb...")

    try:
        # 1. Spustenie notebooku
        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
        ep.preprocess(notebook)

        # 2. Log
        with open(log_path, "a") as log:
            log.write(f"{datetime.now()}: ✅ Notebook bol úspešne spustený\n")

        # 2.1 Vymazanie starých riadkov v CSV
        truncate_running_data(csv_file, keep_last_n=60)

        # 3. Záloha CSV každých backup_interval sekúnd
        if os.path.exists(csv_file) and loop_counter % backup_interval == 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"backup_{timestamp}.csv")
            shutil.copy(csv_file, backup_file)
            with open(log_path, "a") as log:
                log.write(f"{datetime.now()}: 🔒 Záloha vytvorená: {backup_file}\n")

    except Exception as e:
        error_message = f"{datetime.now()}: ❌ Chyba pri spúšťaní notebooku: {e}"
        print(error_message)
        with open(log_path, "a") as log:
            log.write(error_message + "\n")
        time.sleep(3)

    loop_counter += 1

def predict_current_uc(latest_window_df):
    if len(latest_window_df) < SEQUENCE_LENGTH:
        return -1, -1.0  # Nedostatok dát

    # Vyber len posledných SEQUENCE_LENGTH riadkov
    window = latest_window_df[SELECTED_FEATURES].tail(SEQUENCE_LENGTH)
    window_scaled = SCALER.transform(window)
    window_scaled = np.expand_dims(window_scaled, axis=0)

    prediction = MODEL.predict(window_scaled, verbose=0)
    predicted_uc = np.argmax(prediction)
    confidence = float(prediction[0][predicted_uc])
    return predicted_uc, confidence

def load_last_sequence(csv_path, selected_features, sequence_length=60):
    try:
        df = pd.read_csv(csv_path)
        df = df.tail(sequence_length)

        # Kontrola, či sú všetky vybrané metriky prítomné
        missing = [f for f in selected_features if f not in df.columns]
        if missing:
            raise ValueError(f"Missing features in input: {missing}")
        
        # Načítame korektné výstupy pre fine-tuning
        if "current_uc" not in df.columns:
            raise ValueError("Missing 'current_uc' column in input data.")
        else:
            correct_labels = df["current_uc"].copy()

        # Výber, preformátovanie a doplnenie chýbajúcich hodnôt
        df = df[selected_features].copy()
        df = df.ffill().fillna(0)

        return df, correct_labels
    except Exception as e:
        print(f"❌ Failed to load sequence: {e}")
        return None

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

        # 🙏 Initial Registration
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

        # ✅ Registration complete
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

            # ⏱️ Čas trvania registrácie
            if ue["reg_start"] and ue["reg_end"] and not ue["reg_duration"]:
                ue["reg_duration"] = (ue["reg_end"] - ue["reg_start"]).total_seconds()
                new_reg_durations.append(ue["reg_duration"])

            ue_details[imsi] = ue
            current_reg = {}

        # Posledné SUCI
        if match := re.search(r'SUCI\[(suci-[^\]]+)\]', line):
            last_seen_suci = match.group(1)

        # Posledné IMSI
        if match := re.search(r'imsi-(\d+)', line):
            current_imsi = match.group(1)

        # 👋🏻 Deregistrácia
        if "UE Context Release" in line or "Implicit De-registered" in line or "De-register UE" in line:
            dereg_block.append(line)

        if dereg_block and "SUCI" in line:
            imsi_match = re.search(r'imsi-(\d+)', line)
            suci_match = re.search(r'SUCI\[(suci-[^\]]+)\]', line)
            dereg_time = timestamp

            imsi = imsi_match.group(1) if imsi_match else current_imsi
            suci = suci_match.group(1) if suci_match else last_seen_suci

            # 🔂 SUCI konverzia na IMSI
            if suci and len(suci) == 33:
                sufix = suci[-10:]
                tac = suci[7:10]
                nci = suci[11:13]
                imsi = f"{tac}{nci}{sufix}"

            # Najskôr hľadáme IMSI
            if imsi and imsi in ue_details:
                ue = ue_details[imsi]
            # Ak nie je nájdený IMSI, hľadáme SUCI
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
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{path_prefix}{today}.keras"
    model.save(filename)
    print(f"💾 Model uložený ako {filename}")

    # Vyčistí staré modely
    clean_old_models()

def clean_old_models(directory="/app/data/Model", keep_last_n=7, pattern="Model_bn_*.keras"):
    files = sorted(glob.glob(os.path.join(directory, pattern)), key=os.path.getmtime, reverse=True)
    if len(files) > keep_last_n:
        for file in files[keep_last_n:]:
            try:
                os.remove(file)
                print(f"🗑️ Odstránený starý model: {file}")
            except Exception as e:
                print(f"⚠️ Nepodarilo sa odstrániť {file}: {e}")

def main_loop(interval=1, prometheus_port=9000):
    print(f"📡 Tracking UEs every {interval}s and exporting to Prometheus on port {prometheus_port}...\n")
    start_http_server(prometheus_port)

    previous_state = {
        "ue_details": {},
        "reg_durations": [],
        "session_durations": [],
        "connected_ue_history": [],
        "max_connected_ue_count": 0
    }

    schedule.every(1).seconds.do(run_main_notebook_with_backup)

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

            # 📨 Export na Prometheus
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

            current_df, correct_labels = load_last_sequence(DATA_PATH, SELECTED_FEATURES, SEQUENCE_LENGTH)
            if current_df is not None:
                predicted_uc, confidence = predict_current_uc(current_df)
                predicted_uc_metric.set(predicted_uc)
                predicted_uc_confidence.set(confidence)
                X_finetune = SCALER.transform(current_df[SELECTED_FEATURES])
                X_finetune = np.expand_dims(X_finetune, axis=0)

                y_finetune = np.array([correct_labels.iloc[-1]])
                y_finetune_cat = tf.keras.utils.to_categorical([y_finetune], num_classes=MODEL.output_shape[-1])

                # Fine-tuning modelu
                history = MODEL.fit(X_finetune, y_finetune_cat, epochs=3, verbose=0)
                model_loss.set(float(history.history['loss'][-1]))
                print(f"✅ Fine-tuned on UC {y_finetune}")

                # predikcia po fine-tuningu
                prediction = MODEL.predict(X_finetune, verbose=0)
                predicted_uc = np.argmax(prediction)
                confidence = float(prediction[0][predicted_uc])
                predicted_uc_metric.set(predicted_uc)
                predicted_uc_confidence.set(confidence)
                true_uc_metric.set(correct_labels.iloc[-1])
                print(f"🔮 Predicted UC after fine-tuning: {predicted_uc}")

            else:
                print("❌ Failed to load current sequence for prediction.")
                predicted_uc_metric.set(-1)
                predicted_uc_confidence.set(0.0)
                true_uc_metric.set(correct_labels.iloc[-1])

            # 🖥️  Výstup do terminálu
            print("\033[H\033[J", end="") # Vyčistí terminál
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"🕒 Timestamp:       {timestamp}")
            print(f"📓 Notebook:        main.ipynb spustený ✅")
            print(f"🧹 CSV Truncate:    {csv_file} → posledných 60 riadkov\n")

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
