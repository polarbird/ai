#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

from ai.mail import Mail

mail = Mail()

message = '通知消息正文'


mail.notice(message)
