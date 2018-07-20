from Inception_net import inception_v3 as googlenet
from ctypes import windll
from PIL import Image
import numpy as np
import requests
import win32api, win32gui, win32ui, win32con
import time
import cv2
import os

window_name = r'BeamNG.drive - 0.13.0.0.6437 - RELEASE - x64'
image_size = (200,150)

WIDTH = 200
HEIGHT = 150
LR = 0.001
MODEL_NAME = 'BeamNG_0.1'
model = googlenet(WIDTH, HEIGHT, 3, LR, output=8, model_name=MODEL_NAME)
model.load('model/{}'.format(MODEL_NAME))

keysOn = set()

def windowHandle(name):
    while True:
        try:
            handle = win32gui.FindWindow(None, name)
            print('Handle: ', handle)
            break
        except:
            print('ERROR: could not find handle.')
            time.sleep(5)
    return handle

'''

def keypress(keys, handle):
    print(keys)
    for key in keys:
        win32api.PostMessage(handle, win32con.WM_KEYDOWN, ord(key), None)
        time.sleep(.1)
        
    for key in keys:
        win32api.PostMessage(handle, win32con.WM_KEYUP, ord(key), None)
        time.sleep(.1)
'''


def turn(keys, handle):
    keys.append('S')
    for key in keys:
        win32api.SendMessage(handle, win32con.WM_KEYDOWN, ord(key), None)
        time.sleep(.12)
        win32api.SendMessage(handle, win32con.WM_KEYUP, ord(key), None)


def keypress(keys, handle):
    global keysOn
    for key in keys:
        if key in keysOn:
            keysOn.remove(key)
        win32api.SendMessage(handle, win32con.WM_KEYDOWN, ord(key), None)
        
    if keysOn:
        for key in keysOn:
            print('stop ', key)
            win32api.SendMessage(handle, win32con.WM_KEYUP, ord(key), None)

    keysOn = set(keys)

        

def imageCap(handle):
    left, top, right, bot = win32gui.GetWindowRect(handle)
    w = right - left
    h = bot - top
    hwndDC = win32gui.GetWindowDC(handle)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    PW_RENDERFULLCONTENT = 2
    result = windll.user32.PrintWindow(handle, saveDC.GetSafeHdc(), PW_RENDERFULLCONTENT)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    image = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(handle, hwndDC)
    if result == 1:
        return np.array(image)

def main():
    
    print('Countdown')
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    handle = windowHandle(window_name)
    
    while True:
        frame = imageCap(handle)
        frame = cv2.resize(frame, image_size)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        prediction = model.predict([frame.reshape(WIDTH,HEIGHT,3)])[0]
        #np.array([4.5, 0.1, 0.1, 0.1,  1.8, 1.8, 0.5, 0.5])
        prediction = np.array(prediction) * np.array([ 2.4, 2.2, 0.5, 0.5, 3.5, 0.1, 0.1, 0.1])
        mode_choice = np.argmax(prediction)
        
        if mode_choice == 0:
            turn(['A'], handle)
            choice_picked = 'forward+left'
            
        elif mode_choice == 1:
            turn(['D'], handle)
            choice_picked = 'forward+right'
            
        elif mode_choice == 2:
            keypress(['S', 'A'], handle)
            choice_picked = 'reverse+left'
            
        elif mode_choice == 3:
            keypress(['S', 'D'], handle)
            choice_picked = 'reverse+right'
            
        elif mode_choice == 4:
            keypress(['W'], handle)
            choice_picked = 'forward'
            
        elif mode_choice == 5:
            keypress(['S'], handle)
            choice_picked = 'reverse'
            
        elif mode_choice == 6:
            keypress(['A'], handle)
            choice_picked = 'left'
            
        elif mode_choice == 7:
            keypress(['D'], handle)
            choice_picked = 'right'

        print(choice_picked)

main()



















        
