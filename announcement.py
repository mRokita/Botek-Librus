# -*- coding: utf-8 -*-
from json import dumps
import re
from librus import SessionExpiredError
from hashlib import md5
from base64 import b64encode
class Announcement:
    """
    Klasa reprezentująca ogłoszenie
    """
    PATTERN_CLASS = "([\d \\,]+)l\\.? ?.{0,8}%s[ABCDEF]{0,4}%s[ABCDEF]{0,4} (.+)"

    def __init__(self, author, time, content, title, trim_to_class = False):
        """
        Funkcja inicjalizująca
        :param author: Autor wpisu
        :param date: Czas wysłania wpisu
        :param content: Zawartość ogłoszenia
        """
        self.author = author
        self.time = time
        self.content = content
        self.title = title
        print [self.title]
        self.id = md5(self.title).hexdigest()
        if trim_to_class:
            self.trim_to_class(trim_to_class)

        self.checksum = md5(self.content).hexdigest() # suma kontrolna używana do porównywania ogłoszeń.

    def trim_to_class(self, cl):
        year, letter = tuple(cl)
        content = ""
        add_to_endline = False
        for i in self.content.split("\n"):
            if i == cl:
                add_to_endline = True
                continue
            if add_to_endline and not i:
                add_to_endline = False
            if add_to_endline or re.match(self.PATTERN_CLASS % (year, letter), i):
                content += i + "\n"
        self.content = content

    def __str__(self):
        return dumps(dict(self))

    def __repr__(self):
        return "<Announcement({}, {}, {})>".format(self.author, self.time, [self.content])

    def __getitem__(self, item):
        return getattr(self, item)

    def __iter__(self):
        return vars(self).iteritems()

class Announcements:
    """
    Klasa reprezentująca listę ogłoszeń
    """
    def __init__(self, librus, on_new_announcement, trim_to_class=False):
        self.librus = librus
        self.announcement_list = dict()
        self.trim_to_class = trim_to_class
        self.on_new_announcement = on_new_announcement

    def update(self):
        try:
            data = self.librus.get_announcements()
        except SessionExpiredError:
            print "Session has expired, loging in again."
            self.librus.login()
            data = self.librus.get_announcements()
        announcement_list = [Announcement(trim_to_class=self.trim_to_class, **a) for a in data]
        announcement_list.reverse()
        for a in announcement_list:
            if (a.id in self.announcement_list and self.announcement_list[a.id].checksum != a.checksum)\
                    or not a.id in self.announcement_list:
                self.announcement_list[a.id] = a
                self.on_new_announcement(a)

    def __iter__(self):
        for a in self.announcement_list.values():
            yield a

