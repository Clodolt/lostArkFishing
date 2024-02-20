import pyautogui
#import cv2
import random
import time
import numpy as np
from pathlib import Path

class screen:
    weight = 2560
    height = 1440
    rect = ((int(weight * 0.47), int(height * 0.36)), (int(weight * 0.47 + weight * 0.0625), int(height * 0.36 + height * 0.178)))

debug=False

# tamplates
#1210,520-145,240
time.sleep(2)
fishing_key="R"

def detect_exclamation_mark():
    image = pyautogui.screenshot(
        region=(screen.weight * 0.47, screen.height * 0.36, screen.weight * 0.0625, screen.height * 0.178))
    # image=Image.open("1.png")
    # image.show()
    arr = np.array(image)  # 1203,518-1403,718  160*255
    mark_pixels = 0
    swimmer_pixels = 0
    r = 0
    g = 1
    b = 2
    for x in arr:
        for y in x:
            if 190 < y[r] and 160 < y[g] < 230 and y[b] < 200:
                mark_pixels += 1
            if 100 < y[r] and y[g] < 100 and y[b] < 200:
                swimmer_pixels+=1

    if mark_pixels>200 and swimmer_pixels < 70:
        return True,mark_pixels,image,swimmer_pixels
    else: return False, mark_pixels,image,swimmer_pixels

temp=Path("temp")
t=temp.joinpath("True")
f=temp.joinpath("False")
if debug:
    temp.mkdir(exist_ok=True)
    t.mkdir(exist_ok=True)
    f.mkdir(exist_ok=True)
switch=True
index=0
last_fish=time.time()

def loop():
    global switch
    global rod_is_out
    global last_fish
    if switch:
        folder=t
    else:
        folder=f
    if not rod_is_out:
        print(time.strftime("%H:%M:%S", time.gmtime()), "throwing a fishing rod")
        pyautogui.press(fishing_key,interval=random.uniform(0.05,0.1))
        rod_is_out=True
        time.sleep(5)

    res,val,image,swimmer=detect_exclamation_mark()
    global index
    if debug:
        image.save(folder.joinpath(str(index) + "-" + str(val)+"-"+str(swimmer) + ".jpg").open("wb")) #DEBUG
    index += 1

    # either press w or loop again
    if res:
        switch = not switch
        if switch:
            l = t
        else:
            l = f
        if debug:
            for file in l.iterdir():
                file.unlink()
                index = 0
        time.sleep(0.1)
        print(time.strftime("%H:%M:%S", time.gmtime()), "Time to fish!")
        #collect fish
        pyautogui.press(fishing_key, interval=random.uniform(0.05, 0.1))
        rod_is_out=False
        #wait for rod to be retrieved
        time.sleep(random.uniform(6.0,8.0))
        last_fish=time.time()

    if time.time()-last_fish>40:
        last_fish=time.time()
        print("reset rod")
        rod_is_out=False



rod_is_out=False
while True:
    starttime = time.time()
    loop()
    time.sleep(0.05)
