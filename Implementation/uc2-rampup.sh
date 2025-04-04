#!/bin/bash

# === DEFAULTS ===
CSV_PATH="./digital_shadow/data/uc2_rampup.csv"
NUM_UES=10
INTERVAL_SECONDS=10

# === PARSE FLAGS ===
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --ues)
      NUM_UES="$2"
      shift 2
      ;;
    --interval)
      INTERVAL_SECONDS="$2"
      shift 2
      ;;
    *)
      echo "❌ Unknown argument: $1"
      echo "Usage: $0 [--count N] [--interval S]"
      exit 1
      ;;
  esac
done

echo "📁 Creating UC2 CSV: Gradual UE Ramp-up..."
python3 - <<EOF
import pandas as pd
from datetime import datetime, timedelta

num_ues = $NUM_UES
interval = $INTERVAL_SECONDS
start_time = datetime.now()

rows = [{"timestamp": (start_time + timedelta(seconds=i * interval)).strftime('%Y-%m-%d %H:%M:%S'), "Active UEs": i} for i in range(num_ues + 1)]

df = pd.DataFrame(rows)
df.to_csv("$CSV_PATH", index=False)
print("✅ CSV saved to $CSV_PATH")
EOF

echo "🚀 Starting UE mirror based on CSV..."
python3 ./digital_shadow/ues_mirror.py --file "$CSV_PATH"

echo "🏁 UC2 completed. All UEs should now be active."
