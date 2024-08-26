from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
# from tkinter import filedialog
import pathlib
import sys, os
import shutil


# import pandas as pd
# from datetime import datetime


def on_created(event):
    if event.event_type == 'created' and event.is_directory != True:
        print("File created:", event.src_path)
        destination_folder = r"\\10.42.230.101\NedFlex_FactoryLogix$\FLX-OUT"

        try:
            shutil.copy(pathlib.Path(event.src_path), pathlib.Path(destination_folder))

            time.sleep(0.1)
            if pathlib.Path(event.src_path).exists():
                pathlib.Path(event.src_path).unlink()
                # os.unlink(event.src_path)
                print(event.src_path, "has been deleted.")

        except Exception as e:
            print(e)


if __name__ == "__main__":
    print("Tracking Source Folder...")
    print(r"C:\FLX_TXT_NedFlex")
    source_folder = pathlib.Path(r"C:\FLX_TXT_NedFlex")
    # os.chmod(source_folder, 0o666)

    files_event_handler = FileSystemEventHandler()
    files_event_handler.on_created = on_created
    # files_event_handler.on_modified = on_modified

    observer = Observer()
    observer.schedule(event_handler=files_event_handler, path=source_folder)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
r"""
can you make a watchdog that copy files
source static: C:\FLX_TXT_NedFlex


destination static:  \\10.42.230.101\NedFlex_FactoryLogix$\FLX-IN


pyinstaller --onefile --add-data "icon.png;." --icon="icon.png" copy_files_watchdog.py
"""
