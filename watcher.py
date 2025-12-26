import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from main_logic import run_intelligence_crew

class DataFileHandler(FileSystemEventHandler):
    """Handles new file events and triggers the structured AI response."""

    def on_created(self, event):
        # Ignore folder creations
        if event.is_directory: 
            return
        
        file_name = os.path.basename(event.src_path)
        
        # Only process supported file types
        if file_name.endswith(('.pdf', '.xlsx', '.csv', '.txt')):
            print(f"\n🚀 [EVENT] New file detected: {file_name}")
            print(f"🤖 Triggering AI Crew for background analysis...")
            
            # 1. Define the background summary query
            query = f"Analyze the new file {file_name} and provide a concise summary of its contents."
            
            try:
                # 2. Run the AI (Now returns a dictionary)
                result_data = run_intelligence_crew(query)
                
                # 3. Create the log entry with all 'Add-ons'
                log_entry = {
                    "event_type": "NEW_FILE",
                    "file_name": file_name,
                    "answer": result_data["answer"],
                    "time_taken": result_data["time_taken"],
                    "accuracy": result_data["accuracy"],
                    "sources": result_data["sources"],
                    "timestamp": time.time()  # To help Streamlit identify the latest update
                }
                
                # 4. Write to background_results.json (The Bridge)
                # We read existing data first to append to the list
                history = []
                if os.path.exists("background_results.json"):
                    with open("background_results.json", "r") as f:
                        try:
                            history = json.load(f)
                        except json.JSONDecodeError:
                            history = []

                history.append(log_entry)
                
                with open("background_results.json", "w") as f:
                    json.dump(history, f, indent=4)
                
                print(f"✅ [SUCCESS] Background analysis saved for {file_name}")
                print(f"⏱️ Time: {result_data['time_taken']}s | 🎯 Accuracy: {result_data['accuracy']}%")

            except Exception as e:
                print(f"❌ [ERROR] Watcher failed to process {file_name}: {str(e)}")

if __name__ == "__main__":
    # Ensure the directory exists
    WATCH_DIRECTORY = "./data_files"
    if not os.path.exists(WATCH_DIRECTORY):
        os.makedirs(WATCH_DIRECTORY)

    event_handler = DataFileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)
    
    print(f"🛡️  IntelSentry Watchdog is Active")
    print(f"📂 Monitoring: {os.path.abspath(WATCH_DIRECTORY)}")
    print("🚦 Waiting for files... (Ctrl+C to stop)")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Watchdog stopped.")
    observer.join()