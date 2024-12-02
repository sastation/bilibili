#!/bin/bash
# 用于下载B站收藏夹中所有视频

favid=$1
uid=$2

folder="./video/Ai"
#folder="./video/test"

usage="$0 {favlist id} {uid}"

if [ "x"$favid == "x" ]; then
    echo "No favid", $usage
    exit -1
fi

if [ "x"$uid == "x" ]; then
    uid="25527367"
fi

url="https://space.bilibili.com/${uid}/favlist?fid=${favid}" 

yt-dlp --write-subs -f "bv*[height<=720]+ba" -o "./${folder}/%(title)s.%(ext)s" \
  --no-mtime --download-archive downfav.list --cookies ./cookie.txt $url

exit 0

