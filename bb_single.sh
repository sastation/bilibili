#!/bin/bash
# 用于下载合集中所有的视频或音频

ftype=$1
bvid=$2

usage="$0 {video|audio} {BVID} "

if [ "x"$bvid == "x" ]; then
    echo "No BVID", $usage
    exit -1
fi

url="https://www.bilibili.com/video/${bvid}" 

if [ "x"$ftype == "xaudio" ]; then
    folder="./audio"
    yt-dlp -x -o "./${folder}/%(title)s.%(ext)s" --cookies ./cookie.txt $url

else
    folder="./video"
    yt-dlp --write-subs -f "bv*[height<=720]+ba" -o "./${folder}/%(title)s.%(ext)s" \
	  --cookies ./cookie.txt $url
fi


exit 0

