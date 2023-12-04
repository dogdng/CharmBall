# Charm Button
提效工具之悬浮球展示系统信息 + 快捷按钮

 1. 启动之后展示为悬浮球，悬浮球显示CPU占用、内存信息和网速，可以通过托盘图标上右键切换显示CPU仪表盘，即CPU逻辑核心的占用情况。这两种视图都支持贴边和自动弹出
 2. 在悬浮球上单击、双击、左键长时间单击和右键的方式分别对应不同的功能。
  - 单击: 展开功能按钮，单击之后，自动变回悬浮球。
  - ~~左键长时间单击，展开功能按钮，不会自动变回悬浮球。~~
  - ~~双击: 自动贴边，靠左或者靠右~~
  - ~~右键：悬浮球自身的菜单~~

## 虚拟环境
激活环境
```
.\.venv\Scripts\Activate.ps1
```
vscode可以在settings.json中配置自动激活环境
## 调试
利用vscode的插件和launch.json调试或者使用pdb
```
python -m pdb main.py
```
## 打包
直接打包成一个exe文件
```
pyinstaller.exe --distpath ./dist --workpath ./build --specpath ./build --clean --onefile --name "fball" --windowed --icon ../resources/CB.ico ./src/main.py -p ./src
```
打包时没有直接使用图片文件，因为在打包之后运行总是找不到图片，绝对路径和相对路径都不行。解决方法是利用convert_base64.py将图片转为base64的字符串存在python源文件中，使用时再转回来。


# 代码

## Windows Manager
管理各个窗口

需要切换窗口时，通过向绑定的槽函数`switch_activate_window`发送切换的信号来实现。

