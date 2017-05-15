#!/usr/bin/env bash

url="http://search.bilibili.com/all?keyword=VOCALOID%E4%B8%AD%E6%96%87%E6%9B%B2&order=click&page="

for num in {1..50}
do
    echo "$url$num"
    curl -s -o page.$num "$url$num"
done
