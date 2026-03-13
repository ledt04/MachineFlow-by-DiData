import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.watchdog.qubit_watcher import watch_qubit

def main():
    # watchdog in qubit input folder
    # watchdog in fragmentanalyzer input folder

    watch_qubit()
    #watch_fragmentanalyzer()
    
    # if data found
    # login
    # depends where data start which func
    # qubit or fragmentanalyzer

    # when done: logout

if __name__ == "__main__":
    main()