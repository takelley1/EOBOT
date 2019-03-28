import sys
import time
import random

import pyautogui as pag

from lib import mouse
from lib import keyboard
from lib import docked

sys.setrecursionlimit(9999999)
conf = 0.95


def drag_items_from_hold():
    # Click and drag all items from ship inventory to station hangar.
    namefield_station_hangar_icon = pag.locateCenterOnScreen(
        './img/namefield_station_hangar.bmp',
        confidence = conf)
    (namefield_station_hangar_iconx,
     namefield_station_hangar_icony) = namefield_station_hangar_icon
    pag.moveTo((namefield_station_hangar_iconx + (random.randint(-5, 250))),
               (namefield_station_hangar_icony + (random.randint(10, 25))),
               mouse.move_time(), mouse.mouse_path())
    pag.mouseDown()
    station_hangar = pag.locateCenterOnScreen('./img/station_hangar.bmp',
                                              confidence = conf)
    (station_hangarx, station_hangary) = station_hangar
    pag.moveTo((station_hangarx + (random.randint(-15, 60))),
               (station_hangary + (random.randint(-10, 10))),
               mouse.move_time(), mouse.mouse_path())
    pag.mouseUp()
    print('drag_items_from_hold -- moved all item stacks from hold')
    return


def unload_ship():
    print('unload_ship -- began unloading procedure')
    docked.open_cargo_hold()
    specialhold = docked.look_for_special_hold()
    items = docked.look_for_items()
    if docked.look_for_items() == 0:
        docked.look_for_special_hold()
        if specialhold == 1:
            # Wait between 0 and 2s before actions for increased randomness.
            time.sleep(float(random.randint(0, 2000)) / 1000)
            docked.open_special_hold()
            items = docked.look_for_items()
            while items == 1:
                time.sleep(float(random.randint(0, 2000)) / 1000)
                docked.focus_inventory_window()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                keyboard.select_all()
                time.sleep(float(random.randint(0, 2000)) / 1000)
                drag_items_from_hold()
                time.sleep(2)
                docked.look_for_items()
                print('unload_ship -- finished unloading procedure')
                return 1
            if items == 0:
                print('unload_ship -- finished unloading procedure')
                return 1
        elif specialhold == 0:
            print('unload_ship -- nothing to unload')
            return 1
    while items == 1:
        docked.focus_inventory_window()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        keyboard.select_all()
        time.sleep(float(random.randint(0, 2000)) / 1000)
        drag_items_from_hold()
        time.sleep(2)
        docked.look_for_special_hold()
        items = docked.look_for_items()
    if specialhold == 1:
        docked.open_special_hold()
        items = docked.look_for_items()
        while items == 1:
            docked.focus_inventory_window()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            keyboard.select_all()
            time.sleep(float(random.randint(0, 2000)) / 1000)
            drag_items_from_hold()
            time.sleep(2)
            docked.look_for_items()
            print('unload_ship -- finished unloading procedure')
            return 1
    elif specialhold == 0:
        print('unload_ship -- finished unloading procedure')
        return 1
