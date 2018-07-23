import win32api, win32gui, win32ui
from random import shuffle
from ctypes import windll
from PIL import Image
import numpy as np
import win32api
import time
import cv2
import os

image_size = (200,150)
window_name = r'BeamNG.drive - 0.13.0.1.6460 - RELEASE - x64'
action = {
    'AW': [1, 0, 0, 0, 0, 0, 0, 0, 0],
    'DW': [0, 1, 0, 0, 0, 0, 0, 0, 0],
    'AS': [0, 0, 1, 0, 0, 0, 0, 0, 0],
    'DS': [0, 0, 0, 1, 0, 0, 0, 0, 0],
    'W' : [0, 0, 0, 0, 1, 0, 0, 0, 0],
    'A' : [0, 0, 0, 0, 0, 1, 0, 0, 0],
    'S' : [0, 0, 0, 0, 0, 0, 1, 0, 0],
    'D' : [0, 0, 0, 0, 0, 0, 0, 1, 0],
    'NA': [0, 0, 0, 0, 0, 0, 0, 0, 1]
    }

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

def keyState(keys='WASD'):
    keys_on = []
    for key in keys:
        state = win32api.GetAsyncKeyState(ord(key))
        if(state < 0 or state == 1):
            keys_on.append(key)
    return keys_on

def save_file(imgs, num):
    #imgs = list(filter(lambda a: a[1] != NA, imgs))
    shuffle(imgs)
    np.save('data/training_data-{}.npy'.format(num), imgs)
        
def main():
    training_data = list()
    file_num = 1
    
    while True:
        file_name = 'data/training_data-{}.npy'.format(file_num)

        if os.path.isfile(file_name):
            print('File exists, moving along', file_num)
            file_num += 1
        else:
            print('Starting at {}.'.format(file_num))
            break
        
    for x in range(5)[::-1]:
        print(x)
        time.sleep(1)

    handle = windowHandle(window_name)

    while True:
        keys_on = keyState()
        frame = imageCap(handle)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, image_size)
        
        if keys_on:
            keys_on.sort()
            keys_on = ''.join(keys_on)
            if keys_on in action:
                print(keys_on)
                output = action[keys_on]
                training_data.append([frame, output])
                if len(training_data) >= 4000:
                    print('starting save')
                    save_file(training_data, file_num)
                    file_num += 1
                    training_data  = list()
                    print('saved')
        else:
            print('NA')
            output = action['NA']
            training_data.append([frame, output])

main()
