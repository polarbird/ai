#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

class HTTPError(Exception):
    '''HTTP错误'''


class TaskNotFoundError(Exception):
    '''任务不存在'''


class TaskError(Exception):
    '''任务出错'''


class TimeoutError(Exception):
    '''任务超时'''
