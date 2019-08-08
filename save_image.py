#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import sqlite3
import requests


def create_task():
    fp = open('D:\\images\\sexy.txt')
    conn = sqlite3.connect('D:\\images\\task.db3')

    try:
        text_lines = fp.readlines()
        id = 0
        for line in text_lines:
            id = id + 1
            c = conn.cursor()
            c.execute('insert into task (id, url, status) values(' + str(id) +
                      ',\'' + str(line) + '\',0)')
        conn.commit()
    finally:
        conn.close()
        fp.close()


def get_tasks():
    result = []
    conn = sqlite3.connect('D:\\images\\task.db3')
    c = conn.cursor()
    cursor = c.execute("select id, url, status from task where status = 0")
    for row in cursor:
        result.append(dict(id=row[0], url=row[1], status=row[2]))
    conn.close()
    return result


def download_image(tasks):
    conn = sqlite3.connect('D:\\images\\task.db3')
    try:
        for task in tasks:
            response = requests.get(task['url'])
            c = conn.cursor()
            if response.status_code == 200:
                f = open('D:\\images\\data\\' + str(task['id']) + '.jpg', 'wb')
                try:
                    f.write(response.content)
                finally:
                    f.close()

                c.execute('update task set response_url=\'' + response.url +
                          '\', status=' + str(response.status_code) +
                          ' where id=' + str(task['id']))
            else:
                c.execute('update task set status=' +
                          str(response.status_code) + ' where id=' +
                          str(task['id']))
            conn.commit()
    finally:
        conn.close()


def main():
    tasks = get_tasks()
    download_image(tasks)


if __name__ == '__main__':
    main()
