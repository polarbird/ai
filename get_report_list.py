#!/usr/bin/env python
# coding: utf-8
# author: Leo <jlm0808@126.com>

from ai.config import Config
import requests
import json
import pymysql

headers = {
    'User-Agent':
    ("Mozilla/5.0 (Linux; Android 4.4.2; MI 6  Build/NMF26X) "
     "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 "
     "Mobile Safari/537.36 MicroMessenger/6.6.7.1321(0x26060736) NetType/WIFI "
     "Language/zh_CN MicroMessenger/6.6.7.1321(0x26060736) NetType/WIFI Language/zh_CN"
     )
}


def save_industry(sid):
    url = 'https://baogao.applinzi.com/api/theme/apiindex'
    body = {'sid': sid}
    response = requests.post(url, data=body, headers=headers)
    industries = response.json().get('infor').get('data')
    save_industry_to_mysql(industries)


def save_parents(sid, industry_id):
    current_page = 1
    next_page = 2
    while current_page < next_page:
        parents = get_parent_list(sid, industry_id, current_page)
        if len(parents) != 0:
            print(str(industry_id) + ' page_index : ' + str(current_page))
            save_parent_to_mysql(parents)
            next_page += 1
        current_page += 1


def get_parent_list(sid, industry_id, page=1):
    url = 'https://baogao.applinzi.com/api/ffile/apiindex'
    body = {'sid': sid, 'theme_id': industry_id, 'rank_type': 1, 'page': page}
    response = requests.post(url, data=body, headers=headers)
    return response.json().get('infor').get('data')


def get_report_list(sid, parent_id, page=1):
    url = 'https://baogao.applinzi.com/api/ffile/apiDirFiles'
    body = {'sid': sid, 'parent_id': parent_id, 'page': page}
    response = requests.post(url, data=body, headers=headers)
    return response.json().get('infor').get('item_list')


def get_mysql_connection():
    config = Config()
    connect_info = config.data['db']['baogao']
    return pymysql.connect(
        host=connect_info['host'],
        user=connect_info['user'],
        password=str(connect_info['password']),
        db=connect_info['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


def save_industry_to_mysql(industries):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = "insert into `industry` (`id`, `name`) VALUES (%s, %s)"
            for row in industries:
                for industry in row:
                    cursor.execute(sql, (industry['id'], industry['name']))
        connection.commit()
    finally:
        connection.close()


def save_parent_to_mysql(parents):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = "insert into `parent` (`id`, `item_id`, `industry_id`,`name`) VALUES (%s, %s, %s, %s)"
            for parent in parents:
                cursor.execute(
                    sql,
                    (parent['id'], parent['item_id'], parent['theme_id'], parent['name']))
        connection.commit()
    finally:
        connection.close()


def save_report_to_mysql(reports):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = "insert into `report` (`id`, `parent_id`, `name`, `url`, `share_url`, `create_time`) VALUES (%s, %s, %s, %s, %s, %s)"
            for report in reports:
                cursor.execute(sql,
                               (report['id'], report['parent_id'],
                                report['name'], report['online_url'],
                                report['share_url'], report['create_time']))
        connection.commit()
    finally:
        connection.close()


def get_parents_from_mysql():
    result = []
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = "select * from parent"
            cursor.execute(sql)
            res = cursor.fetchall()
        connection.commit()
    finally:
        connection.close()
    for item in res:
        result.append(item['item_id'])
    return result


def save_reports(sid, parent_id):
    current_page = 1
    next_page = 2
    while current_page < next_page:
        reports = get_report_list(sid, parent_id, current_page)
        if len(reports) != 0:
            print(parent_id + ' page_index : ' + str(current_page))
            save_report_to_mysql(reports)
            next_page += 1
        current_page += 1


def main():
    sid = 'f05142b48b77ac4993bef27f3b40eecd'
    # save_industry(sid)
    # for industry_id in range(1, 96):
    #     save_parents(sid, industry_id)
    parents = get_parents_from_mysql()
    for parent_id in parents:
        save_reports(sid, parent_id)


if __name__ == '__main__':
    main()
