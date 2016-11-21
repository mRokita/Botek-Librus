# -*- coding: utf-8 -*-
import cookielib
import urllib2
import config
import site_parser
from urllib import urlencode
from json import loads


class WrongPasswordError(Exception):
    pass

class SessionExpiredError(Exception):
    pass


class Librus:
    """Klasa odpowiadająca za odbieranie danych z librusa"""
    def __init__(self, login, password):
        self.__username = login
        self.__password = password
        # Stworzenie słoika na ciasteczka ;)
        self.__cj = cj = cookielib.CookieJar()
        self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        self.__login()

    def login(self):
        self.__login()

    def __login(self):
        """Funkcja wykonująca logowanie do librusa"""
        # Odebranie ciasteczek
        self.__opener.addheaders = [('Authorization', 'Basic MzU6NjM2YWI0MThjY2JlODgyYjE5YTMzZjU3N2U5NGNiNGY=')]

        try:
            self.__opener.open('https://synergia.librus.pl')
            list(self.__cj)[0].domain='api.librus.pl'
            tokens = loads(self.__opener.open('https://api.librus.pl/OAuth/Token',
                                              data=urlencode({
                                                  'grant_type': 'password',
                                                  'username': config.login,
                                                  'password': config.password,
                                                  'librus_long_term_token': '1',
                                              })).read())

        except urllib2.HTTPError as e:
            e.getcode() == 400
            raise WrongPasswordError('Nieprawidłowe hasło')
        self.__opener.addheaders = [('Authorization', 'Bearer %s' % tokens['access_token'])]

    def get_announcements(self):
        """
        Funkcja pobierająca dane ze strony https://librus.synergia.pl/ogloszenia
        :returns: :return: lista [{"author": autor,
                         "title": tytuł,
                         "time": czas,
                         "content": zawartość}]
        """
        # Załadowanie ogłoszeń
        try:
            data = loads(self.__opener.open('https://api.librus.pl/2.0/SchoolNotices').read())
        except urllib2.HTTPError:
            raise SessionExpiredError
        print data
        return [{'author': notice[u'AddedBy'][u'Id'],
                 'title': notice[u'Subject'].encode('utf-8'),
                 'content': notice[u'Content'].encode('utf-8'),
                 'time': notice[u'StartDate']
                 } for notice in data[u'SchoolNotices']]
