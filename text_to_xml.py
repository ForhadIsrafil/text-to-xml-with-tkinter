import os
import time
import pandas as pd
from tkinter import filedialog
import pathlib
import sys
import glob
import re


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


def generate_xml_file(text_file_path, destination_folder, source_folder):
    text_data = open(text_file_path).read()

    lines = text_data.strip().split('\n')

    parent_barcode = ''
    operator = ''
    # barcode = ''
    name = ''
    result = ''
    value = ''
    #     circuit_index = ''

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
            # df.to_csv("data.csv", index=False)
            for idx, single_data in df.iterrows():
                dict_data = single_data.to_dict()
                if dict_data['Messwert'].startswith("PP"):
                    if "B" in dict_data['Messwert']:
                        parent_barcode = dict_data['Messwert'].replace("B", "T")
                    else:
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
            if len(separated_child[0]['Messwert']) > 15:
                barcode = separated_child[0]['Messwert']
                circuit_index = re.sub("\D", "", separated_child[0]['Bezeichnung'])
                # print(barcode, circuit_index)

                # generate measurements
                messurement_arr = []
                for child in separated_child:
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

                # generate each child
                child_str = f"""<Child>
                                <Barcode>{barcode}</Barcode>
                                <CircuitIndex>{circuit_index}</CircuitIndex>
                                <Measurements>
                                    {"".join(messurement_arr)}
                                </Measurements>
                            </Child>\n"""
                childs_arr.append(child_str)

        # build full xml data string for xml file
        childs = "".join(childs_arr)
        xml_str = (f"<?xml version='1.0' encoding='utf-8'?>\n"
                   f"<TestData>"
                   f"<UpdateExistingIdentifiers>True</UpdateExistingIdentifiers>\n"
                   f"<Operator>{operator}</Operator>\n"
                   f"<ParentBarcode>{parent_barcode}</ParentBarcode>\n"
                   f"<Children>\n{childs}</Children>\n"
                   f"</TestData>")

        with open(f'{destination_folder}/{parent_barcode}.xml', "w") as xml_file:
            xml_file.write(xml_str)

        # move text text file to the "processed_to_xml" folder
        os.rename(text_file_path, source_folder / "processed_to_xml" / text_file_path.name)


def main(source_folder, destination_folder):
    text_files_paths = []
    for path in source_folder.iterdir():
        if path.is_file() and path.name.endswith(".txt"):
            text_files_paths.append(path)
    print(text_files_paths)

    for text_file_path in text_files_paths:
        # file_name = text_file_path.name.replace('.txt', '')
        try:
            generate_xml_file(text_file_path=text_file_path, destination_folder=destination_folder,
                              source_folder=source_folder)
        except Exception as e:
            print(e)


if __name__ == "__main__":

    print("SELECT YOUR SOURCE FOLDER...")
    source_folder = get_source_folder()

    try:
        os.mkdir(source_folder / "processed_to_xml")
    except Exception as e:
        pass

    print("SELECT YOUR DESTINATION FOLDER...")
    destination_folder = get_destination_folder()

    while True:
        main(source_folder, destination_folder)
        time.sleep(10)
