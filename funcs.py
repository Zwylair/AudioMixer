import os.path
from settings import *


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
