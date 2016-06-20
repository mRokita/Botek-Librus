# -*- coding: utf-8 -*-
import cookielib
import urllib2
from urllib import urlencode
import site_parser

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
        # Dodanie nagłówków HTTP
        self.__opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0)')
        ]

    def login(self):
        self.__login()

    def __login(self):
        """Funkcja wykonująca logowanie do librusa"""
        # Odebranie ciasteczek
        self.__opener.open("https://synergia.librus.pl/loguj")

        # Wysłanie danych logowania za pomocą POST
        data = self.__opener.open("https://synergia.librus.pl/loguj",
                     urlencode({"login": self.__username,
                                "passwd": self.__password,
                                "ed_pass_keydown": "",
                                "ed_pass_keyup": "",
                                "captcha": "",
                                "jest_captcha": "1",
                                "czy_js": "0"}))
        if "Podano nieprawidłowe hasło lub login" in data.read():
            raise WrongPasswordError

    def get_announcements(self):
        """
        Funkcja pobierająca dane ze strony https://librus.synergia.pl/ogloszenia
        :returns: :return: lista [{"author": autor,
                         "title": tytuł,
                         "time": czas,
                         "content": zawartość}]
        """
        # Załadowanie ogłoszeń
        data = self.__opener.open("https://synergia.librus.pl/ogloszenia").read()
        if "Brak dostępu" in data:
            raise SessionExpiredError
        return site_parser.announcements_from_html(data)
