#!/usr/bin/env bash

export PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin
echo "清理ZLF历史数据开始..."
echo "暂时停止youpin-zlf-queue"
supervisorctl stop youpin-zlf-service-worker:*
cd /mnt/acs_mnt/nas/polarbird/www/youpin-zlf-service
php artisan cache:clear

python3 /mnt/acs_mnt/nas/polarbird/ai/clean_zlf_history_data.py

echo "重新启动youpin-zlf-queue"
supervisorctl start youpin-zlf-service-worker:*

echo "完成清理ZLF历史数据。"
