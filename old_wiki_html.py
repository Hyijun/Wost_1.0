import requests as ru
import setting
import data_reader
import os


def proxy_set():
    try:
        proxies = data_reader.get_data('proxy_info.dat')
    except FileNotFoundError:
        print('代理未设置，请设置代理')
        port = setting.get_proxy_port()
        proxies = {"http": "http://127.0.0.1:" + port, "https": "https://127.0.0.1:" + port}
    return proxies


my_proxies = proxy_set()
data_reader.save_data(my_proxies, 'proxy_info.dat')


def get_html(url, headers=None, times=0):
    try:
        return ru.get(url, headers, proxies=my_proxies).text
    except ru.exceptions.SSLError:
        print('WARNING:网络侦测器重试' + str(times) + '次，可能是代理不稳定的征兆。')
        return get_html(url, times=times + 1)
    except ru.exceptions.ProxyError:
        print('错误：连接代理失败，请重新启动程序并完成设置')
        os.remove('proxy_info.dat')
        exit()
