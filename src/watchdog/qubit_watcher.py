import os
import time
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from src.config.settings import get_local_directory, get_qubit_id

class Handler(FileSystemEventHandler):
    def __init__(self):
        self.file_created = False
        self.file_modified = False
    
    def on_created(self, event):
        print(f"File created: {event.src_path}")
        if not event.is_directory:
            self.file_created = True

    def on_modified(self, event):
        print(f"File modified: {event.src_path}")
        if not event.is_directory:
            self.file_modified = True

    def on_deleted(self, event):
        print(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        print(f"File moved: {event.src_path} -> {event.dest_path}")

def watch_qubit(handler: Handler):
    observer = Observer()

    directory = Path(get_local_directory(get_qubit_id()))
    
    if not directory.exists():
        raise ValueError(f"Invalid directory configured: {directory}")

    observer.schedule(handler, path=directory)
    observer.start()
    return observer

def stop_watch_qubit(observer: Observer):
    observer.stop()
    observer.join()
