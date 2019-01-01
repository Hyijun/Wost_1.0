import re
# import threading
import wiki_html
# import page_info
import urllib.error
from tools import *


class Oversee(threading.Thread):
    def __init__(self, t_name, page_name, output_object):
        threading.Thread.__init__(self)
        self.name = t_name
        self.page_name = page_name
        # self.this_page_info = page_info.get_page_info(page_name)
        self.output_inter = output_object
        self.alive = True
        self.exception = ''

    def run(self):
        add_tkinter_dict_info(self.output_inter, self.name, "开始监视线程：" + self.name)
        try:
            self.overseeing()
        except urllib.error.HTTPError as e:
            add_tkinter_error_dict_info(self.output_inter, self.name, '线程意外退出，错误信息：' + str(e))
            self.alive = False
        except urllib.error.URLError as e:
            add_tkinter_error_dict_info(self.output_inter, self.name, '线程意外退出，错误信息：' + str(e))
            self.alive = False
            self.exception = 'network_cut_off'
        add_tkinter_error_dict_info(self.output_inter, self.name, "因为异常退出线程：" + self.name)

    def overseeing(self):
        url = 'https://zh.wikipedia.org/w/index.php?title=' + self.page_name + '&action=history'
        list1 = []
        html = wiki_html.get_html(url)
        for each_str in re.findall(his_re, html):
            list1.append(each_str)
        list_len = len(list1)
        add_tkinter_dict_info(self.output_inter, self.name, '已获取条目基础信息')
        # add_tkinter_dict_info(self.output_inter, page_name, '\t条目信息：')
        # for k, y in self.this_page_info.items():
        #     add_tkinter_dict_info(self.output_inter, page_name, '\t' + k + ': ' + y[0])
        add_tkinter_dict_info(self.output_inter, self.name, '开始监视')
        self.exception = 'OK'

        while 1:
            html = wiki_html.get_html(url)
            for each_str in re.findall(his_re, html):
                if each_str not in list1:
                    list1.append(each_str)
            if len(list1) != list_len:
                if list1[len(list1) - 1][3] == 'null':
                        add_tkinter_dict_info(
                            self.output_inter,
                            self.name,
                            '条目发生变更，在十秒内发生了' + str(len(list1) - list_len) + '次编辑，编辑者' +
                            list1[len(list1) - 1][1] + '，编辑后字节大小变化：' + list1[len(list1) - 1][4] +
                            ',字节数未变更。')
                else:
                    edit_type = '大量' if list1[len(list1) - 1][2] == 'strong' else '少量' + \
                                                                                  '添加内容' if list1[len(list1) - 1][
                                                                                                3] == 'pos' else '删除内容'
                    add_tkinter_dict_info(
                        self.output_inter,
                        self.name, '条目发生变更，在十秒内发生了' +
                        str(len(list1) - list_len) + '次编辑，编辑者' +
                        list1[len(list1) - 1][1] + '，编辑后字节大小变化：' +
                        list1[len(list1) - 1][4] + '，属于' + edit_type + '编辑')
                list_len = len(list1)
                time.sleep(10)
            else:
                time.sleep(10)
            if not self.alive:
                add_tkinter_colour_dict_info(self.output_inter, key=self.name, info='监视线程正常退出', bg_c='gray')
                exit()


his_re = re.compile('<li data-mw-revid="(\d*)".*?<span '
                    + "class='history-user'>.*?<bdi>(.*?)</bdi>.*?"
                      '<(span|strong) dir="ltr" class="mw-plusminus-(pos|neg|null)'
                      ' mw-diff-bytes" title=".*?">(.*?)</(span|strong)>')
