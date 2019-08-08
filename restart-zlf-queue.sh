#!/usr/bin/env bash

export PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin
echo "Restart youpin-zlf-queue started..."
cd /mnt/acs_mnt/nas/polarbird/www/youpin-zlf-service
php artisan cache:clear
supervisorctl restart youpin-zlf-service-worker:*
echo "Restart youpin-zlf-queue finished."

