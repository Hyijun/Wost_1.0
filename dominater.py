import threading
import time


def change_happening_box(thread_quantity_number, t_pool):
    thread_quantity_number.set(str(len(t_pool)))


class Dominate(threading.Thread):
    def __init__(self, gc_t_pool, t_q_num, h_tip):
        threading.Thread.__init__(self)
        self.gc_thread_pool = gc_t_pool
        self.tqn = t_q_num
        self.h_output = h_tip

    def start_gc(self):
        pass

    def t_pool_gc(self):
        for each in self.gc_thread_pool:
            if not each.alive:
                self.gc_thread_pool.remove(each)
        change_happening_box(self.tqn, self.gc_thread_pool)

    def t_error_check(self):
        for each in self.gc_thread_pool:
            if each.exception:
                if each.exception == 'network_cut_off':
                    self.h_output.set('[×]程序无法连接至维基百科服务器')
                if each.exception == 'OK' and self.h_output.get() == '[?]系统状况未知':
                    self.h_output.set('[√]系统运行正常')

    def run(self):
        while 1:
            self.t_pool_gc()
            self.t_error_check()
            time.sleep(2)
