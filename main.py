import tkinter as tk
import entry_overseer as eo
import urllib.request as ur
import urllib.parse as up
import setting
from data_reader import *
from tools import *
import dominater
# import os


if __name__ == '__main__':
    t_pool = list()
    names = list()

    root = tk.Tk()
    root.title('WOsT监视器 Beta_1.0')

    output_text_box = tk.Listbox(root, height=25, width=100, font=('微软雅黑', 10))
    output_text_box.grid(row=0, column=0, rowspan=2)

    entry_box_form = tk.Frame(root)
    entry_box_form.grid(row=0, column=1, sticky=tk.NW)

    entry_box = tk.Entry(entry_box_form)
    entry_box.grid(row=0, column=0)

    entry_box_tips_text = tk.StringVar()
    entry_box_tips_text.set('')

    entry_box_tips_text_show = tk.Label(entry_box_form, textvariable=entry_box_tips_text)
    entry_box_tips_text_show.grid(row=2, column=0)

    happening_box = tk.Frame(root)
    happening_box.grid(row=2, column=0, sticky=tk.SW, rowspan=3)

    happening_box_text_show = tk.Label(happening_box, text='当前监视线程数：')
    happening_box_text_show.grid(row=0, column=0)
    thread_quantity_number = tk.StringVar('')
    happening_box_text_n_show = tk.Label(happening_box, textvariable=thread_quantity_number)
    happening_box_text_n_show.grid(row=0, column=1)

    line_1 = tk.Label(happening_box, text='|')
    line_1.grid(row=0, column=2, padx=5)

    system_happening = tk.StringVar()
    system_happening.set('[?]系统状况未知')
    system_happening_box = tk.Label(happening_box, textvariable=system_happening)
    system_happening_box.grid(row=0, column=3)

    def run_entry_overseer(entry_name):
        t_pool.append(eo.Oversee(entry_name, up.quote(entry_name), output_text_box))
        t_pool[-1].setDaemon(True)
        t_pool[-1].start()

    def get_entry_name(entry):
        if entry[:3] == 'add':
            run_entry_overseer(entry[4:])
            names.append(entry[4:])
            save_data(names, 'pages.dat')
            entry_box_tips_text.set('成功：添加成功')
        elif entry[:3] == 'del':
            if not t_pool:
                entry_box_tips_text.set('错误：监视列表是空的，所以无法删除任何监视器')
            for each_t in t_pool:
                if each_t.name == entry[4:]:
                    each_t.alive = False
                    t_pool.remove(each_t)
                    entry_box_tips_text.set('成功：已经将' + each_t.name + '从监视列表中移除')
                    page_list = get_data('pages.dat')
                    page_list.remove(each_t.name)
                    save_data(page_list, 'pages.dat')
                    break
                entry_box_tips_text.set('错误：监视列表中未找到' + entry[4:] + '，请检查拼写')

        else:
            entry_box_tips_text.set('错误：无法加入监视列表，因为参数有误')

    def get_entry_items():
        get_entry_name(entry_box.get())
        entry_box.delete(0, tk.END)


    add_entry_name_button = tk.Button(entry_box_form, text='执行操作', command=lambda: get_entry_items())
    add_entry_name_button.grid(row=1, column=0)

    try:
        proxies = get_data('proxy_info.dat')
    except FileNotFoundError:
        proxies = setting.proxy_set()
        # if os.path.exists('main.py'):
        #     os.popen('py main.py')
        # if os.path.exists('main.exe'):
        #     os.system('start main.exe')
        # exit(0)

    opener_data = ur.ProxyHandler(proxies)
    opener1 = ur.build_opener(opener_data)
    ur.install_opener(opener1)

    try:
        names = get_data('pages.dat')
        add_tkinter_dict_info(output_text_box, 'SYSTEM', '已读取原先监视条目')
    except FileNotFoundError:
        add_tkinter_dict_info(output_text_box, 'SYSTEM', '未找到原先运行遗留数据文件，已建立新的缓存')
    save_data(names, 'pages.dat')

    for each in names:
        t_pool.append(eo.Oversee(each, up.quote(each), output_text_box))

    for each in t_pool:
        each.setDaemon(True)
        each.start()

    dominating = dominater.Dominate(t_pool, thread_quantity_number, system_happening)
    dominating.setDaemon(True)
    dominating.start()

    tk.mainloop()
