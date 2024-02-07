#!/bin/bash


from_bracket() {
    # 从()中提取歌名
    IFS=$'\n'
    for in_file in `ls *mp3`
    do
        #out_file=`echo $in_file | awk -F"\(P[0-9]+\. " '{print $2}' | awk -F"\)\.mp3" '{print $1".mp3"}'`
        out_file=`echo $in_file | grep -Eo "P[0-9]+.*" | sed -E 's/\)\.mp3/\.mp3/g'`
        mv "$in_file" "$out_file"
    done
}

from_book() {
    # 从《》中提取歌名
    IFS=$'\n'
    for in_file in `ls *mp3`
    do
        p_str=`echo $in_file | grep -Eo "P[0-9]+"`
        n_str=`echo $in_file | grep -Eo "《.*》" | sed "s/《\(.*\)》/\1/g"`
        if [ "x"$n_str == "x" ]; then
            out_file=$in_file
        else
            out_file="$p_str. $n_str.mp3"
            mv "$in_file" "$out_file"
        fi
    done
}


# Main
from_bracket

exit 0
