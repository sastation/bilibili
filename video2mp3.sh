#!/bin/bash

f_process() {
    # 提取视频文件中的音频，平滑后转成MP3存放
    in_file=$1

    out_file=`echo $in_file | sed "s/&/-/g" | sed "s/\.mp4//g"`
    echo "$in_file ===> $out_file"

    # 将音频转换成mp3并平滑音量
    ffmpeg -i "$in_file" -vn -f mp3 -af "loudnorm=i=-14" "$out_file.mp3"
}


# Main, 找出7天内生成的MP4文件，提取音频平滑音量
IFS=$'\n'
for in_file in `find . -ctime -7 -name "*.mp4"`
do
  f_process "$in_file"
done


exit 0


#find . -ctime -7 -name "*.mp4" | while read file; do f_process "$file"; done
# mv *.mp3 ../../audio/Ai
