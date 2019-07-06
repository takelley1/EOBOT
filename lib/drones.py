import random
import time

import pyautogui as pag

drones = 2

drones_dict = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}


def launch_drones():
    # User must custom-set the "launch drones" hotkey to be Shift-l
    if drones != 0:
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('l')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('l')
        time.sleep(float(random.randint(300, 800)) / 1000)

    # Wait for drones to launch by looking for '0' in drone bay
    drones_launched_var = pag.locateOnScreen(
        './img/indicators/drones/0_drone_in_bay.bmp')
    tries = 0
    while drones_launched_var is None and tries <= 25:
        time.sleep(float(random.randint(500, 2000)) / 1000)
        drones_launched_var = pag.locateOnScreen(
            './img/indicators/drones/0_drone_in_bay.bmp')
        tries += 1
    if drones_launched_var is not None and tries <= 25:
        print('launch_drones -- drones launched')
        return 1
    else:
        print('launch_drones -- timed out waiting for drones to launch')
        return 1


def drones_launched():
    drones_launched_var = pag.locateOnScreen(
        './img/indicators/drones/0_drone_in_bay.bmp')
    if drones_launched_var is not None:
        print('drones_launched -- drones are in space')
        return 1
    else:
        return 0


def recall_drones():
    if drones != 0:
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyDown('r')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('shift')
        time.sleep(float(random.randint(10, 800)) / 1000)
        pag.keyUp('r')

        # Wait for all drones to return to drone bay.
        drones_recalled = pag.locateOnScreen('./img/indicators/drones/' + (
            drones_dict[drones]) + '_drone_in_bay.bmp')
        tries = 1
        while drones_recalled is None and tries <= 25:
            time.sleep(float(random.randint(1000, 2000)) / 1000)
            drones_recalled = pag.locateOnScreen('./img/indicators/drones/' + (
                drones_dict[drones]) + '_drone_in_bay.bmp')
            tries += 1
        if drones_recalled is not None and tries <= 25:
            print('recall_drones -- drones returned to bay')
            return 1
        else:
            print('recall_drones -- timed out waiting for drones to return')
            return 1
    else:
        return 0
