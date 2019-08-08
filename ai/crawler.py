#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

from ai.http_client import HTTPClient
from ai.weixin_client import WeixinClient
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 30 * 60
HTML_PARSER = 'lxml'


class HtmlCrawler:
    def __init__(self):
        self.client = HTTPClient()

    def get(self, url):
        bValues = self.client.get(url)
        return bValues
        # return str(bValues,'UTF-8')

    def formatHtml(self, html):
        if html is None:
            print('HTML IS NONE')
        elif isinstance(html, int):
            raise TypeError('HTML TYPE ERROR ' + str(html))
        else:
            return BeautifulSoup(html, HTML_PARSER)


class WeixinCrawler:
    def __init__(self):
        self.client = WeixinClient()

    def get(self, weixin_id_list):
        try:
            #登录之后，通过微信公众号后台提供的微信公众号文章接口爬取文章
            #爬取微信公众号文章，并存在本地文本中
            self.client.handle(weixin_id_list)
            print("爬取完成")
        except Exception as e:
            print(str(e))
