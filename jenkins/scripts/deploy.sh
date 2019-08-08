#!/usr/bin/env sh

echo 'Deploy to production'

rm -rf /home/ai
mkdir /home/ai
cp -rf ./ /home/ai
cp -rf /home/conf.d/ai/* /home/ai
rm -rf /home/ai/.git
rm -rf /home/ai/.gitignore
rm -rf /home/ai/Jenkinsfile
rm -rf /home/ai/jenkins

chmod +x /home/ai/*.sh
