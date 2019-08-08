#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import pycurl
from io import BytesIO


class HTTPClient(object):
    def __init__(self):
        self.buffer = BytesIO()
        self.curl = pycurl.Curl()
        self.curl.setopt(self.curl.WRITEDATA, self.buffer)
        self.curl.setopt(self.curl.FOLLOWLOCATION, True)
        self.curl.setopt(self.curl.USERAGENT, generate_user_agent())

    def get(self, url):
        result = ''
        self.curl.setopt(self.curl.URL, url)
        self.curl.perform()
        if self.curl.getinfo(self.curl.RESPONSE_CODE) == 200:
            result = self.buffer.getvalue()
        else:
            return None
        self.curl.close()
        return result


def generate_user_agent():
    userAgent = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI "
        "WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400")
    return userAgent
