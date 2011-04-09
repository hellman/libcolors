#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import types
import Cookie
import cookielib
from MultipartPostHandler import MultipartPostHandler
from urllib import urlencode, quote
from urllib2 import *

# TODO:
# browser() <- req -> req
# proxy
# send files
# strings (or lists of strings) for data, headers
# cookie
# auth

PASSWORD_MGR = HTTPPasswordMgrWithDefaultRealm

class req():

    def __init__(self, url, headers=None, cookie=None, data=None, auth=None,
                            timeout=10, proxy=None, proxy_auth=None):
        self.url = url
        self.is_file_post = False
        self.data = None

        self.request_headers = {"User-Agent": "Mozilla/5.0"}
        if headers:
            self.update_headers(headers)

        if cookie:
            self.update_cookie(cookie)

        if data:
            self.update_data(data)

        handlers = []
        if proxy:
            handlers.append(self.proxy_handler(proxy))
        if proxy_auth:
            handlers.append(self.proxy_auth_handler(proxy_auth))
        if auth:
            handlers.append(self.auth_handler(auth))
        if self.is_file_post:
            handlers.append(MultipartPostHandler)
            print "MULTIPART APPEND"

        opener = build_opener(*handlers)
        opener.addheaders = self.request_headers.items()
        res = opener.open(self.url, self.data, timeout)

        self.data = res.read()
        self.status = res.code
        self.headers = res.headers
        return

    def auth_handler(self, auth):
        h = HTTPBasicAuthHandler(PASSWORD_MGR())
        h.add_password(None, self.url, auth[0], auth[1])
        return h

    def proxy_handler(self, proxy):
        h = ProxyHandler({'http': proxy, 'https': proxy})
        return h

    def proxy_auth_handler(self, proxy_auth):
        h = ProxyBasicAuthHandler(PASSWORD_MGR())
        h.add_password(None, self.url, proxy_auth[0], proxy_auth[1])
        return h

    def update_headers(self, headers):
        if type(headers) == types.DictType:
            self.request_headers.update(headers)
        if type(headers) == types.ListType:
            for h in headers:
                if type(h) == types.StringType:
                    name, value = h.split(": ", 1)
                    self.request_headers[name] = value
                elif type(h) == types.TupleType:
                    self.request_headers[h[0]] = h[1]
        return

    def update_cookie(self, cookie):
        cookies = []
        for key in cookie:
            cookies.append(quote(key) + "=" + quote(cookie[key]))
        cookie_str = "; ".join(cookies)

        if "Cookie" in self.request_headers:
            self.request_headers["Cookie"] += "; " + cookie_str
        else:
            self.request_headers["Cookie"] = cookie_str
        return

    def update_data(self, data):
        self.data = data  #urlencode(data)
        for name, value in data.iteritems():
            if type(value) == types.FileType:
                self.is_file_post = True
                return
        return


headers = {"User-Agent": "Medved/5.0", "Cookie": "first=next"}
r = req("http://localhost/auth_test/?lol=qwe", auth=("hellman", "preved"),
                                       headers=headers,
                                       cookie={"user": "test", "u%20ser2": "test2"},
                                       data={"@posted%20%20": "medved%20", "filik": open("/etc/passwd")})
print "\n---\n"
print r.request_headers.items()
print "\n---\n"
print r.data
print "---\n"
print r.headers


sys.exit(0)




class Browser():
    def __init__(self):
        return


class req_old:

    """Do a HTTP request and return an object with answer headers and data."""

    def __init__(self, url, path="/", method="GET", data={}, headers={},
                                                    timeout=5, addr=None):

        if addr is None:
            addr = url + ":80"

        headers["Host"] = url
        headers["Connection"] = "Close"

        if data:
            method = "POST"

        if method == "POST":
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        params = urllib.urlencode(data)
        #print addr, headers, path
        conn = httplib.HTTPConnection(addr, timeout=timeout)
        conn.request(method, path, params, headers)
        res = conn.getresponse()

        self.status = (res.status, res.reason)
        self.headers_list = res.getheaders()
        self.data = res.read()

        self.headers = dict()
        for header, value in self.headers_list:
            self.headers[header] = value

        conn.close()

        #ret = {"status": status,
        #        "headers": headers,
        #        "data": data}
        return

# ---------------------
req = Request(url='https://localhost/cgi-bin/test.cgi',
                      data='This data is passed to stdin of the CGI')
print urlopen(req).read()
# ---------------------
opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
opener.open('http://www.example.com/')
# ---------------------
proxy_handler = ProxyHandler({'http': 'http://www.example.com:3128/'})
proxy_auth_handler = ProxyBasicAuthHandler()
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

opener = build_opener(proxy_handler, proxy_auth_handler)
# This time, rather than install the OpenerDirector, we use it directly:
opener.open('http://www.example.com/login.html')
