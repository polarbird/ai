#!/usr/bin/env bash

cd /mnt/acs_mnt/nas/polarbird/www/csom
git pull
systemctl restart tomcat7.service
echo '恭喜你！CSOM系统已成功部署。'
