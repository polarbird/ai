#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import os
import logging
import logging.config
import pyodbc

from ai.config import Config
from ai.mail import Mail

# 初始化Logger
path = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(path + "/logging.conf")
logger = logging.getLogger()

tables = [
    'bcprkdH', 'bcptkdH', 'bqdydH', 'fhdH', 'fldbdH', 'jmsdbdH', 'jmsrkdH',
    'sjspdrdH', 'sjsprkdH', 'sprkdH', 'bcprkdB', 'bcptkdB', 'bqdydB', 'fhdB',
    'fldbdB', 'jmsdbdB', 'jmsrkdB', 'sjspdrdB', 'sjsprkdB', 'sprkdB'
]

config = Config('db.yaml')
db = config.data['db']['zlf']
message = ''


def get_sqlsrv_connection():
    connect_str = 'DRIVER={%s};SERVER=%s,%s;DATABASE=%s;UID=%s;PWD=%s' % (
        db['driver'], db['host'], db['port'], db['database'], db['user'],
        db['password'])
    return pyodbc.connect(connect_str)


def get_top_ten(table_name):
    result = ''
    error = ''
    title = 'TABLE_NAME:' + table_name + '\n'
    sql = 'select top 10 * from %s order by DjLsh desc' % table_name
    conn = get_sqlsrv_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
            count = 'Count:' + str(len(res))
            result = title + count + '\n'
    except Exception as e:
        error = title + str(e) + '\n'
    finally:
        conn.close()
        return result, error


def main():
    results = []
    error_count = 0
    logger.info('开始测试ZLF数据库...')
    for table_name in tables:
        result, error = get_top_ten(table_name)
        if '' == error:
            results.append(result)
        else:
            error_count += 1
            results.append(error)
    if error_count> 0:
        logger.info('连接ZLF数据库出现异常!')
        logger.info('通知邮件发送中...')
        mail = Mail()
        mail.notice(''.join(results))
        logger.info('通知邮件发送成功!')
    else:
        logger.info('连接ZLF数据库正常!')
    logger.info('测试ZLF数据库连接完成!')


if __name__ == '__main__':
    main()
