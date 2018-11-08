import sys
from lib.mouse import *

pyautogui.PAUSE = 2.5
os.chdir('D:\OneDrive\Documents\Scripts\Python\PY-NEOBOT-GitHub\lib')


def select_waypoint():  # click on current waypoint in overview by looking for either station or stargate icons
    loopnum = 0  # set a loop number variable to determine how many loops of each imagesearch in total are run
    station_waypoint_icon = pyautogui.locateCenterOnScreen('station_waypoint_icon.png')  # look for station icon
    while station_waypoint_icon is None:
        loopnum = loopnum + 1  # increment loop number by one if icon not found
        print('cant find station_waypoint_icon', loopnum)  # print loop number
        pyautogui.PAUSE = 1  # wait 1 second before rerunning loop
        stargate_waypoint_icon = pyautogui.locateCenterOnScreen('stargate_waypoint_icon.png')  # if station icon not found, look for stargate icon
        if stargate_waypoint_icon is None:
            print('cant find stargate_waypoint_icon', loopnum)
            pyautogui.PAUSE = 1
            select_waypoint()  # if stargate icon not found, repeat loop
        else:
            loopnum = 0  # reset loop number to 0 if icon found
            (stargate_waypoint_iconx, stargate_waypoint_icony) = stargate_waypoint_icon  # separate x and y coordinates of location
            pyautogui.moveTo(stargate_waypoint_iconx, stargate_waypoint_icony, move_time(), mouse_path())  # clicks the center of where the button was found
            click()
            waypointfound = 'stargate'  # tell the function's caller that a stargate was found
            return waypointfound
    else:
        loopnum = 0
        print('found station_waypoint_icon')
        (station_waypoint_iconx, station_waypoint_icony) = station_waypoint_icon
        pyautogui.moveTo(station_waypoint_iconx, station_waypoint_icony, move_time(), mouse_path())  # clicks the center of where the button was found
        click()
        waypointfound = 'station'  # tell the function's caller that a station was found
        return waypointfound


def select_jump_button():  # locate jump button in selection box if stargate icon was found
    jump_button = pyautogui.locateCenterOnScreen('jump_button.png')
    if jump_button is None:
        print('cant find jump_button')
        sys.exit()
    else:
        (jump_buttonx, jump_buttony) = jump_button
        pyautogui.moveTo(jump_buttonx, jump_buttony, move_time(), mouse_path())
        click()
        return


def select_dock_button():  # locate dock button in selection box if station icon was found
    dock_button = pyautogui.locateCenterOnScreen('dock_button.png')
    if dock_button is None:
        print('cant find dock_button')
        sys.exit()
    else:
        (dock_buttonx, dock_buttony) = dock_button
        pyautogui.moveTo(dock_buttonx, dock_buttony, move_time(), mouse_path())
        click()
        return


def detect_dock_or_jump():  # check if client has docked or jumped
    loopnum = 0  # set a loop number variable to determine how many loops of each imagesearch in total are run
    undock_icon = pyautogui.locateCenterOnScreen('undock_icon.png')  # look for undock icon to indicate a dock has been made
    while undock_icon is None:  # if undock icon is not found, look for 'no object selected' in selection box, indicating a jump has been made
        loopnum = loopnum + 1
        print('not docked', loopnum)
        no_object_selected_icon = pyautogui.locateCenterOnScreen('no_object_selected_icon.png')
        if no_object_selected_icon is None:  # if jump is not detected, wait and rerun function
            print('no jump', loopnum)
            pyautogui.PAUSE = 0.5
            detect_dock_or_jump()
        else:
            loopnum = 0  # reset loop number to 0 if icon found
            print('detected jump')
            pyautogui.PAUSE = 1
            (no_object_selected_iconx, no_object_selected_icony) = no_object_selected_icon
            pyautogui.moveTo(no_object_selected_iconx, no_object_selected_icony, move_time(), mouse_path())
            click()
            return
    else:
        loopnum = 0
        print('detected dock!')
        pyautogui.PAUSE = 1
        (undock_iconx, undock_icony) = undock_icon
        pyautogui.moveTo(undock_iconx, undock_icony, move_time(), mouse_path())
        click()
        return