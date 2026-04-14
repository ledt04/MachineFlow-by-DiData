import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.watchdog.qubit_watcher import watch_qubit, stop_watch_qubit, Handler as QubitHandler
from src.watchdog.fragmentanalyzer_watcher import watch_fragmentanalyzer, stop_watch_fragmentanalyzer, Handler as FragmentHandler
from src.utils.logger import login, logout
from src.mashines.qubit.main import main as qubit_main

def main():
    # watchdog in qubit input folder
    # watchdog in fragmentanalyzer input folder
    qubit_handler = QubitHandler()
    fragment_handler = FragmentHandler()
    
    qubit_observer = watch_qubit(qubit_handler)
    fragment_observer = watch_fragmentanalyzer(fragment_handler)
    
    # Debug
    # session = login()
    # qubit_main(session)
    # logout(session)
    
    try:
        while True:
            if qubit_handler.file_created:
                qubit_handler.file_created = False
                session = login()
                qubit_main(session)
                logout(session)

            if fragment_handler.file_created:
                fragment_handler.file_created = False
                session = login()
                # process_fragmentanalyzer(session)
                logout(session)
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        stop_watch_qubit(qubit_observer)
        stop_watch_fragmentanalyzer(fragment_observer)

if __name__ == "__main__":
    main()