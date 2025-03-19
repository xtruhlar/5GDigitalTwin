from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        """Triggered when a file is modified."""
        if event.is_directory or not event.src_path.endswith(".log"):
            return
        
        print(f"📝 Log file modified: {event.src_path}")  # Debugging: File modified

        try:
            # Read only the last few lines of the log file
            with open(event.src_path, "r") as f:
                lines = f.readlines()[-5:]  # Last 5 lines for debugging
                if lines:
                    print(f"📢 New log entries detected in {event.src_path}:")
                else:
                    print(f"⚠️ No new log entries in {event.src_path}!")
                
                for line in lines:
                    print(f"📌 Log line: {line.strip()}")  # Debugging: Show new logs
        except Exception as e:
            print(f"❌ Error reading log file {event.src_path}: {e}")  # Debugging: Read error

# Set up observer
log_dir = "../log/"  # Make sure this matches the actual path

if not os.path.exists(log_dir):
    print(f"❌ ERROR: Log directory '{log_dir}' does not exist!")
    exit(1)

print(f"🚀 Watching log directory: {log_dir}")

observer = Observer()
event_handler = LogFileHandler()
observer.schedule(event_handler, path=log_dir, recursive=False)
observer.start()

print("✅ Log monitoring started. Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)  # Keep script running
except KeyboardInterrupt:
    print("\n🛑 Stopping real-time monitoring...")
    observer.stop()
observer.join()
print("✅ Observer stopped successfully.")
