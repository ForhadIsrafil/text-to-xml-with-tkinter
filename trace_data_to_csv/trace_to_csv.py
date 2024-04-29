import time
from tkinter import filedialog
import pathlib
import pandas as pd
import shutil
from glob import glob
import flet as ft
from flet import Text, Column, Row, Container, View, AppBar
from flet import RouteChangeEvent, ViewPopEvent, MainAxisAlignment, CrossAxisAlignment
import os

file_path_text_box = ft.TextField("Select Trace Folder Path(*.trace)", read_only=True, width=580)
trace_destination_folder_text_box = ft.TextField("Trace Destination Folder Path", read_only=True, width=580)
csv_destination_folder_text_box = ft.TextField("CSV Destination Folder Path", read_only=True, width=580)

status = Text("")

pr = ft.ProgressBar(width=500, border_radius=5, scale=5)
pr.color = "#FF5733"
pr.bgcolor = "#96DED1"


def generate_csv():
    if len(glob(file_path_text_box.value + "\*.trace")) == 0:
        status.value = "No trace files found/directoy not selected."
        status.color = "#FF5733"
        status.size = 20
        status.update()
        time.sleep(3.5)

        status.value = ''
        status.color = None
        status.update()

    for file_path in glob(file_path_text_box.value + "\*.trace"):
        # update status and progress view
        status.value = ''
        status.update()
        pr.value = None
        pr.update()

        print('file:', file_path)
        file_name = os.path.basename(file_path).split('.')[0]
        # trace_folder_path = pathlib.Path(file_path_text_box.value)
        # destination_folder_path = pathlib.Path(destination_folder_text_box.value)
        # print(destination_folder_path)
        # print(trace_folder_path)
        try:
            df = pd.read_csv(file_path, sep='|', )
            df.columns = columns = ["@1|DateStamp (YYYY-MM-DD)", "@2|TimeStamp (hh:mm:ss) (24h system)",
                                    "@3|MP (NLUD/SKVR/DRO/USPB)",
                                    "@4|FLXPANELID", "@5|FLXSUBPANELID", "@6|FLXUID", "@7|Result"]
            df.to_csv(f"{csv_destination_folder_text_box.value}\\{file_name}.csv", index=False)
            shutil.move(file_path, trace_destination_folder_text_box.value)

            pr.value = 100
            pr.update()

            status.value = file_name
            status.update()
            time.sleep(1)

        except Exception as e:
            status.value = str(e)
            status.update()


def on_dialog_result(e: ft.FilePickerResultEvent):
    print("Selected folder:", e.path)
    # print("Selected files:", e.files)
    # print("Selected file or directory:", e.files[0])

    if file_path_text_box.data == "trace_folder":
        file_path_text_box.value = e.path
        file_path_text_box.data = None
        file_path_text_box.update()

    if trace_destination_folder_text_box.data == "trace_destination_folder":
        trace_destination_folder_text_box.value = e.path
        trace_destination_folder_text_box.data = None
        trace_destination_folder_text_box.update()

    if csv_destination_folder_text_box.data == "csv_destination_folder":
        csv_destination_folder_text_box.value = e.path
        csv_destination_folder_text_box.data = None
        csv_destination_folder_text_box.update()


def home(page: ft.Page):
    page.window_width = 810
    page.window_height = 450
    page.window_resizable = False
    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()

    def which_folder(folder_name):
        print("which_folder", folder_name)

        if folder_name == "trace_folder":
            file_path_text_box.data = folder_name
            file_path_text_box.update()
            file_picker.get_directory_path(dialog_title="Select Trace Folder (*.trace)")

        if folder_name == "trace_destination_folder":
            trace_destination_folder_text_box.data = folder_name
            trace_destination_folder_text_box.update()
            file_picker.get_directory_path(dialog_title="Select Trace Destination Folder")

        if folder_name == "csv_destination_folder":
            csv_destination_folder_text_box.data = folder_name
            csv_destination_folder_text_box.update()
            file_picker.get_directory_path(dialog_title="Select CSV Destination Folder")

    choose_trace_folder = ft.ElevatedButton("Choose Trace Folder", on_click=lambda _: which_folder("trace_folder"), )

    trace_destination_folder = ft.ElevatedButton("Trace Destination Folder",
                                                 on_click=lambda _: which_folder("trace_destination_folder"))
    csv_destination_folder = ft.ElevatedButton("CSV Destination Folder",
                                               on_click=lambda _: which_folder("csv_destination_folder"))

    page.add(
        Row(
            controls=[
                file_path_text_box,
                choose_trace_folder,

            ],
            # spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        Row(
            controls=[
                trace_destination_folder_text_box,
                trace_destination_folder,

            ],
            # spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        Row(
            controls=[
                csv_destination_folder_text_box,
                csv_destination_folder,

            ],
            # spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        Row(
            controls=[
                ft.IconButton(icon=ft.icons.PLAY_CIRCLE_OUTLINE_SHARP, on_click=lambda _: generate_csv(), icon_size=40),
            ],
            # spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Divider(),
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Stack(
                        [
                            pr,
                        ],
                        width=50,
                        height=50
                    ),
                    status
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                # alignment=ft.MainAxisAlignment.CENTER,

            ),
            alignment=ft.alignment.center,
            margin=10
        )
    )
    page.update()


ft.app(target=home)

"""
csv:
after 10 boards column 5 changes from 1-1 to 1-2
after again 10 boards it changes from 1-2 to 1-3

max 40 lines so it ends with 1-4


at the moment i dont have more files but when you have it ready tomorrow i will have more files

Will the converted csv save in the same folder where .trace file exist?

no different folder





-----------------------------------------------------------------------------

First question: can you also build software with a gui or do you prefer Python?

We need again a watchdog.
They need to select which kind of production.
1) Default FLX Production.
2) CM Production.

when you select "Default FLX" it needs to copy from folder xxx to folder "C:\Trace_FLX".
when you select "CM Production" it needs to copy from folder xxx to folder "C:\Trace_CM".

The Default FLX option will just copy the .trace file to the other directory
The CM Production need to copy to "C:\Trace_CM" and create also a .csv file 
from it in a different format and place it in "C:\Trace_NF".




"""
