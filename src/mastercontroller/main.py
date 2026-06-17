import sys
import os
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.logger import login, logout
from src.mashines.qubit.main import main as qubit_main
from src.mashines.fragmentanalyzer.main import main as fragment_main
from src.config.settings import (
    get_local_directory, 
    get_backup_directory, 
    get_qubit_id, 
    get_fragmentanalyzer_id
)

class MaschineHandler(FileSystemEventHandler):
    def __init__(self, machine_type, machine_id):
        self.machine_type = machine_type
        self.machine_id = machine_id

    def on_created(self, event):
        # Wir reagieren nur auf echte .csv Dateien
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # SONDERFALL: Wenn das Event feuert, die Datei aber bereits 
        # durch einen vorherigen parallelen Prozess verschoben wurde
        if not file_path.exists():
            return

        if not file_path.suffix.lower() == '.csv':
            return

        # Fragment Analyzer Spezifikum beachten
        if self.machine_type == "fragmentanalyzer" and "peak table" not in file_path.name.lower():
            return

        print(f"\n[{self.machine_type.upper()}] New CSV detected: {file_path.name}")
        
        # Dem Gerät Zeit geben, den Schreibvorgang komplett zu beenden
        time.sleep(2) 
        
        # Doppelte Absicherung nach dem Sleep
        if not file_path.exists():
            print(f"[{self.machine_type.upper()}] File was already processed and moved by another event loop.")
            return

        # Hauptverzeichnis holen (z.B. E:\QubitFlex)
        root_dir = Path(get_local_directory(self.machine_id))
        
        # Falls die Datei in einem Unterordner liegt (wie beim Qubit Flex)
        is_in_subfolder = file_path.parent != root_dir
        temp_root_path = root_dir / file_path.name

        if is_in_subfolder:
            # Kopiere die Datei kurz in den Hauptordner, damit dein Original-Skript sie sofort sieht!
            shutil.copy(str(file_path), str(temp_root_path))
            print(f"[{self.machine_type.upper()}] Prepared file in root directory for processing.")

        # Deine originalen Skripte unverändert ausführen (mit nur 1 Argument)
        session = login()
        try:
            if self.machine_type == "qubit":
                qubit_main(session)
            elif self.machine_type == "fragmentanalyzer":
                fragment_main(session)
            
            # --- BACKUP LOGIK ---
            backup_dir_str = get_backup_directory(self.machine_id)
            if backup_dir_str:
                backup_dir = Path(backup_dir_str)
                backup_dir.mkdir(parents=True, exist_ok=True)
                
                target_path = backup_dir / file_path.name
                if target_path.exists():
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    target_path = backup_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
                
                # Verschiebe die originale Datei ins Backup
                if file_path.exists():
                    shutil.move(str(file_path), str(target_path))
                    print(f"Moved original file to backup: {target_path.name}")

                # Unterordner aufräumen, falls er jetzt leer ist
                parent_dir = file_path.parent
                if is_in_subfolder and parent_dir.exists():
                    if not any(parent_dir.iterdir()):
                        parent_dir.rmdir()
                        print(f"Cleaned up empty folder: {parent_dir.name}")

        except Exception as e:
            print(f"Error during processing: {e}")
        finally:
            # Die temporäre Datei im Hauptordner immer löschen, damit alles sauber bleibt
            if temp_root_path.exists():
                os.remove(temp_root_path)
            logout(session)

            
def main():
    observer = Observer()
    
    qubit_id = get_qubit_id()
    fragment_id = get_fragmentanalyzer_id()
    
    qubit_path = get_local_directory(qubit_id)
    fragment_path = get_local_directory(fragment_id)
    
    Path(qubit_path).mkdir(parents=True, exist_ok=True)
    Path(fragment_path).mkdir(parents=True, exist_ok=True)
    
    # Überwacht rekursiv alle Unterordner
    observer.schedule(MaschineHandler("qubit", qubit_id), qubit_path, recursive=True)
    observer.schedule(MaschineHandler("fragmentanalyzer", fragment_id), fragment_path, recursive=True)
    
    observer.start()
    print(f"Watching for Qubit files/folders in: {qubit_path}")
    print(f"Watching for Fragment Analyzer files in: {fragment_path}")
    print("System active and monitoring...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
if __name__ == "__main__":
    main()