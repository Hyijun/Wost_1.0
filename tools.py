import time
import threading
import tkinter

lock = threading.Lock()


def _format_dict_info(key, info):
    now_time = time.strftime('%H:%M:%S /', time.localtime(time.time()))
    return '[' + now_time + 'INFO/' + key + '] ' + info + '\n'


def add_tkinter_dict_info(output_object, key='Unknow', info='<None>'):
    output_object.insert(tkinter.END, _format_dict_info(key=key, info=info))


def add_tkinter_error_dict_info(output_object, key='ERROR', info='Some Unknow error appeared.'):
    add_tkinter_colour_dict_info(output_object, bg_c='red', key=key, info=info)


def add_tkinter_colour_dict_info(output_object, bg_c='white', font_c='black', key='Unknow', info='<None>'):
    if lock.acquire():
        output_object.insert(tkinter.END, _format_dict_info(key=key, info=info))
        output_object.itemconfig(tkinter.END, bg=bg_c, fg=font_c)
    lock.release()
