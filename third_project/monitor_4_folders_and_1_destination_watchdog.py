from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from tkinter import filedialog
import pathlib
import sys
import shutil

# folder monitor that only copy’s new files in a folder
"""
NOTE:
- Make sure that the file is not in a read-only directory.
- If the file is in a read-only directory, you can try copying the file to a different directory where you have permission to write.
- If you are running the Python program as a non-administrative user, you can try running the program as an administrator. To do this, right-click on the Python script and select "Run as administrator".
"""

global destination_folder


def on_created(event):
    if event.event_type == 'created' and event.is_directory != True:
        # print(event.key)
        print("File created:", event.src_path)
        try:
            shutil.copy(event.src_path, destination_folder)
        except Exception as e:
            print(e)


def get_source_folder():
    folder = filedialog.askdirectory(mustexist=True, title="Select Source Folder")
    if not folder:
        sys.exit("NO FOLDER SELECTED")
    return pathlib.Path(folder)


def get_destination_folder():
    folder = filedialog.askdirectory(mustexist=True, title="Select Destination Folder")
    if not folder:
        sys.exit("NO DESTINATION FOLDER SELECTED")
    return pathlib.Path(folder)


if __name__ == "__main__":
    source_folder_paths = []
    for folder_number in range(1, 5):
        print(f"Select Your {folder_number} Number Source Folder...")
        source_folder = get_source_folder()
        source_folder_paths.append(source_folder)
        print(f"{folder_number} Number Source Folder >>>", source_folder, '\n')

    print("Select Your Destination Folder...")
    destination_folder = get_destination_folder()
    print("Destination Folder >>>", destination_folder, '\n')

    files_event_handler = FileSystemEventHandler()
    files_event_handler.on_created = on_created
    # files_event_handler.on_modified = on_modified

    observer_list = []
    observer = Observer()
    for source_folder_path in source_folder_paths:
        observer.schedule(files_event_handler, path=source_folder_path)
        observer_list.append(observer)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for single_observer in observer_list:
            # Stop observer if interrupted
            single_observer.stop()

            # Wait until the thread terminates before exit
            single_observer.join()
