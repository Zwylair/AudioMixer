import copy
import json
import os.path
import subprocess
from datetime import datetime
import dearpygui.dearpygui as dpg
from tabulate import tabulate
from pydub import AudioSegment
from settings import *

AudioSegment.converter = FFMPEG_PATH


def get_strf_weight(weight_b: int):
    weight_postfix = 'b'

    if weight_b > 1200:
        weight_b = int(weight_b) / 1024
        weight_postfix = 'kb'

    if weight_b > 1200:
        weight_b = int(weight_b) / 1024
        weight_postfix = 'mb'

    return f'{weight_b:.2f}'.rstrip('.00') + weight_postfix


def get_strf_name(fn: str) -> str:
    return f'{fn[:FN_LIMIT_HALVED]}...{fn[FN_LIMIT_HALVED - FN_LIMIT_HALVED * 2:]}' if len(fn) > FN_LIMIT else fn


def get_all_files(folder_path) -> list:
    file_list = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def fn_handler(fns: list):
    # define a dirs and append subfiles to list
    all_fns = copy.copy(fns)
    for i in fns:
        if os.path.isdir(i):
            all_fns.remove(i)
            all_fns += get_all_files(i)

    headers = ['Name', 'Weight', 'Extension', 'Status']
    shorted_fn_dict = {}
    data = []

    for i in all_fns:
        fn = get_strf_name(i)
        shorted_fn_dict[fn] = i
        weight = get_strf_weight(os.path.getsize(i))
        extension = os.path.splitext(i)[1].lstrip('.')[:9]

        data.append([fn, weight, extension, 'Waiting'])

    dpg.set_value('shorted_fn_dict', json.dumps(shorted_fn_dict))
    dpg.set_value('headers', json.dumps(headers))
    dpg.set_value('data', json.dumps(data))
    dpg.set_value('log', tabulate(data, headers, tablefmt=TABLEFMT))


def process_button_callback():
    if dpg.get_value('log') == "Here will be sounds' info":
        return

    def update(_data: list):
        dpg.set_value('log', tabulate(_data, headers, tablefmt=TABLEFMT))

    dpg.disable_item('process_button')

    shorted_fn_dict = json.loads(dpg.get_value('shorted_fn_dict'))
    headers = json.loads(dpg.get_value('headers'))
    data = json.loads(dpg.get_value('data'))
    out_format = dpg.get_value('format')
    loaded = []

    for line, line_index in zip(data, range(len(data))):
        fn, weight, ext, status = line
        data[line_index] = [fn, weight, ext, 'Loading']
        update(data)
        loaded.append(AudioSegment.from_file(shorted_fn_dict[fn]))
        data[line_index] = [fn, weight, ext, 'Loaded']
        update(data)

    data_new = [[line[0], line[1], line[2], 'Mixing'] for line in data]
    update(data_new)

    out_audio = loaded[0]
    for i in loaded[1:]:
        out_audio = out_audio + i

    date_strf = datetime.now().strftime("%Y.%m.%d %H-%M")
    output_fn = f'c:\\output\\{len(loaded)} files mixed [{date_strf}].{out_format}'

    if not os.path.exists('c:/output'):
        os.mkdir('c:/output')

    out_audio.export(output_fn, out_format)

    data = [[line[0], line[1], line[2], 'Done'] for line in data]
    update(data)

    subprocess.Popen(f'explorer /select,"{output_fn}"')
    dpg.enable_item('process_button')
