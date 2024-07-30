# Windows 聚焦壁纸获取脚本

本脚本仅提取长像素为1920以及以上，宽像素为1080以及以上的图片。
如需其他大小的图片，自行对函数的```width```和```height```变量进行修改

## 需要的环境
 - Python 3
 - pip3

## 运行前准备
```shell
pip install pillow
```

## 使用
```shell
cd 到脚本所在目录
```
```shell
python main.py
```
脚本所在目录下的```img```文件夹就是获取到的壁纸。