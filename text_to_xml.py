import pandas as pd
from tkinter import filedialog
import pathlib
import sys
import glob


def get_source_folder():
    folder = filedialog.askdirectory(mustexist=True, title="SELECT SOURCE FOLDER")
    print("SOURCE FOLDER >>>", folder, '\n')
    if not folder:
        sys.exit("NO FOLDER SELECTED")
    return pathlib.Path(folder)


def get_destination_folder():
    folder = filedialog.askdirectory(mustexist=True, title="SELECT DESTINATION FOLDER")
    print("DESTINATION FOLDER >>>", folder, '\n')
    if not folder:
        sys.exit("NO DESTINATION FOLDER SELECTED")
    return pathlib.Path(folder)


def generate_xml_file(source_file_path, file_name, destination_folder):
    text_data = open(source_file_path).read()

    lines = text_data.strip().split('\n')

    parent_barcode = ''
    operator = ''
    barcode = ''
    name = ''
    result = ''
    value = ''
    childs_arr = []
    childs_dicts = {}
    for index, data in enumerate(lines):
        if data.startswith('Testername:'):
            operator = data.split(":")[1].strip()
            # print(operator)

        # print(index,data)
        if data.startswith("Modul\t"):
            # print(index, data)
            required_data = [line.split('\t') for line in lines[index:]]

            # generate xml
            df = pd.DataFrame(required_data[1:], columns=data.split('\t'))

            for idx, single_data in df.iterrows():
                dict_data = single_data.to_dict()
                if dict_data['Messwert'].startswith("PP"):
                    parent_barcode = dict_data['Messwert']

                if "Funktionstest/Laser_DMC" in dict_data['Modul']:
                    # print(dict_data)
                    if dict_data['Bezeichnung'].split(' ')[0] not in childs_dicts:
                        childs_dicts[dict_data['Bezeichnung'].split(' ')[0]] = []

                    if dict_data['Bezeichnung'].split(' ')[0] in childs_dicts:
                        childs_dicts[dict_data['Bezeichnung'].split(' ')[0]].append(dict_data)

            break

    # generate the xml string
    if len(childs_dicts) != 0:
        for separated_child in childs_dicts.values():
            messurement_arr = []
            for child in separated_child:
                if len(child['Messwert']) > 15:
                    barcode = child['Messwert']

                if child['Ergebnis'] == 'Gut':
                    result = 'PASSED'
                try:
                    name = child["Bezeichnung"].split(' ')[1]
                except Exception as e:
                    name = child["Bezeichnung"]

                value = f"{child['Untergrenze']} {child['Messwert']} {child['Obergrenze']}"

                if child['Ergebnis'] == 'Fehler':
                    result = 'FAILED'

                messurement_str = f"""<Measurement>
                                        <Name>{name}</Name>
                                        <Result>{result}</Result>
                                        <Value>{value}</Value>
                                        <Units/>
                                        <LowerLimit/>
                                        <UpperLimit/>
                                        <FailDesc/>
                                        <DateAndTime/>
                                    </Measurement>"""
                messurement_arr.append(messurement_str)
            child_str = f"""<Child>
                            <Barcode>{barcode}</Barcode>
                            <Measurements>
                                {"".join(messurement_arr)}
                            </Measurements>
                        </Child>\n"""
            childs_arr.append(child_str)

        childs = "".join(childs_arr)
        xml_str = (f"<?xml version='1.0' encoding='utf-8'?>\n"
                   f"<TestData>"
                   f"<UpdateExistingIdentifiers>True</UpdateExistingIdentifiers>\n"
                   f"<Operator>{operator}</Operator>\n"
                   f"<ParentBarcode>{parent_barcode}</ParentBarcode>\n"
                   f"<Children>\n{childs}</Children>\n"
                   f"</TestData>")

        with open(f'{destination_folder}/{file_name}.xml', "w") as xml_file:
            xml_file.write(xml_str)


def main():
    print("SELECT YOUR SOURCE FOLDER...")
    source_folder = get_source_folder()
    text_files_paths = []
    for path in source_folder.iterdir():
        if path.is_file() and path.name.endswith(".txt"):
            text_files_paths.append(path)

    print("SELECT YOUR DESTINATION FOLDER...")
    destination_folder = get_destination_folder()

    for text_file_path in text_files_paths:
        file_name = text_file_path.name.replace('.txt', '')
        try:
            generate_xml_file(source_file_path=text_file_path, file_name=file_name,
                              destination_folder=destination_folder)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
