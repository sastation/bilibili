# bilibili
> analyze bilibili.com data

## update you-get
```bash
sudo su -
pip3 install --upgrade you-get
```

## 获得收藏夹中的内容
- bb_favorite.py
    -m, --mid, 用户空间编号，默认为 25527367/推车老牛
    -t, --title, 收藏夹名称，默认为 VC.01
    -v, --view, 查看 (若无此项则为下载)

```bash
# 查看
./bb_favorite.py -v -t VC.02

## 下载
./bb_favorite.py -t VC.02
```

## 将视频转为MP3
```bash
# 转换后的MP3将生成在视频目录中
./bb_mp3.py -p ./video/favorite/VC.01
```

## 将弹幕由xml转换为ass
```bash
./bb_menu.py -p video/Vsinger.Live.2017 -e video/danmaku2ass/
# -p: 视频目录
# -e: danmaku2ass 程序目录
```
