#!/bin/bash
#changing working dir
cd /home/etl/einander-helfen/etl/scripts

# Installing required python packages
pip3 install -r ../requirements.txt

# execute elastic upload
python3 ../execute_elastic_upload.py

# executing crawl and enhancement
python3 ../main.py

# package enhanced data for prod
tar cfvz enhanced_output.tar.gz ../data_enhancement/data ../data_enhancement/output

# copy packaged data to make it available for nginx endpoint
cp enhanced_output.tar.gz /var/www/html
