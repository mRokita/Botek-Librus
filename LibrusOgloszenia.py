#!/usr/bin/env python
# -*- coding: utf-8 -*-
from facebook import Facebook, Post
from announcement import Announcements
from librus import Librus
from time import strftime, sleep
import config
from os.path import exists
from json import loads, dumps

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
            events.append("Brak zmian dla naszej klasy na ten dzień (Jak na razie)")

        post = Post(message=announcement.title+"\n\n"+"\n".join(sorted(events)))
        if was_updated:
            print "Aktualizowanie " + announcement.title
            post.id = sent_announcements[announcement.id]["post_id"]
            facebook.update_post(post)
            facebook.add_comment(post.id, "Edytowano ogłoszenie.")
            sent_announcements[announcement.id]["checksum"] = announcement.checksum
        else:
            print "Dodawanie " + announcement.title
            post_id = facebook.add_post(config.group_id, post)
            sent_announcements[announcement.id] = {"post_id": post_id, "checksum": announcement.checksum}
        with open(".sent_announcements", "w+") as fo:
            fo.write(dumps(sent_announcements))

if __name__ == "__main__":
    if exists(".sent_announcements"):
        with open(".sent_announcements", "r+") as fo:
            sent_announcements = loads(fo.read())
    else:
        sent_announcements = {}

    a_post_ids = []
    facebook = Facebook(config.token)
    announcements = Announcements(Librus(config.login, config.password), on_new_announcement, config.filter_class)
    while True:
        print "Updating..."
        try:
            announcements.update()
            print "Updated!"
        except Exception, e:
            print e
        sleep(60)
