激活环境
```
.\.venv\Scripts\Activate.ps1
```

生成requirements.txt
```
pip3 freeze > requirements.txt
```

https://blog.csdn.net/weixin_44446598/article/details/115031335

悬浮球

 1. 启动之后展示为悬浮球
 2. 在悬浮球上单击、双击、左键长时间单击和右键的方式分别对应不同的功能
  - 静态显示cpu占用和内存占用，自动贴边
  - 单击: 展开功能按钮，单击之后或者失去焦点，自动变回悬浮球。
  - 左键长时间单击，同单击按钮，不会自动变回悬浮球。
  - 双击: 自动贴边
  - 右键