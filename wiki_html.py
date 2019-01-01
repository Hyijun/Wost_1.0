import urllib.request as ur
import sys

proxies = {"http": "http://127.0.0.1:2233", "https": "https://127.0.0.1:2233"}


def get_html(url):
    return ur.urlopen(url).read().decode()


if __name__ == '__main__':
    opener_data = ur.ProxyHandler(proxies)
    opener1 = ur.build_opener(opener_data)
    print(get_html('https://www.baidu.com/'))
