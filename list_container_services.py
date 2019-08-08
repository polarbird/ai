#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

import os
import logging
import logging.config

from ai.config import Config
from ai.container_service import ContainerService

path = os.path.split(os.path.realpath(__file__))[0]

# 初始化Logger
logging.config.fileConfig(path + "/logging.conf")
logger = logging.getLogger()

container_service = ContainerService()

def restart_container_service(service_id):
    logger.info('重启' + service_id + '服务开始...')
    if (container_service.restart_service(service_id) is True):
        logger.info('重启' + service_id + '完成。')
    else:
        logger.info('重启' + service_id + '结束。')


# 重启nosql_redis服务
# restart_container_service('nosql_redis')


# 查询容器服务列表
services = container_service.list_services()
logger.info(';'.join(services))
