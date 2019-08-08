#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

from ai.config import Config
import sqlite3
import pymysql
import re
import requests
import json


def format_content(source):
    result = ''
    re_image_a = re.compile('<a[^>]+href="(https://\\S+)"', re.I)
    data = re_image_a.findall(source)
    if len(data) != 0:
        for item in data:
            result = result + '<img src="' + item + '"/>'
    return result


def get_tasks():
    result = []
    conn = sqlite3.connect('D:\\ai\\data\\spider_task.db3')
    c = conn.cursor()
    cursor = c.execute("select id, task_id, last_id from task")
    for row in cursor:
        result.append(dict(id=row[0], task_id=row[1], last_id=row[2]))
    conn.close()
    return result


def update_task(task_id, last_id):
    conn = sqlite3.connect('D:\\ai\\data\\spider_task.db3')
    c = conn.cursor()
    c.execute('update task set last_id = ' + str(last_id) + ' where task_id = ' + str(task_id))
    conn.commit()
    conn.close()


def get_articles_from_sqlite(task_id, last_id):
    result = []
    conn = sqlite3.connect('D:\\火车采集器V9\\Data\\' + str(task_id) + '\\SpiderResult.db3')
    c = conn.cursor()
    cursor = c.execute("select ID, PageUrl, 标题, 内容 from Content where ID > " + str(last_id))
    for row in cursor:
        if row[0] > last_id:
            last_id = row[0]
        content = format_content(row[3])
        if content != '':
            result.append(dict(page_url=row[1], title=row[2], content=content))
    conn.close()
    return result, last_id


def post_articles(articles):
    config = Config()
    crawler_token = config.data['mp']['crawler_token']
    url = 'https://beauty-service.tryer.cn/v1/acg_articles/batch'
    headers = {'CRAWLER': crawler_token}
    requests.post(url, json=articles, headers=headers)


def save_articles_to_mysql(articles):
    config = Config()
    connect_info = config.data['db']['beauty']
    connection = pymysql.connect(host=connect_info['host'],
                                 user=connect_info['user'],
                                 password=str(connect_info['password']),
                                 db=connect_info['database'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "insert into `acg_article` (`page_url`, `title`, `content`) VALUES (%s, %s, %s)"
            for article in articles:
                cursor.execute(sql, (article['page_url'], article['title'], article['content']))
        connection.commit()
    finally:
        connection.close()


def main():
    tasks = get_tasks()
    for task in tasks:
        task_id = task['task_id']
        articles, last_id = get_articles_from_sqlite(task_id, task['last_id'])
        if len(articles) != 0:
            update_task(task_id, last_id)
            # save_articles_to_mysql(articles)
            post_articles(articles)


if __name__ == '__main__':
    main()
