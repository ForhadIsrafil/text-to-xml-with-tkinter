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
text_destination_folder_text_box = ft.TextField("Text Destination Folder Path", read_only=True, width=580)

status = Text("")

pr = ft.ProgressBar(width=500, border_radius=5, scale=5)
pr.color = "#FF5733"
pr.bgcolor = "#96DED1"


def generate_text():
    if len(glob(file_path_text_box.value + "\*.trace")) == 0:
        status.value = "No trace files found/directoy not selected."
        status.color = "#FF5733"
        status.size = 20
        status.update()
        time.sleep(3.5)

        status.value = ''
        status.color = None
        status.update()
        return

    if '\\' not in text_destination_folder_text_box.value:
        status.value = 'Text Destination Folder Path Not Selected.'
        status.color = "#FF5733"
        status.size = 20
        status.update()
        time.sleep(3.5)

        status.value = ''
        status.color = None
        status.update()
        return

    if '\\' not in trace_destination_folder_text_box.value:
        status.value = 'Trace Destination Folder Path Not Selected.'
        status.color = "#FF5733"
        status.size = 20
        status.update()
        time.sleep(3.5)

        status.value = ''
        status.color = None
        status.update()
        return

    for file_path in glob(file_path_text_box.value + "\*.trace"):
        # update status and progress view
        status.value = ''
        status.update()
        pr.value = None
        pr.update()

        # print('file:', file_path)
        file_name = os.path.basename(file_path).split('.')[0]
        # trace_folder_path = pathlib.Path(file_path_text_box.value)
        # destination_folder_path = pathlib.Path(destination_folder_text_box.value)
        # print(destination_folder_path)
        # print(trace_folder_path)
        try:
            with open(file_path, 'r') as trace_file:
                trace_data = trace_file.readlines()

            with open(f"{text_destination_folder_text_box.value}\\{file_name}.txt", 'w') as text_file:
                all_lines = "".join(line for line in trace_data)
                # print(all_lines)
                text_file.write(all_lines.strip())
                text_file.close()

            shutil.move(file_path, trace_destination_folder_text_box.value)

            # remove the 4 lines that start with SVTL" and in the destination folder
            removed_lines = "".join(line for line in trace_data if "SVTL" not in line)
            with open(f"{trace_destination_folder_text_box.value}\\{file_name}.trace", 'w') as updated_trace_file:
                file = updated_trace_file.write(removed_lines.strip())

            pr.value = 100
            pr.update()

            status.value = file_name + ' [Done!]'
            status.update()
            time.sleep(1)

        except Exception as e:
            pass
            # status.value = str(e)
            # status.update()

    file_path_text_box.value = None
    file_path_text_box.data = None
    file_path_text_box.update()


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

    if text_destination_folder_text_box.data == "text_destination_folder":
        text_destination_folder_text_box.value = e.path
        text_destination_folder_text_box.data = None
        text_destination_folder_text_box.update()


def home(page: ft.Page):
    page.title = "Convert Trace File To Text File."
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

        if folder_name == "text_destination_folder":
            text_destination_folder_text_box.data = folder_name
            text_destination_folder_text_box.update()
            file_picker.get_directory_path(dialog_title="Select Text Destination Folder")

    choose_trace_folder = ft.ElevatedButton("Choose Trace Folder", on_click=lambda _: which_folder("trace_folder"), )

    trace_destination_folder = ft.ElevatedButton("Trace Destination Folder",
                                                 on_click=lambda _: which_folder("trace_destination_folder"))
    text_destination_folder = ft.ElevatedButton("Text Destination Folder",
                                                on_click=lambda _: which_folder("text_destination_folder"))

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
                text_destination_folder_text_box,
                text_destination_folder,

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
                ft.IconButton(icon=ft.icons.PLAY_CIRCLE_OUTLINE_SHARP, on_click=lambda _: generate_text(),
                              icon_size=40),
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
one question, will the output file is a text file or a csv/excel file?
ans: Text

It will convert all files in a folders and will move the original file after processing to C:\FLX_Trace_Processed
and the converted file in C:\FLX_TXT_Generated.


Needs to remove 4 lines and export is as .trace file again
The lines with svtl
Always 4 files


the will be no data like @1 @2



"""
