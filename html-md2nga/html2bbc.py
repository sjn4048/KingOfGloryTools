# encoding=utf-8

from html2bbcode.parser import HTML2BBCode
from bs4 import BeautifulSoup
import re
import json
import markdown2
from hashlib import md5
from datetime import date, datetime
import os
from werkzeug.utils import secure_filename
import requests


save_path = './data/save'


def save_text(text, seed, filename, ext):
    hl = md5()
    hl.update(str(seed).encode(encoding='utf-8'))
    md5_hash = hl.hexdigest()
    file_name = secure_filename(f'{md5_hash[:16]}_{filename}.{ext}')
    today = str(date.today().strftime('%Y%m%d'))
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(os.path.join(save_path, file_name), 'w') as f:
        f.write(text)


def get_timestamp():
    return int(datetime.timestamp(datetime.now()))


class Converter:
    def convert(self, text):
        soup = BeautifulSoup(text, 'lxml')
        self.__formalize_html(soup)
        fontsize = self._get_default_fontsize(text)
        return self.__postprocess_text(str(HTML2BBCode().feed(str(soup), default_fontsize=fontsize)))

    @staticmethod
    def __formalize_html(soup):
        for x in soup.find_all():
            if len(x.get_text(strip=True)) == 0:
                children = x.findChildren(recursive=True)
                if all(y.name in ('span', 'strong', 'p') for y in children) and len(children) > 0:
                    x.extract()

    def _get_default_fontsize(self, text):
        reg = re.findall(r'font-size:\s*(\d+)pt', text)
        try:
            font_sizes = [int(s) for s in reg]
            default_size = max(set(font_sizes), key=font_sizes.count)
            if default_size < 8 or default_size > 20:
                default_size = 16
        except ValueError:
            default_size = 16
        return default_size

    def __postprocess_text(self, text):
        text = text.replace('&nbsp;', ' ')
        text = text.replace(u'\xa0', u' ')
        # 一些积累的特殊情况
        text = text.replace('[url=][/url]', '')
        return text


def html2bbcode(html):
    timestamp = get_timestamp()
    filename = html[:15]
    save_text(html, timestamp, filename, 'html')
    conv = Converter()
    bbcode = conv.convert(html, )
    save_text(bbcode, timestamp, filename, 'html.bbc')
    return bbcode


def md2bbcode(md):
    if not md:
        raise Exception('Invalid markdown text.')

    timestamp = get_timestamp()
    filename = md[:15]
    save_text(md, timestamp, filename, 'md')
    html = markdown2.markdown(md)
    save_text(html, timestamp, filename, 'md.html')
    bbcode = Converter().convert(html)
    save_text(bbcode, timestamp, filename, 'md.html.bbc')
    return bbcode


if __name__ == '__main__':
    test_md = '***This is Markdown test***'
    print(f'output: {md2bbcode(test_md)}')
    test_html = '<span style="font-size: 16px; color: #055bfa;">This is HTML test</span>'
    print(f'output: {html2bbcode(test_html)}')
