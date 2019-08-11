# coding=utf-8
from __future__ import unicode_literals
from configparser import RawConfigParser
from html.parser import HTMLParser
from collections import defaultdict
from os.path import join, dirname
import re


class Attributes(dict):
    def __getitem__(self, name):
        try:
            return super(Attributes, self).__getitem__(name)
        except KeyError:
            return ''


class ConfigParser(RawConfigParser, object):
    def get(self, section, option, *, raw=False, vars=None, fallback=None):
        value = super(ConfigParser, self).get(section, option)
        return value.replace('\\n', '\n')


class HTML2BBCode(HTMLParser):
    """
    HTML to BBCode converter

    >>> parser = HTML2BBCode()
    >>> str(parser.feed('<ul><li>one</li><li>two</li></ul>'))
    '[list][*]one[*]two[/list]'

    >>> str(parser.feed('<a href="http://google.com/">Google</a>'))
    '[url=http://google.com/]Google[/url]'

    >>> str(parser.feed('<img src="http://www.google.com/images/logo.png">'))
    '[img]http://www.google.com/images/logo.png[/img]'

    >>> str(parser.feed('<em>EM test</em>'))
    '[i]EM test[/i]'

    >>> str(parser.feed('<strong>Strong text</strong>'))
    '[b]Strong text[/b]'

    >>> str(parser.feed('<code>a = 10;</code>'))
    '[code]a = 10;[/code]'

    >>> str(parser.feed('<blockquote>Beautiful is better than ugly.</blockquote>'))
    '[quote]Beautiful is better than ugly.[/quote]'

    >>> str(parser.feed('<font face="Arial">Text decorations</font>'))
    '[font=Arial]Text decorations[/font]'

    >>> str(parser.feed('<span style="font-size: 16px;">Text decorations</span>'))
    'Text decorations'

    >>> str(parser.feed('<span style="font-size: 20px;">Text decorations</span>'))
    '[size=125%]Text decorations[/size]'

    >>> str(parser.feed('<span style="font-size: 16px; color: #055bfa;">Text decorations</span>'))
    '[color=royalblue]Text decorations[/color]'

    >>> str(parser.feed('<font color="red">Text decorations</font>'))
    '[color=red]Text decorations[/color]'

    >>> str(parser.feed('<font face="Arial" color="green" size="2">Text decorations</font>'))
    '[color=green][font=Arial][size=2]Text decorations[/size][/font][/color]'

    >>> str(parser.feed('Text<br>break'))
    'Text\\nbreak'

    # >>> str(parser.feed('&nbsp;'))
    # '&nbsp;'
    """

    default_fontsize = None

    def __init__(self, config=None):
        HTMLParser.__init__(self)
        self.config = ConfigParser(allow_no_value=True)
        self.config.read(join(dirname(__file__), 'data/myconf.conf'))
        if config:
            self.config.read(config)

    def handle_starttag(self, tag, attrs):
        if len(attrs) == 1 and attrs[0][0] == 'style':
            new_attrs = []
            for x in attrs[0][1].split(';'):
                if x.strip() != '':
                    k, v = x.strip().split(': ')
                    new_attrs.append((k, v))
            attrs = new_attrs

        if self.config.has_section(tag):
            self.attrs[tag].append(dict(attrs))
            self.data.append(
                self.config.get(tag, 'start') % Attributes(attrs or {}))
            if self.config.has_option(tag, 'expand'):
                self.expand_starttags(tag)

    def handle_endtag(self, tag):
        if self.config.has_section(tag):
            self.data.append(self.config.get(tag, 'end'))
            if self.config.has_option(tag, 'expand'):
                self.expand_endtags(tag)
            self.attrs[tag].pop()

    def handle_data(self, data):
        self.data.append(data)

    def feed(self, data, default_fontsize=16):
        self.data = []
        self.default_fontsize = default_fontsize
        self.attrs = defaultdict(list)
        HTMLParser.feed(self, data)
        return ''.join(self.data)

    def expand_starttags(self, tag):
        for expand in self.get_expands(tag):
            if expand in self.attrs[tag][-1]:
                if expand in ('font', 'font-size'):
                    # 特殊处理
                    pts = int(self.attrs[tag][-1][expand][:-2])
                    percentage = min(pts / self.default_fontsize, 2)
                    if percentage == 1:
                        # default size, pass
                        continue
                    value = self.config.get(expand, 'start') % "{0:.0%}".format(percentage)
                    self.data.append(value)
                elif expand == 'color':
                    color = self.attrs[tag][-1][expand].lower()
                    self.attrs[tag][-1][expand] = self.parse_color_str(color)
                    self.data.append(
                        self.config.get(expand, 'start') % self.attrs[tag][-1])
                else:
                    self.data.append(
                        self.config.get(expand, 'start') % self.attrs[tag][-1])

    def expand_style(self, value):
        for x in value.split(';'):
            if x.strip() != '':
                self.handle_starttag('font', [tuple(x.strip().split(': '))])

    def expand_endtags(self, tag):
        for expand in reversed(self.get_expands(tag)):
            if expand in self.attrs[tag][-1]:
                if expand in ('font', 'font-size'):
                    # 特殊处理，如果字号为默认字号则跳过处理
                    pts = int(self.attrs[tag][-1][expand][:-2])
                    if pts == self.default_fontsize:
                        continue
                    else:
                        self.data.append(
                            self.config.get(expand, 'end') % self.attrs[tag][-1])
                else:
                    self.data.append(
                        self.config.get(expand, 'end') % self.attrs[tag][-1])

    def get_expands(self, tag):
        expands = self.config.get(tag, 'expand').split(',')
        return list(map(lambda x: x.strip(), expands))

    def handle_entityref(self, name):
        self.data.append('&{};'.format(name))

    def handle_charref(self, name):
        self.data.append('&#{};'.format(name))

    def parse_color_str(self, color_str):
        d = {
            '#87ceeb': 'skyblue',
            '#4169e1': 'royalblue',
            '#0000ff': 'blue',
            '#00008b': 'darkblue',
            '#ffa500': 'orange',
            '#ff4500': 'orangered',
            '#dc143c': 'crimson',
            '#ff0000': 'red',
            '#b22222': 'firebrick',
            '#8b0000': 'darkred',
            '#00ff00': 'green',
            '#32cd32': 'limegreen',
            '#2e8b57': 'seagreen',
            '#008080': 'teal',
            '#ff1493': 'deeppink',
            '#ff6347': 'tomato',
            '#ff7f50': 'coral',
            '#800080': 'purple',
            '#4b0082': 'indigo',
            '#deb887': 'burlywood',
            '#f4a460': 'sandybrown',
            '#d2691e': 'chocolate',
            '#a0522d': 'sienna',
            '#c0c0c0': 'silver'
        }
        if color_str in d.keys():
            return d[color_str]
        elif color_str in d.values():
            # 直接就是color_name，此时可以不操作
            return color_str
        elif re.match('#[0-9a-fA-F]{6}', color_str):
            # 都不在，找最近的
            min_diff = 256 ** 2 * 3  # largest possible rgb diff
            best_match = None
            for rgb in d.keys():
                diff = (int(rgb[1:3], 16) - int(color_str[1:3], 16)) ** 2 + \
                       (int(rgb[3:5], 16) - int(color_str[3:5], 16)) ** 2 + \
                       (int(rgb[5:7], 16) - int(color_str[5:7], 16)) ** 2
                if diff < min_diff:
                    min_diff = diff
                    best_match = d[rgb]
            return best_match
        else:
            print(f'[WARNING] Invalid color string {color_str}. Use RoyalBlue as default')
            return 'royalblue'


if __name__ == '__main__':
    import doctest

    doctest.testmod()
