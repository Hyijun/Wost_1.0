import tkinter as tk

import data_reader


def get_proxy_port():
    def finish():
        global items
        items = entry_box1.get()
        tk.Label(root, text='设置完毕，可以关闭此页面').grid(row=3, column=0, columnspan=2)
        root.quit()

    root = tk.Toplevel()
    root.geometry()

    form1 = tk.Frame(root)
    form1.grid(row=0, column=0, columnspan=2)

    text1 = tk.Label(form1, text='您的代理未设置，请在下面的输入框中输入相应信息。', font=('微软雅黑', 13))
    text1.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

    text2 = tk.Label(form1, text='代理于本机的端口号：', font=('微软雅黑', 10))
    text2.grid(row=1, column=0, padx=10, pady=5)

    entry_box1 = tk.Entry(form1)
    entry_box1.grid(row=1, column=1, ipadx=10, ipady=0, pady=0, padx=5)

    finish_button = tk.Button(form1, text='完成', font=('微软雅黑', 8), command=lambda: finish())
    finish_button.grid(row=2, column=0, columnspan=2, ipadx=5, ipady=0, pady=5)

    tk.mainloop()
    del root

    return items


def proxy_set():
    try:
        proxies = data_reader.get_data('proxy_info.dat')
    except FileNotFoundError:
        print('代理未设置，请设置代理')
        port = get_proxy_port()
        proxies = {"http": "http://127.0.0.1:" + port, "https": "https://127.0.0.1:" + port}
        data_reader.save_data(proxies, 'proxy_info.dat')
    return proxies


if __name__ == '__main__':
    print(get_proxy_port())
