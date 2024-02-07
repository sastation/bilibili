# bilibili
> analyze bilibili.com data

## update you-get
```bash
sudo su -
pip3 install --upgrade you-get
```

## 修改 you-get Version:version 0.4.1650
- 无法访问bilibili接口
    - 文件：`lib/python3.8/site-packages/you_get/extractors/bilibili.py`
    - 101行：return 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    - 修改为：return 'https://api.bilibili.com/x/player/wbi/v2?%s&sign=%s' % (params, chksum)
- 文件名最长为80修改为256
    - 文件为：`lib/python3.8/site-packages/you_get/util/fs.py`
    - 倒数第二行: text = text[:80] # Trim to 82 Unicode characters long
    - 修改为:     text = text[:255] # Trim to 256 Unicode characters long


## 获得收藏夹中的内容
- `bb_favorite.py`
    -l, --list, 列出收藏夹名称与对应的mid
    -f, --folder, 收藏夹名称
    -d, --download, 下载选项，若无则为查看

```bash
# 查看
./bb_favorite.py -f VC.02

## 下载
./bb_favorite.py -f VC.02 -d
```

## 将视频转为MP3
```bash
# 转换后的MP3将生成在视频目录中
./bb_mp3.py -p ./video/favorite/VC.01
```

## 对MP3文件进行整理
`./mp3_rename.sh`
1. 从()中提取
2. 从《》中提取

## 下载单个视频中的所有子视频
`./bb_single.sh`, 需要提供视频URL，并指定起始数字

## 将弹幕由xml转换为ass
```bash
./bb_menu.py -p video/Vsinger.Live.2017 -e video/danmaku2ass/
# -p: 视频目录
# -e: danmaku2ass 程序目录
```

## 获取排名前1000的Vocaloid中文曲数据并存入数据库vc.db
`./vc_update.py`

## 下载 vc.db 中播放数超过10万的视频，下载后标记为已完成
`./vc_download.py`
