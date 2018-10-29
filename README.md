# 东南大学课程表导出工具

本工具可获取东南大学的各学期的课程表、物理实验、考试日程等信息，并作为 ics 文件导出，方便导入至 Windows、macOS、iOS、Android 等各平台的自带日历或其它日历软件中。

> 注意：本工具需要使用东南大学统一身份认证，只能用于在校学生导出自己本人的课表。

## 安装与配置
1. 下载并安装 **[Python 3](https://www.python.org/downloads/)**；
2. 确认 Python 版本，请在命令行中输入（请注意这里 -V 是大写）：
```command
python -V
```
若返回的是 Python 2 版本号，你可能需要输入：
```command
python3 -V
```
3. 安装 Python Requests 插件：
+ 对于 Windows，在**以管理员权限运行**的命令提示符中输入：
```command
pip install requests
```
+ 对于 macOS 或 Linux，在终端中输入：
```command
sudo pip install requests
```
> 注意：若在第 2 步中你使用的是 `python3`，这里相应地需要使用 `pip3`。
4. 在 **[Release](https://github.com/NN708/SEU-Curriculum-Export/releases)** 中下载本工具的最新版本源代码，解压到本地目录中。

## 运行本工具
1. 在命令行中切换到上一步解压出的路径：
+ 对于 Windows，打开命令提示符，先输入 `C:`、`D:`、`E:` 等切换到文件所在的驱动器，之后使用 `cd` 命令切换到正确的路径；
+ 对于 macOS 或 Linux，打开终端，使用 `cd` 命令切换到正确的路径；
2. 在命令行中输入以下命令运行本工具：
```command
python curriculum.py
```
也可能是
```command
python3 curriculum.py
```
3. 根据程序提示，输入东南大学一卡通号、统一身份认证密码、你想要导出的学期以及是否导出近期物理实验或考试；
4. 当程序提示“已导出为 curriculum.ics”时，说明导出成功，你可以在程序的同一目录中找到导出的 ics 文件。

## 导入到日历
### Windows
右键导出的 ics 文件，选择使用 Windows 10 自带的日历软件打开，点击“添加到日历”即可。

### macOS
打开 macOS 自带的日历软件，点击“文件”->“导入”，选择导出的 ics 文件，点击“导入”即可。

### iOS
将导出的 ics 文件发送到你的邮箱，在 iOS 自带的邮件应用中登录你的邮箱，找到该邮件并打开附件中的 ics 文件，点击“添加全部”即可。

### Android 或其它日历软件
具体方法请查看日历软件的帮助文档。

---

特别感谢 [@WhatTheNathan](https://github.com/WhatTheNathan) 和 [@HeraldStudio](https://github.com/HeraldStudio) 提供的 API 接口。