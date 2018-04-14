# Fuck The Supplicant

This is a third-party Amrand Client Network Authentication Clients based on Python, support `BAS` authentication, socks code references [lyq1996](https://github.com/lyq1996/).

Currently tested in the Yantai University network environment, other school may need to modify the **host IP**.

  

## Screenshots

![](https://cdn.mayuko.cn/blog/20180413210739.png)

![](https://cdn.mayuko.cn/blog/20180413210957.png)



## Support

- Windows (pass the test on the Windows 10)
- Mac OS (pass the test on the Mac OS 10.3)
- Linux (GHOME)


  


## Required

- Python2.7 (if you want to make a release do  yourself)


Use the wxPython module to build the UI, If you need preview, please install the module first：

```shell 
pip install wxPython
```

  


## Package

Please make sure you have the following modules: `py2exe`(Windows) or `py2app`(Mac OS) first:

```shell
pip install py2exe
```

Windows device executes `creat_gui_windows.py` file, Mac device executes `creat_gui_mac.py` file:

```python
cd fuckthesupplicant
python creat_gui_windows.py py2exe
```

For more information please visit the [py2exe official website](http://www.py2exe.org/).



## Release

- Windows: [fuck-the supplicant.exe](https://github.com/mayuko2012/fuck-the-supplicant/releases/tag/v0.1.1)
- Mac OS: None

  

## License

MIT.