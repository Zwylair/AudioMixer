import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd
import dnd_setup
import dpg_funcs
from settings import *

dpg.create_context()
dpg_dnd.initialize()
dpg.create_viewport(title='Sound mixer v1.1.0', small_icon='assets/icon.ico', width=533, height=400)

with dpg.value_registry():
    dpg.add_string_value(tag='shorted_fn_dict')
    dpg.add_string_value(tag='table_headers')
    dpg.add_string_value(tag='table_data')
    dpg.add_string_value(tag='file_format', default_value=SUPPORTED_FORMATS[0])

#

with dpg.font_registry():
    with dpg.font('assets/ubuntu_regular.ttf', 14, default_font=True, id='ubuntu'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    with dpg.font('assets/ubuntu_mono-regular.ttf', 12, default_font=False, id='ubuntu_mono'):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
dpg.bind_font('ubuntu')

#

with dpg.window(no_title_bar=True, no_resize=True, no_close=True, no_move=True) as window:
    dpg.add_input_text(default_value="Here will be sounds' info", tag='log',
                       readonly=True, multiline=True, width=500, height=320)

    with dpg.group(horizontal=True):
        dpg.add_combo(SUPPORTED_FORMATS, label='Output format', source='file_format', width=50)
        dpg.add_button(label='Process', tag='process_button', callback=dpg_funcs.process_button_callback)
        dpg.add_text(default_value='Drag&Drop the sounds', color=(90, 90, 90))

dpg.bind_item_font('log', 'ubuntu_mono')
dpg.set_primary_window(window, True)
dnd_setup.setup(dpg_funcs.drop_handler)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
