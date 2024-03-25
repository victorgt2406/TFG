import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.fo_json import update_jsonfile
from utils.fo_pdf import update_pdffile
from utils.fo_text import update_textfile

class MyHandler(FileSystemEventHandler):

    def handle_new_change(self, src_path:str):
        if src_path.endswith(".json"):
            update_jsonfile(src_path)
        elif src_path.endswith(".txt"):
            update_textfile(src_path)
        elif src_path.endswith(".pdf"):
            update_pdffile(src_path)
        elif src_path.endswith(".csv"):
            pass
            

    def on_created(self, event):
        print(f'{event.src_path} has been created!')
        if not event.is_directory:
            self.handle_new_change(event.src_path)

    
    def on_modified(self, event):
        print(f'{event.src_path} has been modified!')
        if not event.is_directory:
            self.handle_new_change(event.src_path)

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