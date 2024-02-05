#!/bin/bash
# 用于一首首下载合集中的歌曲

#url="https://www.bilibili.com/video/BV1us411X76M" # pages: 353, {欧美必听&循环}那些我们单曲循环无数次的欧美歌曲
url="https://www.bilibili.com/video/BV1QX4y1d7tr" # pages: 200, 【欧美流行音乐】全站最全英文歌曲合集！好听到骨子里的英文歌曲！

for page in {55..200}
do
    echo $page
    you-get -o ./video/经典歌曲 -c cookie.txt --format=dash-flv720 $url/\?p\=$page
done
