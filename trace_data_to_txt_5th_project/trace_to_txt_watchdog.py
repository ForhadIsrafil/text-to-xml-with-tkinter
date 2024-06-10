from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from tkinter import filedialog
import pathlib
import sys
import shutil
import pandas as pd
from datetime import datetime

pd.options.mode.chained_assignment = None


# global destination_folder


def generate_txt(trace_file_path, file_name):
    try:
        df = pd.read_csv(pathlib.Path(trace_file_path), sep='|', header=None, dtype=str)

        df.columns = [f'@{i}' for i in range(1, 9)]

        # panel-id
        panel_id = df['@4'].iloc[0]
        sub_panel_id = panel_id.replace('PV', 'SV')
        # drop first two columns
        df.drop(['@1', '@2'], axis=1, inplace=True)

        # separate column @3
        df[['date', 'time']] = df['@3'].str.split(' ', expand=True)

        # drop column @3
        df.drop(['@3'], axis=1, inplace=True)

        # correct of date
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

        # correct of time
        df['time'] = pd.to_datetime(df['time'], format='%H%M%S').dt.time

        # static value skvr
        df['skvr'] = "SKVR"
        df['panel-id'] = panel_id

        # generate sub-panel-id
        df['sub_panel_id'] = sub_panel_id

        # Rearrange the columns
        df2 = df[
            ["date", "time", "skvr", "panel-id", "sub_panel_id", "@4", "@5", "@6", "@7", "@8"]]  # "@4" is circuit-id

        # range the dataframe 1 to 40 number row
        main_df = df2.iloc[1:41]

        # update sub-panel-id
        sub_panels = [[sub_panel_id + "-" + str(i) for g in range(10)] for i in [2, 4, 1, 3]]
        sub_panel_list = str(sub_panels).replace('[', '').replace(']', '').replace("'", "")
        # print(len(sub_panel_list.split(',')))
        main_df['sub_panel_id'] = sub_panel_list.split(',')
        main_df['sub_panel_id'] = main_df['sub_panel_id'].str.strip()

        main_df.to_csv(f"C:\FLX_TXT_NedFlex\\{file_name.split('.')[0]}.txt", sep="|", header=None, index=False)

        # ------------------------------------------------------------------------------
        # Remove 4 lines start with SVTL and save trace file into C:\FLX_Xlink_Input
        with open(pathlib.Path(trace_file_path), 'r') as trace_file:
            trace_data = trace_file.readlines()

        with open(f"C:\FLX_Xlink_Input\\{file_name.split('.')[0]}.trace", 'w') as new_trace_file:
            all_lines = "".join(line for line in trace_data if "SVTL" not in line)
            # print(all_lines)
            new_trace_file.write(all_lines.strip())
            new_trace_file.close()

        # move the original input file to C:\FLX_Trace_Asys.
        shutil.move(trace_file_path, "C:\FLX_Trace_Asys")

    except Exception as e:
        print(e)


def on_created(event):
    if event.event_type == 'created' and event.is_directory != True:
        # print(event.key)
        print("File created:", event.src_path)
        file_name = event.src_path.split('\\')[-1]
        if file_name.startswith("PVTL") or file_name.startswith("P-VTL"):
            generate_txt(event.src_path, file_name)
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

In case the file starts with PVTL or P-VTL we need to generate an additional file 
what is a copy of the input .trace file but then only remove the SVTL Lines.
That file needs to be saved also to C:\FLX_Xlink_Input

only remove that 4 lines, SVTL Lines?
yes.

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

# pyinstaller --onefile --add-data "icon.png;." --icon="icon.png" trace_to_txt_watchdog.py
