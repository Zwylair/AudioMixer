import copy
import json
import subprocess
from datetime import datetime
import dearpygui.dearpygui as dpg
import pydub.exceptions
from tabulate import tabulate
from funcs import *

pydub.AudioSegment.converter = FFMPEG_PATH
pydub.AudioSegment.ffprobe = '/ffmpeg/ffprobe.exe'


def drop_handler(fns: list):
    # define a directory and add subfiles to it
    all_fns = copy.copy(fns)
    for i in fns:
        if os.path.isdir(i):
            all_fns.remove(i)
            all_fns += get_all_files(i)

    headers = ['Name', 'Weight', 'Extension', 'Status']
    shorted_fn_dict = {}
    data = []

    # data collection into a single array
    for i in all_fns:
        fn = get_strf_name(i)
        shorted_fn_dict[fn] = i
        weight = get_strf_weight(os.path.getsize(i))
        extension = os.path.splitext(i)[1].lstrip('.')[:9]

        if extension in SUPPORTED_FORMATS:
            data.append([fn, weight, extension, 'Waiting'])

    dpg.set_value('shorted_fn_dict', json.dumps(shorted_fn_dict))
    dpg.set_value('table_headers', json.dumps(headers))
    dpg.set_value('table_data', json.dumps(data))
    dpg.set_value('log', tabulate(data, headers, tablefmt=TABLEFMT))


def process_button_callback():
    # if the sounds weren't dropped stop
    if dpg.get_value('log') == "Here will be sounds' info":
        return

    def update_log():
        dpg.set_value('log', tabulate(data, headers, tablefmt=TABLEFMT))

    dpg.disable_item('process_button')  # prevent breakage of the mixing code

    shorted_fn_dict = json.loads(dpg.get_value('shorted_fn_dict'))
    headers = json.loads(dpg.get_value('table_headers'))
    data = json.loads(dpg.get_value('table_data'))
    out_format = dpg.get_value('file_format')
    loaded = []

    # every loaded file
    for line, line_index in zip(data, range(len(data))):
        fn, weight, ext, status = line

        # update status
        data[line_index] = [fn, weight, ext, 'Loading']
        update_log()

        try:  # waiting for corrupted file or etc.
            loaded.append(pydub.AudioSegment.from_file(shorted_fn_dict[fn]))

            data[line_index] = [fn, weight, ext, 'Loaded']
            update_log()
        except BaseException:
            data[line_index] = [fn, weight, ext, 'Loading err']
            update_log()

    data = [[line[0], line[1], line[2], 'Applying' if line[3] == 'Loaded' else line[3]] for line in data]
    update_log()

    if not loaded:
        data = [[line[0], line[1], line[2], 'Audios not found'] for line in data]
        update_log()
        return

    # mixing
    out_audio = loaded[0]
    for i in loaded[1:]:
        out_audio = out_audio + i

    date_strf = datetime.now().strftime("%Y.%m.%d %H-%M")
    output_fn = f'c:\\output\\{len(loaded)} files mixed [{date_strf}].{out_format}'

    if not os.path.exists('c:/output'):
        os.mkdir('c:/output')

    try:
        out_audio.export(output_fn, out_format)
    except OSError:  # no space left on device (idk, maybe it could happen someday)
        complete_status = 'Free space lack'
    else:
        complete_status = 'Done'

    data = [[line[0], line[1], line[2], complete_status if line[3] == 'Applying' else line[3]] for line in data]
    update_log()

    subprocess.Popen(f'explorer /select,"{output_fn}"')
    dpg.enable_item('process_button')
