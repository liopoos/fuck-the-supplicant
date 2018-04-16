Status APP版本是一个运行在Mac OS状态栏上的APP。

  

## 截图

![](https://cdn.mayuko.cn/blog/20180416150105.png)



## 外部依赖

使用 `rumps` 构建 ，请先确保已安装 `rumps` 模块：

使用pip，

```
pip install rumps
```

[源代码](https://github.com/jaredks/rumps)，

```
python setup.py install
```

  

## 打包

使用py2app打包，请先确保已安装相应模块：

```shell
pip install py2app
```

安装完模块后执行 `setup.py` 文件:

```python
cd sa
python setup.py py2app
```



## 发行版本

[fuck the supplicant.app](https://github.com/mayuko2012/fuck-the-supplicant/releases/tag/v0.1.1)

   

## 使用

1.运行打包或发行版本的`fuck the supplicant.app`

2.点击偏好设置，编辑配置文件。

![](https://cdn.mayuko.cn/blog/20180416153055.png)

配置文件为json格式，请填写相应字段：

```json
{
　　"re-upset":true,//是否断线重连，默认为是
　　"number":"",//账号
　　"bug_report":"i@mayuko.cn",
　　"host":"219.218.154.250",//远程服务器
　　"version":"0.1.1",
　　"mac_address":"",//mac地址
　　"password":""//密码
}
```

3.重启程序，点击上线

4.享受！



