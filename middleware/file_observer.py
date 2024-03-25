import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.fo_json import update_jsonfile

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f'{event.src_path} has been created!')
        if not event.is_directory:
            print(f'{event.src_path} is a file')
            if event.src_path.endswith(".json"):
                update_jsonfile(event.src_path)

    
    def on_modified(self, event):
        print(f'{event.src_path} has been modified!')
        if not event.is_directory:
            print(f'{event.src_path} is a file')
            if event.src_path.endswith(".json"):
                update_jsonfile(event.src_path)

def file_observer(path='../data'):
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