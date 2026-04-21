from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from src.config.settings import get_local_directory, get_qubit_id

class Handler(FileSystemEventHandler):
    def __init__(self):
        self.file_created = False
        self.file_modified = False
        self.latest_file_path = None
    
    def on_created(self, event):
        print(f"File created: {Path(event.src_path).name}")
        if not event.is_directory:
            self.file_created = True
            self.latest_file_path = event.src_path

    def on_modified(self, event):
        print(f"File modified: {Path(event.src_path).name}")
        if not event.is_directory:
            self.file_modified = True
            self.latest_file_path = event.src_path

    def on_deleted(self, event):
        print(f"File deleted: {Path(event.src_path).name}")

    def on_moved(self, event):
        print(f"File moved: {Path(event.src_path).name} -> {Path(event.dest_path).name}")

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
