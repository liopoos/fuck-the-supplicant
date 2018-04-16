GUI版本提供了简单的可视化界面。

  

## 截图

![](https://cdn.mayuko.cn/blog/20180413210739.png)

![](https://cdn.mayuko.cn/blog/20180413210957.png)

  

## 外部依赖

使用 `wxPython` 构建 GUI 界面，请先确保已安装 `wxPython` 模块：

```shell 
pip install wxPython
```

​    

## 打包

使用 py2exe（Windows）或 py2app（Mac OS）打包，请先确保已安装相应模块：

```shell
pip install py2exe
```

Windows 设备请执行 `creat_gui_windows.py` 文件，Mac 设备请执行 `creat_gui_mac.py` 文件:

```python
cd gui
python creat_gui_windows.py py2exe
```

更多信息请查看[py2exe](http://www.py2exe.org/)官方网站。



## 发行版本

- Windows： [fuck-the supplicant.exe](https://github.com/mayuko2012/fuck-the-supplicant/releases/tag/v0.1.1)
- Mac OS：None