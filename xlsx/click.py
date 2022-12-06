import sys
import time

import keyboard
import pyautogui

print('把鼠标移动到需要的位置，5秒后会获取坐标')
print('Move the mouse to the desired position, and the coordinates will be obtained after 5 seconds')
i = 1
for i in range(6):
    print(i)
    time.sleep(1)
p = pyautogui.position()
print('按下空格停止')
print('Press space to stop')
while True:
    flag = False


    def key_press(key):
        global flag
        if key.name == 'space':
            flag = True


    keyboard.on_press(key_press)
    pyautogui.click(p)
    time.sleep(1)
    if flag:
        flag = False
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        sys.exit()
