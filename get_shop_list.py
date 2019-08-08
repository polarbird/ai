#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import csv
import re


def check_invoice_number(row):
    invoice_number = row['invoice_number']
    digits = filter(str.isdigit, invoice_number)
    invoice_number_str = ''.join(list(digits))
    if invoice_number_str.startswith('2019'):
        return False
    elif invoice_number_str.startswith('19'):
        return False
    else:
        return True


def get_messages():
    meesages = []
    with open('C:\\ai\\data\\zlf\\source.csv',
              'r',
              newline='',
              encoding='utf-8') as source:
        reader = csv.DictReader(source)
        for row in reader:
            meesages.append(row)

    with open('C:\\ai\\data\\zlf\\message.csv',
              'w',
              newline='',
              encoding='utf-8') as target:
        fieldnames = [
            'shop_id', 'shop_name', 'invoice_number', 'client_id', 'send_time'
        ]
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        for row in meesages:
            writer.writerow(row)


def count_by_shops():
    result = []
    shops = []
    errors = {}
    with open('C:\\ai\\data\\zlf\\message.csv',
              'r',
              newline='',
              encoding='utf-8') as source:
        reader = csv.DictReader(source)
        for row in reader:
            shop_id = row['shop_id']
            if shop_id in errors:
                errors[shop_id] = errors[shop_id] + 1
            else:
                shops.append(shop_id)
                errors[shop_id] = 1

    with open('C:\\ai\\data\\zlf\\shop_count.csv',
              'w',
              newline='',
              encoding='utf-8') as target:
        fieldnames = ['shop_id', 'count']
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        for shop_id in shops:
            writer.writerow({'shop_id': shop_id, 'count': errors[shop_id]})


def get_province(name):
    return name[0:2]


def get_address():
    shops = []
    address = {}
    names = {}
    with open('C:\\ai\\data\\zlf\\shops.csv',
              'r',
              encoding='utf-8',
              newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            shop_id = row['shop_id'].upper().strip()
            shops.append(shop_id)
            address[shop_id] = get_province(row['name'])
            names[shop_id] = row['name']

    with open('C:\\ai\\data\\zlf\\address.csv',
              'w',
              encoding='utf-8',
              newline='') as target:
        fieldnames = ['shop_id', 'province', 'name']
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        for shop_id in shops:
            writer.writerow({
                'shop_id': shop_id,
                'province': address[shop_id],
                'name': names[shop_id]
            })


def save_count():
    shops = []
    counts = {}
    address = {}
    names = {}
    with open('C:\\ai\\data\\zlf\\shop_count.csv',
              'r',
              encoding='utf-8',
              newline='') as csv_shops:
        reader = csv.DictReader(csv_shops)
        for row_1 in reader:
            shop_id = row_1['shop_id']
            shops.append(shop_id)
            counts[shop_id] = row_1['count']
    with open('C:\\ai\\data\\zlf\\address.csv',
              'r',
              encoding='utf-8',
              newline='') as csv_address:
        reader = csv.DictReader(csv_address)
        for row in reader:
            address[row['shop_id']] = row['province']
            names[row['shop_id']] = row['name']

    with open('C:\\ai\\data\\zlf\\result.csv', 'w', encoding='utf-8',
              newline='') as target:
        fieldnames = ['shop_id', 'province', 'name', 'count']
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        for key in counts:
            print(key)
            writer.writerow({
                'shop_id': key,
                'province': address[key],
                'name': names[key],
                'count': counts[key]
            })


def get_clients():
    clients = []
    with open('C:\\ai\\data\\zlf\\message.csv',
              'r',
              encoding='utf-8',
              newline='') as source:
        reader = csv.DictReader(source)
        for row in reader:
            client_id = row['client_id']
            if client_id not in clients:
                clients.append(client_id)
    for client in clients:
        print(client)


def main():
    get_messages()
    count_by_shops()
    get_address()
    save_count()
    get_clients()


if __name__ == '__main__':
    main()
