import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.watchdog.qubit_watcher import watch_directory

def main():
    # in interval 60s watchdog service
    # watchdog in qubit input folder
    # watchdog in fragmentanalyzer input folder

    watch_directory()
    
    # if data found
    # login
    # depends where data start which func
    # qubit or fragmentanalyzer

    # when done: logout
    
    pass

if __name__ == "__main__":
    main()