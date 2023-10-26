# -*- coding: utf-8 -*-

import base64, os

def main():

    pics = [
        "closemenu.png",
        "CB.ico",
        "mission.png",
        "screen.png",
        "desktop.png"
        ]
    for i in pics:
        pic2py(i)
    print("ok")

def pic2py(picture_name: str):
    """
    将图像文件转换为py文件
    """
    path = os.path.abspath("resources")
    open_pic = open(os.path.join(path, picture_name), 'rb')
    b64str = base64.b64encode(open_pic.read())
    open_pic.close()
    write_data = f"img = {b64str}"
    path = os.path.join(path, "../src/images")
    f = open(f"{os.path.join(path, picture_name.replace('.', '_'))}.py", 'w+')
    f.write(write_data)
    f.close()

if __name__ == '__main__':
    print(os.path.abspath("."))
    main()