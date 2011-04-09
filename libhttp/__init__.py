#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
libhttp - module for quick http requests
Usage:

import libhttp
libhttp.req("http://www.google.com",
    headers=headers     # dict or list of strings
    cookie=cookie       # dict or str like "a=b&c=d"
    data=post_data      # dict or str like "a=b&c=d"
    get=get_data        # dict or str like "a=b&c=d"
    auth=(user, pass)   # tuple (HTTP Basic Auth)
    proxy="host:port"   # both for http and https
    proxy_auth=(u, p)   # tuple for proxy auth
    timeout=10          # 10 seconds
)

Author: Author: hellman ( hellman1908@gmail.com )
License: GNU GPL v2 ( http://opensource.org/licenses/gpl-2.0.php )
"""

import sys
import urllib
import urllib2
from MultipartPostHandler import MultipartPostHandler as _UploadHandler


_PASSWORD_MGR = urllib2.HTTPPasswordMgrWithDefaultRealm


class req():

    def __init__(self, url, headers=None, cookie=None, data=None, get=None,
                          auth=None, proxy=None, proxy_auth=None, timeout=10):
        self.url = url
        self.is_file_post = False
        self.data = None
        self.request_headers = {"User-Agent": "Mozilla/5.0"}

        if "://" not in url:
            self.url = "http://" + self.url

        if get:
            self.update_get(get)

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
            handlers.append(_UploadHandler)

        opener = urllib2.build_opener(*handlers)
        opener.addheaders = self.request_headers.items()
        res = opener.open(self.url, self.data, timeout)

        self.data = res.read()
        self.status = res.code
        self.headers = res.headers.dict
        return

    def auth_handler(self, auth):
        h = urllib2.HTTPBasicAuthHandler(_PASSWORD_MGR())
        h.add_password(None, self.url, auth[0], auth[1])
        return h

    def proxy_handler(self, proxy):
        h = urllib2.ProxyHandler({'http': proxy, 'https': proxy})
        return h

    def proxy_auth_handler(self, proxy_auth):
        h = urllib2.ProxyBasicAuthHandler(_PASSWORD_MGR())
        h.add_password(None, self.url, proxy_auth[0], proxy_auth[1])
        return h

    def update_get(self, get):
        if type(get) == str:
            get = _dict_from_str(get, "&", "=")

        if "?" in self.url and self.url[-1] != "?":
            self.url += "&"
        
        gets = []
        for key in get:
            gets.append(urllib.quote(str(key)) + "=" + urllib.quote(str(get[key])))
        get_str = "&".join(gets)

        self.url += get_str
        return

    def update_headers(self, headers):
        if type(headers) == dict:
            self.request_headers.update(headers)
        if type(headers) == list:
            for h in headers:
                if type(h) == str:
                    name, value = h.split(": ", 1)
                    self.request_headers[name] = value
                elif type(h) == tuple:
                    self.request_headers[str(h[0])] = str(h[1])
        return

    def update_cookie(self, cookie):
        if type(cookie) == str:
            cookie = _dict_from_str(cookie, "&", "=")

        cookies = []
        for key in cookie:
            cookies.append(urllib.quote(str(key)) + "=" + urllib.quote(str(cookie[key])))
        cookie_str = "; ".join(cookies)

        if "Cookie" in self.request_headers:
            c = ""
            if self.request_headers["Cookie"].strip()[-1] != ";":
                c = "; "
            self.request_headers["Cookie"] += c + cookie_str
        else:
            self.request_headers["Cookie"] = cookie_str
        return

    def update_data(self, data):
        if type(data) == str:
            data = _dict_from_str(data, "&", "=")

        str_data = {}
        for key, value in data.iteritems():
            if type(value) == file or hasattr(value, "upload_name"):
                self.is_file_post = True
                str_data[str(key)] = value
            else:
                str_data[str(key)] = str(value)

        if self.is_file_post:
            self.data = str_data  # Multipart handler encodes it byself
        else:
            self.data = urllib.urlencode(str_data)
        return


class UploadFile:
    def __init__(self, s, filename):
        if type(s) == str:
            self.data = str(s)
        elif type(s) == file:
            self.data = s.read()
        else:
            raise TypeError("Unknown type passed to UploadFile")

        self.upload_name = filename
        self.size = len(self.data)

    def seek(self, x):
        pass

    def read(self, l=None):
        return self.data


def _dict_from_str(data, item_sep, key_sep):
    lst = data.split(item_sep)
    d = {}
    for pair in lst:
        key, value = pair.split(key_sep, 1)
        d[key] = value
    return d


def _main():
    """
    Usage example.
    """
    data = {"username": "hellman", "password": 1234,
            "picture": UploadFile(open("avatar.jpg"), "uploaded_filename.jpg")}
                # or open ("avatar.jpg") - uploaded filename will be avatar.jpg

    r = req("http://localhost/auth_test/index.php?id=3",
        get={"page": 10, "order": "None"},  # or "page=10&order=None",
        auth=("hellman", "preved"),
        headers=["User-Agent: NotMozilla/5.0", "Cookie: PHPSESSID=blabla"],
        cookie={"adv_id": 10, "cache": "blabla"},  # or "adv_id=10&cache=blabla",
        data=data)  # or "username=hellman&password=1234" (but without file)

    print "[HEADERS]"
    print r.headers
    print

    print "[HTML PAGE]"
    print r.data
    print

    return

#[HEADERS]
    #Date: Sun, 10 Apr 2011 05:40:34 GMT
    #Server: Apache/2.2.16 (Ubuntu)
    #X-Powered-By: PHP/5.3.3-1ubuntu9.3
    #Vary: Accept-Encoding
    #Content-Length: 755
    #Connection: close
    #Content-Type: text/html


#[HTML PAGE]
    #COOKIE:
    #'PHPSESSID' => 'blabla'
    #'cache' => 'blabla'
    #'adv_id' => '10'

    #POST:
    #'username' => 'hellman'
    #'password' => '1234'

    #GET:
    #'id' => '3'
    #'page' => '10'
    #'order' => 'None'

    #FILES:
    #Array
    #(
    #    [picture] => Array
    #        (
    #            [name] => uploaded_filename.jpg
    #            [type] => image/jpeg
    #            [tmp_name] => /tmp/phpD9r0Sk
    #            [error] => 0
    #            [size] => 31425
    #        )

    #)

    #REQUEST_HEADERS:
    #'Accept-Encoding' => 'identity'
    #'Content-Length' => '31822'
    #'Connection' => 'close'
    #'User-Agent' => 'NotMozilla/5.0'
    #'Host' => 'localhost'
    #'Cookie' => 'PHPSESSID=blabla; cache=blabla; adv_id=10'
    #'Content-Type' => 'multipart/form-data; boundary=127.0.0.1.1000.30512.1302414034.040.1'
    #'Authorization' => 'Basic aGVsbG1hbjpwcmV2ZWQ='

if __name__ == "__main__":
    _main()
