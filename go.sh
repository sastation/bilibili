#!/usr/bin/env bash

cd /home/zwang/coding/github/bilibili/data

dtm=$(date +"%y%m%d")

../vc_list_data.py > "vc.list-$dtm"
../vc_list_palace.py > palace.list
../vc_list_ranking.py > ranking.list


# collect data into sqlite db
cd /home/zwang/coding/github/bilibili/
./vc_db.py -u > vc_db.log 2>&1
