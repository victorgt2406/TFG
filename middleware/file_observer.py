import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f'File {event.src_path} has been created!')
    
    def on_modified(self, event):
        print(f'File {event.src_path} has been modified!')

def start_observer(path='../data'):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()