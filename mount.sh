#!/bin/bash

[[ -d audio ]] || mkdir audio
[[ -d video ]] || mkdir video

sudo mount --bind /mnt/ssd/pan/bilibili/video ./video
sudo mount --bind /mnt/ssd/pan/bilibili/audio ./audio
