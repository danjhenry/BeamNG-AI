from Inception_net import inception_v3 as googlenet
from ctypes import windll
from PIL import Image
import numpy as np
import requests
import win32api, win32gui, win32ui, win32con
import time
import cv2
import os

monitor_res = (1920, 1080)
window_name = r'BeamNG.drive - 0.13.0.2.6476 - RELEASE - x64'
image_size = (200,150)

WIDTH = 200
HEIGHT = 150
LR = 0.001
MODEL_NAME = 'BeamNG_1.0'
model = googlenet(WIDTH, HEIGHT, 3, LR, output=9, model_name=MODEL_NAME)
model.load('model/{}'.format(MODEL_NAME))

center = (int(monitor_res[0]/2), int(monitor_res[1]/2))

prevkey = ''

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

def keyState(loop, key='P'):
    state = win32api.GetAsyncKeyState(ord(key))
    if(state < 0 or state == 1):
        if loop:
            print('Paused')
            return False
        else:
            print('Resumed')
            return True


def mousemove(handle, pos=center):
    win32api.SetCursorPos(pos)
    
def keypress(key, handle):
    global prevkey
    if prevkey:
        if key != prevkey:
            win32api.SendMessage(handle, win32con.WM_KEYUP, ord(prevkey), None)
            
    win32api.SendMessage(handle, win32con.WM_KEYDOWN, ord(key), None)
    prevkey = key

def noInput(handle):
    global prevkey
    if prevkey:
        win32api.SendMessage(handle, win32con.WM_KEYUP, ord(prevkey), None)
        prevkey = ''

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

def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def Pause_func(loop, key='P'):
    state = win32api.GetAsyncKeyState(ord(key))
    if(state < 0 or state == 1):
        time.sleep(.5)
        if loop:
            print('PAUSED')
            return False
        else:
            print('UNPAUSED')
            return True
    elif loop:
        return True
    else:
        return False


def main():

    runloop = True
    print('Countdown')
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    handle = windowHandle(window_name)

    while True:
        runloop = Pause_func(runloop, key='P')
        while runloop:
            frame = imageCap(handle)
            frame = cv2.resize(frame, image_size)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            prediction = model.predict([frame.reshape(WIDTH,HEIGHT,3)])[0]
            orig = prediction
            prediction = np.array(prediction) * np.array([3.5, 3.5, 0, 0, 2.2, 5, 3.5, 5, 6.5])
            mode_choice = np.argmax(prediction)

            adj = np.round(softmax(orig), 3)
            
            if mode_choice == 0:
                mousepos = center[0] - int(400 * adj[mode_choice])
                mousemove(handle, pos=(mousepos, center[1])) 
                keypress('W', handle)
                choice_picked = 'forward+left'
                
            elif mode_choice == 1:
                mousepos = center[0] + int(400 * adj[mode_choice])
                mousemove(handle, pos=(mousepos, center[1])) 
                keypress('W', handle)
                choice_picked = 'forward+right'
                
            elif mode_choice == 2:
                keypress('AS', handle)
                choice_picked = 'backward+left'
                
            elif mode_choice == 3:
                keypress('DS', handle)
                choice_picked = 'backward+right'
                
            elif mode_choice == 4:
                mousemove(handle)
                keypress('W', handle)
                choice_picked = 'forward'
                
            elif mode_choice == 5:
                mousepos = center[0] - int(400 * adj[mode_choice])
                mousemove(handle, pos=(mousepos, center[1]))
                choice_picked = 'left'

            elif mode_choice == 6:
                mousemove(handle)
                keypress('S', handle)
                choice_picked = 'backward'

            elif mode_choice == 7:
                mousepos = center[0] + int(400 * adj[mode_choice])
                mousemove(handle, pos=(mousepos, center[1]))
                choice_picked = 'right'

            else:
                noInput(handle)
                mousemove(handle)
                choice_picked = 'no input'

            end = np.round(softmax(orig), 3)
            print( '\n',choice_picked, end[mode_choice])
            runloop = Pause_func(runloop, key='P')
    
main()



















        
