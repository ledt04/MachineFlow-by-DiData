import sys
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.logger import login, logout
from src.mashines.qubit.main import main as qubit_main
from src.mashines.fragmentanalyzer.main import main as fragment_main
from src.config.settings import get_local_directory, get_qubit_id, get_fragmentanalyzer_id


class MaschineHandler(FileSystemEventHandler):
    def __init__(self, machine_type):
        self.machine_type = machine_type

    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        print(f"{self.machine_type} file detected: {file_path.name}")
        
        session = login()
        try:
            if self.machine_type == "qubit":
                qubit_main(session)
                print("Qubit processing completed.")
            elif self.machine_type == "fragmentanalyzer":
                fragment_main(session)
                print("Fragment Analyzer processing completed.")
        finally:
            logout(session)
            
def main():
    observer = Observer()
    
    qubit_path = get_local_directory(get_qubit_id())
    fragment_path = get_local_directory(get_fragmentanalyzer_id())
    
    observer.schedule(MaschineHandler("qubit"), qubit_path)
    observer.schedule(MaschineHandler("fragmentanalyzer"), fragment_path)
    
    observer.start()
    print("Watching for files...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
if __name__ == "__main__":
    main()