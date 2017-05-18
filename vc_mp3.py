#!/usr/bin/env python
''' use ffmpeg to convert mp4|flv to mp3 '''

import os
import glob
import subprocess

def convert_mp3(file):
    new_file = os.path.splitext(os.path.split(file)[1])[0]
    cmd = 'ffmpeg -n -i "%s" -f mp3 -vn "%s"' % (file.strip(), new_file+".mp3")
    
    if not os.path.isfile(new_file+".mp3"): 
        cmd = subprocess.call(cmd, shell=True)
        if cmd:
            status = 'wrong'
        else:
            status = 'good'
    else:
        status = 'exist'

    print 'convert %s to mp3 is %s' % (file.strip(), status)
    return 0



if __name__ == '__main__':
    print "Main"
    lines = glob.glob("*.flv")
    lines.extend(glob.glob("*.mp4"))

    for line in lines:
        convert_mp3(line)
