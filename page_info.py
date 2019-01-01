import re
import wiki_html

his_re = re.compile('<li data-mw-revid="(\d*)".*?<span '
                    + "class='history-user'>.*?<bdi>(.*?)</bdi>.*?"
                      '<(span|strong) dir="ltr" class="mw-plusminus-(pos|neg|null)'
                      ' mw-diff-bytes" title=".*?">(.*?)</(span|strong)>')

make_user_re = re.compile('<tr id="mw-pageinfo-firstuser">.*?<bdi>(.*?)</bdi>')
make_time = re.compile('<tr id="mw-pageinfo-firsttime">.*?<a.*?title=".*?">(.*?)</a>')
last_edit_user = re.compile('<tr id="mw-pageinfo-lastuser">.*?<bdi>(.*?)</bdi>')
last_edit_time = re.compile('<tr id="mw-pageinfo-lasttime">.*?<a.*?title=".*?">(.*?)</a>')
edit_times = re.compile('<tr id="mw-pageinfo-edits">.*?<td>(.*?)</td>')
edit_times_near = re.compile('<tr id="mw-pageinfo-recent-edits">.*?<td>(.*?)</td>')
edit_user_near = re.compile('<tr id="mw-pageinfo-recent-authors">.*?<td>(.*?)</td>')


def get_page_info(info_page_title):
    """
    next_page_re = re.compile(r'<a href="(/w/index\.php\?title=.*?)" class="mw-nextlink" title=".*?" rel="next">')
    page_html = wiki_html.get_html(page_url)
    net_page_url = re.search(next_page_re, page_html)
    edit_time = len(re.findall(his_re, page_html))
    while 1:
        net_page_html = wiki_html.get_html(net_page_url)
        edit_time += len(re.findall(his_re, net_page_html))
        net_page_url = re.search(next_page_re, net_page_html)
        if not net_page_url:
            break
    page_info = {'edit_time': edit_time}
    """
    info_page_html = wiki_html.get_html('https://zh.wikipedia.org/w/index.php?title=' + info_page_title + '&action=info'
                                        )
    page_info = dict()
    page_info['创建者'] = re.findall(make_user_re, info_page_html)
    page_info['创建时间'] = re.findall(make_time, info_page_html)
    page_info['最后编辑用户'] = re.findall(last_edit_user, info_page_html)
    page_info['最后编辑时间'] = re.findall(last_edit_time, info_page_html)
    page_info['总编辑次数'] = re.findall(edit_times, info_page_html)
    page_info['30天内编辑次数'] = re.findall(edit_times_near, info_page_html)
    page_info['30天内编辑用户'] = re.findall(edit_user_near, info_page_html)
    return page_info
