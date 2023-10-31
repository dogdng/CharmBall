激活环境
```
.\.venv\Scripts\Activate.ps1
```

调试
```
python -m pdb main.py
```

直接打包成exe
```
pyinstaller.exe --distpath ./dist --workpath ./build --specpath ./build --clean --onefile --name "fball" --windowed ./src/main.py -p ./src
```


悬浮球

 1. 启动之后展示为悬浮球
 2. 在悬浮球上单击、双击、左键长时间单击和右键的方式分别对应不同的功能
  - 静态显示cpu占用和内存占用，自动贴边
  - 单击: 展开功能按钮，单击之后，自动变回悬浮球。
  - 左键长时间单击，展开功能按钮，不会自动变回悬浮球。
  - 双击: 自动贴边，靠左或者靠右
  - 右键：悬浮球自身的菜单


## Windows Manager
管理各个窗口

需要切换窗口时，通过向绑定的槽函数`switch_activate_window`发送切换的信号来实现。

