#-*- coding: utf-8 -*-
"""
Parsowanie strony z ogłoszeniami
"""
import re

PATTERN_ANNOUNCEMENTS = re.compile("<thead>.*?<tr>.*?<td colspan=\\\"2\\\">(.*?)</td>.*?</tr>.*?</thead>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr><tfoot>",
                                   re.DOTALL)

def repl(matchobj):
    """
    :param matchobj: Obiekt do porównania
    :return:
    """
    gr =  matchobj.group(0)
    if gr == "<br />":
        return ""
    elif gr =="&oacute;":
        return "ó"
    elif gr == "&Oacute;":
        return "Ó"
    elif gr == "&quot;":
        return "\""

def announcements_from_html(html):
    """
    Funkja parsująca stronę z ogłoszeniami
    :param html: Zawartość https://librus.synergia.pl/ogloszenia
    :return: lista [{"author": autor,
                     "title": tytuł,
                     "time": czas,
                     "content": zawartość}]
    """
    data = [{"title": a[0],
             "author": a[1][1:],
             "time": a[2][1:],
             "content": re.sub("(<br />)|\\&oacute\\;|\\&Oacute\\;", repl, a[3])}
                for a in PATTERN_ANNOUNCEMENTS.findall(html)]
    return data
