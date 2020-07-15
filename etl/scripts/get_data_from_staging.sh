#!/bin/bash
# change working dir
cd /home/etl

# remove old data
rm -r staging_data

# make data dir
mkdir staging_data

# switch dir
cd staging_data

# remove old data file
rm enhanced_output.tar.gz

# get new file from staging
wget -4 http://cai-einander-helfen-staging.fbi.h-da.de/enhanced_output.tar.gz

# extract data from folder
tar xfvz enhanced_output.tar.gz

# delete old data
rm -r /home/etl/einander-helfen/etl/data_enhancement/data
rm -r /home/etl/einander-helfen/etl/data_enhancement/output

# move data to data_exraction folder
cp -r data_enhancement/data /home/etl/einander-helfen/etl/data_enhancement
cp -r data_enhancement/output /home/etl/einander-helfen/etl/data_enhancement
