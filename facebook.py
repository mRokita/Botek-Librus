from urllib2 import urlopen
from urllib import urlencode
from httplib import HTTPSConnection
from json import loads

class Post:
    def __init__(self, message=None, link=None,
                 picture=None, name=None, caption=None, description=None, id=None, updated_time=None):
        if not (message or link):
            raise TypeError("Message or link is required.")
        if not link and (picture or name or caption or description):
            raise TypeError("No link specified.")
        l = locals()
        for var in l:
            if var != "self" and l[var]:
                setattr(self, var, l[var])

    def __repr__(self):
        return "<Post({})>".format(dict(self))

    def __iter__(self):
        for attr in ["message", "link", "picture", "name", "caption", "description"]:
            if hasattr(self, attr):
                yield (attr, getattr(self, attr))

class Facebook:
    FEED_URL = "https://graph.facebook.com/v2.6/{feed_id}/feed?access_token={token}"
    DEL_URL = "/v2.6/{post_id}?access_token={token}"
    POST_URL = "https://graph.facebook.com/v2.6/{post_id}?access_token={token}"
    COMMENT_URL = "https://graph.facebook.com/v2.6/{post_id}/comments?access_token={token}"

    def __init__(self, token):
        self.__token = token

    def format_url(self, url, **kwargs):
        return url.format(token=self.__token, **kwargs)

    def get_feed(self, feed_id):
        return loads(urlopen(self.format_url(self.FEED_URL, feed_id=feed_id)).read())["data"]

    def del_post(self, post_id):
        c = HTTPSConnection("graph.facebook.com")
        c.request('DELETE', self.format_url(self.DEL_URL, post_id=post_id))
        return c.getresponse().read()

    def get_posts(self, feed_id):
        feed = self.get_feed(feed_id)
        ret = []
        for event in feed:
            if "message" in event:
                ret.append(Post(**event))
        return ret

    def update_post(self, post):
        return loads(urlopen(self.format_url(self.POST_URL, post_id=post.id),
                             urlencode(dict(post))).read())

    def add_comment(self, post_id, message):
        return loads(urlopen(self.format_url(self.COMMENT_URL, post_id=post_id),
                             urlencode({"message": message})).read())

    def add_post(self, feed_id, post):
        return loads(urlopen(self.format_url(self.FEED_URL, feed_id=feed_id),
                             urlencode(dict(post))).read())["id"]
