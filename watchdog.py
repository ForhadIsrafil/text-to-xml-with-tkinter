import time
from tkinter import filedialog
import pathlib
import sys

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler


# folder monitor that only copy’s new files in a folder
#

def on_created(event):
    if event.event_type=="created":
        print(f"hey, {event.event_type} {event.key} {event.src_path} has been created!")


def on_modified(event):
    print(f"hey buddy, {event.event_type} {event.key} {event.src_path} has been modified")

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = True  # False if check subdirectories files
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_modified = on_modified

    path = "C:/Users/forha/Downloads"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()

