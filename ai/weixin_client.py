#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import time
import json
import requests
import re
import random

from selenium import webdriver

from ai.config import Config



class WeixinClient:
    def __init__(self):
        self._driver = 'C:\\chromedriver\\chromedriver.exe'
        #打开微信公众号登录页面
        self._url = 'https://mp.weixin.qq.com/'
        #搜索微信公众号的接口地址
        self._search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        #微信公众号文章接口地址
        self._appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        self._cookies_file = 'cookie.txt'
        self._headers = {
            "HOST":
            "mp.weixin.qq.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }
        self.set_config()
        self.set_cookies()
        self.set_token()

    def set_config(self):
        config = Config('mp.yaml')
        self._config = config.data['mp']

    def handle(self, accounts):
        #抓取微信公众号文章列表
        for account_id in accounts:
            #爬取微信公众号文章，并存在本地文本中
            print("开始爬取公众号：" + account_id)
            self.get_content(account_id)
            print("爬取" + account_id + "完成")

    #登录微信公众号，获取登录之后的cookies信息，并保存到本地文本中
    def weixin_login(self):
        #用webdriver启动谷歌浏览器
        print("启动浏览器，打开微信公众号登录界面")
        driver = webdriver.Chrome(executable_path=self._driver)
        driver.get(self._url)
        #等待5秒钟
        time.sleep(5)
        print("正在输入微信公众号登录账号和密码......")
        #清空账号框中的内容
        driver.find_element_by_xpath("./*//input[@name='account']").clear()
        #自动填入登录用户名
        driver.find_element_by_xpath("./*//input[@name='account']").send_keys(
            self._config['email'])
        #清空密码框中的内容
        driver.find_element_by_xpath("./*//input[@name='password']").clear()
        #自动填入登录密码
        driver.find_element_by_xpath("./*//input[@name='password']").send_keys(
            self._config['password'])

        # 在自动输完密码之后需要手动点一下记住我
        print("请在登录界面点击:记住账号")
        time.sleep(10)
        #自动点击登录按钮进行登录
        driver.find_element_by_xpath("./*//a[@class='btn_login']").click()
        # 拿手机扫二维码！
        print("请拿手机扫码二维码登录公众号")
        time.sleep(20)
        print("登录成功")
        #重新载入公众号登录页，登录之后会显示公众号后台首页，从这个返回内容中获取cookies信息
        driver.get(self._url)
        #获取cookies
        cookie_items = driver.get_cookies()
        self.write_cookies(cookie_items)
        self.set_cookies()

    def write_cookies(self, cookies):
        #定义一个空的字典，存放cookies内容
        post = {}
        #获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
        for cookie_item in cookies:
            post[cookie_item['name']] = cookie_item['value']
        cookie_str = json.dumps(post)
        with open(self._cookies_file, 'w+', encoding='utf-8') as f:
            f.write(cookie_str)
        print("cookies信息已保存到本地")

    def set_cookies(self):
        #读取上一步获取到的cookies
        with open(self._cookies_file, 'r', encoding='utf-8') as f:
            cookie = f.read()
        self._cookies = json.loads(cookie)

    def set_token(self):
        #登录成功之后的微信公众号首页url变化为：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1849751598，从这里获取token信息
        response = requests.get(url=self._url, cookies=self._cookies)
        if self._url == str(response.url):
            self.weixin_login()
            response = requests.get(url=self._url, cookies=self._cookies)
        self._token = re.findall(r'token=(\d+)', str(response.url))[0]

    #爬取微信公众号文章，并存在本地文本中
    def get_content(self, query):
        #query为要爬取的公众号名称
        fakeid = self.get_fakeid(query)

        max_num = self.get_appmsg_count(query, fakeid)
        #每页至少有5条，获取文章总的页数，爬取时需要分页爬
        num = int(int(max_num) / 5)
        #起始页begin参数，往后每页加5
        begin = 0
        while num + 1 > 0:
            query_id_data = {
                'token': self._token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '{}'.format(str(begin)),
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            print('正在翻页：--------------', begin)

            #获取每一页文章的标题和链接地址，并写入本地文本中
            query_fakeid_response = requests.get(
                self._appmsg_url,
                cookies=self._cookies,
                headers=self._headers,
                params=query_id_data)
            time.sleep(5)
            content = query_fakeid_response.json()
            print(content)
            # self.post_articles(content)
            num -= 1
            begin = int(begin)
            begin += 5
            time.sleep(2)

    def post_articles(self, articles):
        url = 'https://ai-service.tryer.cn/v1/articles/batch'
        headers = {'CRAWLER': self._config['crawler_token']}
        requests.post(url, json=articles, headers=headers)

    def get_fakeid(self, query):
        #搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
        query_id = {
            'action': 'search_biz',
            'token': self._token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5'
        }
        #打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
        search_response = requests.get(
            self._search_url,
            cookies=self._cookies,
            headers=self._headers,
            params=query_id)
        #取搜索结果中的第一个公众号
        lists = search_response.json().get('list')[0]
        #获取这个公众号的fakeid，后面爬取公众号文章需要此字段
        return lists.get('fakeid')

    def get_appmsg_count(self, query, fakeid):
        #搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
        query_id_data = {
            'token': self._token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '0',  #不同页，此参数变化，变化规则为每页加5
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        #打开搜索的微信公众号文章列表页
        appmsg_response = requests.get(
            self._appmsg_url,
            cookies=self._cookies,
            headers=self._headers,
            params=query_id_data)
        #获取文章总数
        return appmsg_response.json().get('app_msg_cnt')
