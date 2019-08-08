#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import os
import urllib3
import json
import datetime
import csv

global app_id
app_id = '478834039'
global pages
#每页50个评论
pages = 10

path = os.path.split(os.path.realpath(__file__))[0]


def search_ios_review(app_id, page_no):
    url = "https://itunes.apple.com/cn/rss/customerreviews/page=" + page_no + "/id=" + app_id + "/sortby=mostrecent/json"
    httpManager = urllib3.PoolManager()
    urllib3.disable_warnings()
    req = httpManager.request('GET', url)
    # print(req.data)
    jsonData = json.loads(req.data)
    # print(jsonData)
    array = jsonData['feed']['entry']
    reviewList = []
    for each in array:
        dic = each['author']
        name = dic['name']['label']
        uri = dic['uri']['label']
        version = each['im:version']['label']
        rating = each['im:rating']['label']
        idStr = each['id']['label']
        title = each['title']['label']
        content = each['content']['label']
        i = [uri, name, version, rating, idStr, title, content]
        reviewList.append(i)
    print('第' + page_no + '页')
    return reviewList


def save(all_review_list):
    file_name = datetime.datetime.now().strftime('%Y%m%d')
    # file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    full_name = path +'/data/' + file_name + '.csv'
    print(full_name)

    with open(full_name, 'w', encoding='utf-8', newline='') as target:
        fieldnames = [
            'uri', 'name', 'version', 'rating', 'id', 'title', 'content'
        ]
        writer = csv.writer(target)
        writer.writerow(fieldnames)
        for row in all_review_list:
            writer.writerow(row)


def main():
    all_review_list = []
    for i in range(0, pages):
        plist = search_ios_review(app_id, str(i + 1))
        all_review_list += plist

    save(all_review_list)


if __name__ == '__main__':
    main()
