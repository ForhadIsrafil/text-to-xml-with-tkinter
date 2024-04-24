import time
from tkinter import filedialog
import pathlib
import pandas as pd
import flet as ft
from flet import Text, Column, Row, Container, View, AppBar
from flet import RouteChangeEvent, ViewPopEvent, MainAxisAlignment, CrossAxisAlignment

file_path_text_box = ft.TextField("Selected File Path:", read_only=True, width=600)

status = Text("")

pr = ft.ProgressRing(width=200, height=200, stroke_width=20)
pr.color = "#FF5733"
pr.bgcolor = "#96DED1"


def generate_csv(file_path):
    trace_file_path = pathlib.Path(file_path.path)
    # print(trace_file_path)

    status.value = ''
    status.update()
    pr.value = None
    pr.update()

    try:
        df = pd.read_csv(trace_file_path, sep='|', )
        df.columns = columns = ["@1|DateStamp (YYYY-MM-DD)", "@2|TimeStamp (hh:mm:ss) (24h system)",
                                "@3|MP (NLUD/SKVR/DRO/USPB)",
                                "@4|FLXPANELID", "@5|FLXSUBPANELID", "@6|FLXUID", "@7|Result"]
        df.to_csv(f"{trace_file_path.__str__().split('.')[0]}.csv", index=False)
        time.sleep(1)

        for i in range(1, 101):
            pr.value = i
            time.sleep(0.01)
            pr.update()

        status.value = 'Done!'
        status.update()
    except Exception as e:
        status.value = str(e)
        status.update()


def on_dialog_result(e: ft.FilePickerResultEvent):
    # print("Selected files:", e.files)
    # print("Selected file or directory:", e.files[0])
    file_path_text_box.value = e.files[0].path
    file_path_text_box.update()
    generate_csv(e.files[0])


def home(page: ft.Page):
    page.window_width = 800
    page.window_height = 300
    page.window_resizable = False
    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()

    file = ft.ElevatedButton("Choose file...",
                             on_click=lambda _: file_picker.pick_files(allow_multiple=False))

    page.add(
        Row(
            controls=[
                file_path_text_box,
                file,

            ],
            # spacing=5,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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
