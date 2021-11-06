#!/bin/bash
lockfile=/var/tmp/ETLlock

if ( set -o noclobber; echo "$$" > "$lockfile") 2> /dev/null; then

        trap 'rm -f "$lockfile"; exit $?' INT TERM EXIT

        #changing working dir
        cd /home/etl/einander-helfen/etl/scripts

        # Installing required python packages
        pip3 install -r ../requirements.txt

        # executing crawl and enhancement
        python3 ../main.py

        # package enhanced data for prod
        tar cfvz enhanced_output.tar.gz ../data_enhancement/data ../data_enhancement/output

        # copy packaged data to make it available for nginx endpoint
        cp enhanced_output.tar.gz /var/www/html

        # execute elastic upload
        python3 ../execute_elastic_upload.py

        # clean up after yourself, and release your trap
        rm -f "$lockfile"
        trap - INT TERM EXIT
else
        echo "Lock Exists: $lockfile owned by $(cat $lockfile)"
fi