#!/usr/bin/env python
# -*- coding: utf-8 -*-
from announcement import Announcements
from librus import Librus
from time import strftime, sleep
from telegram.ext import Updater
import config
from os.path import exists
from json import loads, dumps
from cgi import escape


def on_new_announcement(announcement):
    global sent_announcements
    events = []
    was_updated = announcement.id in sent_announcements\
                  and sent_announcements[announcement.id]["checksum"] != announcement.checksum

    if was_updated or announcement.id not in sent_announcements and "planie LO" in announcement.title:
        if announcement.content:
            for event in announcement.content.split("\n"):
                events.append(event)
        else:
            events.append("\nBrak zmian dla naszej klasy na ten dzień (Jak na razie)")
        message_text = "<strong>"+announcement.title+"</strong>"+"\n".join(sorted(events))
        u.bot.send_message(chat_id=config.chat_id, parse_mode='HTML', text=message_text)
        sent_announcements[announcement.id] = {"checksum": announcement.checksum}
        with open(".sent_announcements", "w+") as fo:
            fo.write(dumps(sent_announcements))

if __name__ == "__main__":
    u = Updater(token=config.token)
    if exists(".sent_announcements"):
        with open(".sent_announcements", "r+") as fo:
            sent_announcements = loads(fo.read())
    else:
        sent_announcements = {}

    a_post_ids = []

    announcements = Announcements(Librus(config.login, config.password), on_new_announcement, config.filter_class)
    while True:
        print "Updating..."
        try:
            announcements.update()
            print "Updated!"
        except Exception, e:
            print e
        sleep(60)
