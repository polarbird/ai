#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import os
import logging
import logging.config
import pymysql

from datetime import timedelta, datetime

from ai.config import Config

# 初始化Logger
path = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(path + "/logging.conf")
logger = logging.getLogger()

config = Config('db.yaml')
db = config.data['db']['youpin_zlf']

OFFSET = 30

now = datetime.now()
one_month_ago = now - timedelta(days=OFFSET)
end_time = datetime(one_month_ago.year, one_month_ago.month, one_month_ago.day,
                    0, 0, 0, 0)
cqsj = end_time - timedelta(seconds=123)
zjsj = end_time - timedelta(seconds=62)
fhsj = end_time - timedelta(seconds=1)


def log_time():
    logger.info('当前时间 = ' + str(now))
    logger.info('历史数据标识时间 = ' + str(end_time))
    logger.info('出签时间 = ' + str(cqsj))
    logger.info('质检时间 = ' + str(zjsj))
    logger.info('发货时间 = ' + str(fhsj))


def get_mysql_connection():
    return pymysql.connect(host=db['host'],
                           user=db['user'],
                           password=str(db['password']),
                           db=db['database'],
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def get_table_names():
    result = []
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = "select * from zlf_dlmc"
            cursor.execute(sql)
            res = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    for item in res:
        result.append(item)
    return result


def update_order_status():
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = (
                "update `zlf_order` set `status`=7,`notify_status`=1 where `accepted_at`<'"
                + str(end_time) +
                "' and `status`<7 and `invoice_type` in('sjsprkdh','sjspdrdh','jmsrkdh','jmsdbdh','bqdqdh')"
            )
            logger.info("update_order_status : " + sql)
            result = cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
    logger.info("result of update_order_status is " + str(result))
    return result


def update_order_cqsj():
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = ("Update `zlf_order` set `cqsj`= '" + str(cqsj) +
                   "' where `cqsj` is null and `accepted_at`<'" +
                   str(end_time) + "' and status=7")
            logger.info("update_order_cqsj : " + sql)
            result = cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
    logger.info("result of update_order_cqsj is " + str(result))
    return result

def update_order_zjsj():
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = ("Update `zlf_order` set `zjsj`= '" + str(zjsj) +
                   "' where `zjsj` is null and `accepted_at`<'" +
                   str(end_time) + "' and status=7")
            logger.info("update_order_zjsj : " + sql)
            result = cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
    logger.info("result of update_order_zjsj is " + str(result))
    return result


def update_order_fhsj():
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = ("Update `zlf_order` set `fhsj`= '" + str(fhsj) +
                   "' where `fhsj` is null and `accepted_at`<'" +
                   str(end_time) + "' and status=7")
            logger.info("update_order_fhsj : " + sql)
            result = cursor.execute(sql)
        connection.commit()
    finally:
        connection.close()
    logger.info("result of update_order_fhsj is " + str(result))
    return result


def main():
    log_time()
    update_order_status()
    update_order_cqsj()
    update_order_zjsj()
    update_order_fhsj()


if __name__ == '__main__':
    main()
