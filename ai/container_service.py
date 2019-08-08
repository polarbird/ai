#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>
import json
import os
import yaml
import requests

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import RoaRequest
'''
阿里云容器服务Swarm API接口
https://help.aliyun.com/document_detail/26044.html?spm=a2c4g.11186623.6.875.GmUr5C
'''


class ContainerService:

    __PRODUCT = 'CS'
    __API_VERSION = '2016-02-04'

    def __init__(self):
        self.__path = os.path.split(os.path.realpath(__file__))[0]
        self.__ca = self.__get_full_path('/../certs/ca.pem')
        self.__key = self.__get_full_path('/../certs/key.pem')
        self.__cert = self.__get_full_path('/../certs/cert.pem')
        self.__config_path = self.__get_full_path('/../config/cs.yaml')

        config = self.__get_config()
        self.__cluster_id = config['cs']['cluster_id']
        self.__client = AcsClient(config['cs']['access_key_id'],
                                  config['cs']['access_key_secret'],
                                  config['cs']['region_id'])
        if (config['cs']['master_url'] is None):
            config['cs']['master_url'] = self.__get_master_url()
            self.__save_config(config)
        self.__master_url = config['cs']['master_url']
        if (os.path.isdir(self.__path + '/../certs') is False):
            self.__save_certs()

    def __get_full_path(self, file_name):
        return self.__path + file_name

    def __get_config(self):
        f = open(self.__config_path, encoding='utf-8')
        content = yaml.safe_load(f)
        f.close()
        return content

    def __save_config(self, config):
        f = open(self.__config_path, 'w')
        yaml.dump(config, f, default_flow_style=False)
        f.close()

    def __get_master_url(self):
        request = RoaRequest(self.__PRODUCT, self.__API_VERSION,
                             'GetClusterById')
        request.set_uri_pattern('/clusters/[ClusterId]')
        request.set_method('GET')
        request.add_path_param('ClusterId', self.__cluster_id)
        response = self.__client.do_action_with_exception(request)
        cluster = json.loads(response.decode('utf-8'))
        return cluster['master_url']

    def __get_certs(self):
        request = RoaRequest(self.__PRODUCT, self.__API_VERSION,
                             'GetClusterById')
        request.set_uri_pattern('/clusters/[ClusterId]/certs')
        request.set_method('GET')
        request.add_path_param('ClusterId', self.__cluster_id)
        response = self.__client.do_action_with_exception(request)
        certs = json.loads(response.decode('utf-8'))
        return certs

    def __save_certs(self):
        certs = self.__get_certs()
        os.makedirs(self.__path + '/certs')
        ca_file = open(self.__ca, 'w')
        ca_file.write(certs['ca'])
        ca_file.close()
        cert_file = open(self.__cert, 'w')
        cert_file.write(certs['cert'])
        cert_file.close()
        key_file = open(self.__key, 'w')
        key_file.write(certs['key'])
        key_file.close()

    def list_services(self):
        url = self.__master_url + '/services/'
        response = requests.get(url,
                                verify=self.__ca,
                                cert=(self.__cert, self.__key))
        if (response.ok):
            services = response.json()
            result = []
            for service in services:
                if not service['id'].startswith('acs'):
                    result.append(service['id'])
            return result
        else:
            return False

    def restart_service(self, service_id):
        '''重启服务'''
        url = self.__master_url + '/services/' + service_id + '/restart'
        response = requests.post(url,
                                 verify=self.__ca,
                                 cert=(self.__cert, self.__key))
        if (response.ok):
            return True
        else:
            return False

    def stop_service(self, service_id):
        '''关闭服务'''
        url = self.__master_url + '/services/' + service_id + '/stop'
        response = requests.post(url,
                                 verify=self.__ca,
                                 cert=(self.__cert, self.__key))
        if (response.ok):
            return True
        else:
            return False

    def start_service(self, service_id):
        '''启动服务'''
        url = self.__master_url + '/services/' + service_id + '/start'
        response = requests.post(url,
                                 verify=self.__ca,
                                 cert=(self.__cert, self.__key))
        if (response.ok):
            return True
        else:
            return False
