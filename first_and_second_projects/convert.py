import datetime as dt
import pathlib
import sys
from tkinter import filedialog


TEMPLATE = '''<?xml version="1.0" encoding="utf8">
<BarcodeList operator="11111">
    <Job assembly="" assemblyRev="" name="{name}" lot="">
        <Barcode scanTime="{scan_time}" id="{id}" custSN="" />
    </Job>
</BarcodeList>
'''


if hasattr(sys, "_MEIPASS"):
    FOLDER = pathlib.Path(sys.executable).parent
else:
    FOLDER = pathlib.Path(__file__).parent
OUTPUT_FOLDER = FOLDER / "archive"
OUTPUT_FOLDER.mkdir(exist_ok=True)


def get_folder() -> pathlib.Path:
    folder = filedialog.askdirectory(mustexist=True)
    if not folder:
        print("Conversion Cancelled")
        sys.exit()
    return pathlib.Path(folder)


def convert(file: pathlib.Path) -> None:
    try:
        with file.open("r", encoding="utf8") as f:
            line = next(f).strip("\n")
        name, others = line.split("||", maxsplit=1)
        assert name
        scan_time, id_, _, status, _, _ = others.split("|")
        assert scan_time
        assert id_
        assert status == "PASS"
        scan_time = dt.datetime.strptime(
            scan_time, "%Y%m%d %H%M%S").isoformat()
        xml_string = TEMPLATE.format(name=name, scan_time=scan_time, id=id_)
        new_file_path = OUTPUT_FOLDER / f"{file.stem}.xml"
        new_file_path.write_text(xml_string)
    except Exception:
        unable_to_process_folder = file.parent / "unabletoprocess"
        unable_to_process_folder.mkdir(exist_ok=True)
        if (unable_to_process_folder / file.name).exists():
            i = 1
            while (
                unable_to_process_folder / f"{file.stem} ({i}){file.suffix}"
            ).exists():
                i += 1
            file.rename(
                unable_to_process_folder / f"{file.stem} ({i}){file.suffix}")
        else:
            file.rename(unable_to_process_folder / file.name)


def main() -> None:
    folder = get_folder()
    for path in folder.iterdir():
        if not path.is_file():
            continue
        convert(path)
    print("Conversion Complete")


if __name__ == "__main__":
    main()
