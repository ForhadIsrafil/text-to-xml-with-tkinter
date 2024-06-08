from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from tkinter import filedialog
import pathlib
import sys
import shutil

global destination_folder


def generate_txt():
    pass


def on_created(event):
    if event.event_type == 'created' and event.is_directory != True:
        # print(event.key)
        print("File created:", event.src_path)
        file_name = event.src_path.split('\\')[-1]
        if file_name.startswith("PVTL") or file_name.startswith("P-VTL"):
            generate_txt()
        else:
            print(f"File {file_name} moved to C:\FLX_Xlink_Input")
            shutil.move(src=event.src_path, dst="C:\FLX_Xlink_Input")

        # try:
        #     shutil.copy(event.src_path, destination_folder)
        # except Exception as e:
        #     print(e)


def get_source_folder():
    folder = filedialog.askdirectory(mustexist=True, title="Select Source Folder")
    print("Source Folder Path:", folder, '\n')
    if not folder:
        sys.exit("NO FOLDER SELECTED")
    return pathlib.Path(folder)


# def get_destination_folder():
#     folder = filedialog.askdirectory(mustexist=True, title="Select Destination Folder")
#     print("Destination Folder >>>", folder, '\n')
#     if not folder:
#         sys.exit("NO DESTINATION FOLDER SELECTED")
#     return pathlib.Path(folder)


if __name__ == "__main__":

    print("Select Source Folder...")
    source_folder = get_source_folder()
    #
    # print("Select Your Destination Folder...")
    # destination_folder = get_destination_folder()

    files_event_handler = FileSystemEventHandler()
    files_event_handler.on_created = on_created
    # files_event_handler.on_modified = on_modified

    observer = Observer()
    observer.schedule(files_event_handler, path=source_folder)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

"""
NOTE:
This script needs to monitor a folder
Whenever a new file appears it need to check the name of the file

When its starts with PVTL or P-VTL it needs to convert it and save output of the file in C:\FLX_TXT_NedFlex 
and move the original input file to C:\FLX_Trace_Asys.
When the filename start with a different value as PVTL or P-VTL it just needs to move the file to C:\FLX_Xlink_Input

Will the folder paths always be same as you mentioned above?
ans: yes.

---------------------------------------------------------------------------------------------------------------
one question, will the output file is a text file or a csv/excel file?
ans: Text

It will convert all files in a folders and will move the original file after processing to C:\FLX_Trace_Processed
and the converted file in C:\FLX_TXT_Generated.


Needs to remove 4 lines and export is as .trace file again
The lines with svtl
Always 4 files


the will be no data like @1 @2
"""

# pyinstaller --onefile --add-data "icon.png;." --icon="icon.png" monitor_4_folders_and_1_destination_watchdog.py
