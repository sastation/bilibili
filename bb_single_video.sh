#!/bin/bash
# 用于一首首下载合集中的歌曲

bvid=$1
pages=$2
start=$3
usage="$0 {BVID} {PAGES}"

if [ "x"$bvid == "x" ]; then
    echo "No BVID", $usage
    exit -1
fi

if [ "x"$pages == "x" ]; then
    echo "No Pages", $usage
    exit -1
fi

if [ "x"$start == "x" ]; then
    start=1
fi

echo $bvid, $pages
url="https://www.bilibili.com/video/${bvid}" 

for page in $(seq $start $pages)
do
    echo $page
    you-get -o ./video/经典歌曲 -c cookie.txt --format=dash-flv720-AVC $url/\?p\=$page
done
