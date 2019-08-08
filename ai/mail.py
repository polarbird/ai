#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import os
import logging
import logging.config
import smtplib

from email.mime.text import MIMEText

from ai.config import Config

# 初始化Logger
path = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(path + "/../logging.conf")
logger = logging.getLogger()


class Mail:
    def __init__(self):
        self.__config = Config('mail.yaml').data['mail']
        self.__server = smtplib.SMTP_SSL(self.__config['host'],
                                         self.__config['port'])
        self.__server.set_debuglevel(1)
        self.__server.login(self.__config['username'],
                            self.__config['password'])        

    def send(self, to_addr, subject, content):
        message = MIMEText(content,_subtype='plain',_charset='utf-8')
        message['Subject'] = subject
        message['From'] = 'AIDevOps <'+self.__config['username'] + '>'
        message['To'] = ";".join(to_addr)
        self.__server.sendmail(self.__config['username'], to_addr, message.as_string())

    def notice(self, content):
        to_addr = [self.__config['receiver']]
        self.send(to_addr, self.__config['title'], content)
        
    def quit(self):
        self.__server.quit()
