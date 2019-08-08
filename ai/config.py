#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import os
import yaml


class Config:
    def __init__(self, file_name):
      self.__path = os.path.split(os.path.realpath(__file__))[0]
      self.data = self.read_config(file_name)

    def read_config(self, file_name='config.yaml'):
        path = self.__path + '/../config/' + file_name
        # print(path)
        if os.path.exists(path):
            with open(path, 'rt') as f:
                return yaml.full_load(f.read())
        else:
            print('the input path doesn\'t exist')
