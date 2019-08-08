#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import os
import logging
import logging.config
import pymysql
import json

from datetime import datetime

from ai.config import Config

# 初始化Logger
path = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(path + "/logging.conf")
logger = logging.getLogger()

config = Config('db.yaml')
db = config.data['db']['youpin_zlf']


def get_mysql_connection():
    return pymysql.connect(host=db['host'],
                           user=db['user'],
                           password=str(db['password']),
                           db=db['database'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def get_failed_jobs():
    result = []
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = "select `id`, `payload`, `failed_at` from `failed_jobs`"
            cursor.execute(sql)
            res = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    for item in res:
        result.append(item)
    return result


def main():
    result = get_failed_jobs()
    print(result)


if __name__ == '__main__':
    main()
