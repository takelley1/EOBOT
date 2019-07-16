import time
import random
import sys
import logging
import pyautogui as pag
from lib import mouse, keyboard
from lib.vars import originx, originy, windowx, windowy, conf

logging.basicConfig(format='(%(levelno)s) %(asctime)s - %(funcName)s -- %('
                           'message)s', level=logging.DEBUG)


def docked_check():
    """Check if the ship is currently docked by looking for the undock_loop
     icon."""
    undock_icon = pag.locateCenterOnScreen('./img/buttons/undock.bmp',
                                           confidence=conf,
                                           region=(originx, originy,
                                                   windowx, windowy))
    if undock_icon is None:
        logging.debug('not docked')
        return 0
    elif undock_icon is not None:
        logging.debug('docked')
        return 1


def open_ship_inv():
    """Click on the ship's inventory button in the inventory window while
    docked."""
    logging.debug('opening ship inventory')
    tries = 1
    ship_inv = pag.locateCenterOnScreen('./img/buttons/ship_inv.bmp',
                                        confidence=conf,
                                        region=(originx, originy,
                                                windowx, windowy))
    while ship_inv is None and tries <= 25:
        logging.error('cannot find ship inventory')
        tries += 1
        ship_inv = pag.locateCenterOnScreen('./img/buttons/ship_inv.bmp',
                                            confidence=conf,
                                            region=(originx, originy,
                                                    windowx, windowy))
        time.sleep(1)
    if ship_inv is not None and tries <= 25:
        (ship_invx, ship_invy) = ship_inv
        pag.moveTo((ship_invx + (random.randint(-4, 50))),
                   (ship_invy + (random.randint(-6, 6))),
                   mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        return 0


def open_spec_inv_ore():
    """If a special inventory was found (for ore, minerals, planetary
    products etc.) click on it in inventory window while docked."""
    logging.debug('opening special inventory')
    tries = 0
    spec_inv_ore = pag.locateCenterOnScreen('./img/buttons/spec_inv_ore.bmp',
                                            confidence=conf,
                                            region=(originx, originy,
                                                    windowx, windowy))
    while spec_inv_ore is None and tries <= 25:
        logging.error('cannot find special hold')
        tries += 1
        spec_inv_ore = pag.locateCenterOnScreen(
            './img/buttons/spec_inv_ore.bmp',
            confidence=conf,
            region=(originx, originy,
                    windowx, windowy))
        time.sleep(1)
    if spec_inv_ore is not None and tries <= 25:
        (spec_invx, spec_invy) = spec_inv_ore
        pag.moveTo((spec_invx + (random.randint(-4, 50))),
                   (spec_invy + (random.randint(-3, 3))),
                   mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        return 0


def open_station_inv():
    """Click on the station inventory button within the main inventory window
    while docked."""
    logging.debug('opening station inventory')
    tries = 0
    station_inv = pag.locateCenterOnScreen('./img/buttons/station_inv.bmp',
                                           confidence=conf,
                                           region=(originx, originy,
                                                   windowx, windowy))
    while station_inv is None and tries <= 25:
        logging.error('cannot find station inventory icon')
        tries += 1
        station_inv = pag.locateCenterOnScreen('./img/buttons/station_inv.bmp',
                                               confidence=conf,
                                               region=(originx, originy,
                                                       windowx, windowy))
        time.sleep(1)
    if station_inv is not None and tries <= 25:
        (station_inv, station_invy) = station_inv
        pag.moveTo((station_inv + (random.randint(-6, 50))),
                   (station_invy + (random.randint(-6, 6))),
                   mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        return 0


def focus_inv_window():
    """Click somewhere inside the station inventory window to focus it before
    any items are selected. Look for the sorting buttons in top right corner
    of the inventory window and position the mouse cursor relative to those
    buttons to click a non-interactive area within the inventory window."""
    tries = 0
    sort_station_inv = pag.locateCenterOnScreen(
        './img/buttons/station_sorting.bmp',
        confidence=conf,
        region=(originx, originy, windowx, windowy))

    while sort_station_inv is None and tries <= 25:
        logging.error('cannot find sorting icon')
        tries += 1
        sort_station_inv = pag.locateCenterOnScreen(
            './img/buttons/station_sorting.bmp',
            confidence=conf,
            region=(originx, originy, windowx, windowy))
        time.sleep(1)
    if sort_station_inv is not None and tries <= 25:
        (sort_station_invx,
         sort_station_invy) = sort_station_inv
        pag.moveTo((sort_station_invx - (random.randint(0, 250))),
                   (sort_station_invy + (random.randint(50, 300))),
                   mouse.duration(), mouse.path())
        mouse.click()
        return 1
    else:
        return 0


def detect_items():
    """Look at the bottom-right corner of the station inventory window for the
    '0 items found' text. If it isn't present, there must be items in the
    station's inventory."""
    global no_items_station_inv
    no_items_station_inv = pag.locateOnScreen(
        './img/indicators/station_inv_0_items.bmp',
        confidence=.9,
        region=(originx, originy, windowx, windowy))

    if no_items_station_inv is None:
        logging.debug('items remain')
        return 1
    elif no_items_station_inv is not None:
        logging.debug('no more items')
        return 0


def detect_spec_inv():
    """Look for different kinds of special inventory locations on your ship."""
    no_additional_invs = pag.locateCenterOnScreen(
        './img/indicators/no_additional_bays.bmp',
        confidence=conf, region=(originx, originy, windowx, windowy))

    spec_inv_ore = pag.locateCenterOnScreen('./img/buttons/spec_inv_ore.bmp',
                                            confidence=conf,
                                            region=(originx, originy,
                                                    windowx, windowy))
    if spec_inv_ore is not None and no_additional_invs is None:
        logging.debug('found ore inventory')
        return 1

    else:
        return 0


def spec_inv_warning():
    """Look for a popup indicating the selected inventory items aren't
    compatible with the ship's special inventory. This warning is partially
    transparent so confidence rating must be slightly lower than normal."""
    spec_inv_warning_var = pag.locateCenterOnScreen(
        './img/popups/spec_inv.bmp',
        confidence=0.8,
        region=(originx, originy, windowx, windowy))
    if spec_inv_warning_var is None:
        logging.debug('no special inventory warning')
        return 0
    else:
        logging.debug('detected special inventory warning')
        return 1


def set_quant_warning():
    """Check if a 'set quantity' window appears, indicating there isn't enough
    space in the ship's inventory for a full item stack."""
    set_quant = pag.locateOnScreen('./img/popups/set_quant.bmp',
                                   confidence=0.85,
                                   region=(originx, originy,
                                                 windowx, windowy))
    if set_quant is None:
        logging.debug('no set quantity warning')
        return 0
    else:
        logging.debug('detected set quantity warning')
        time.sleep(float(random.randint(100, 800)) / 1000)
        pag.keyDown('enter')
        time.sleep(float(random.randint(5, 100)) / 1000)
        pag.keyUp('enter')
        return 1


def not_enough_space_warning():
    # Check if a 'not enough space' warning appears, indicating the item stacks
    # selected will not fit into the ship's inventory, or inventory is
    # already full.
    not_enough_space = pag.locateCenterOnScreen(
        './img/warnings/not_enough_space.bmp',
        confidence=conf,
        region=(originx, originy, windowx, windowy))
    if not_enough_space is None:
        logging.debug('no not enough space warning')
        return 0
    else:
        logging.debug('detected not enough space warning')
        time.sleep(float(random.randint(100, 800)) / 1000)
        pag.keyDown('enter')
        time.sleep(float(random.randint(5, 100)) / 1000)
        pag.keyUp('enter')
        return 1


def undock_loop():
    """Undock from the station with the default hotkey. The undock_loop has been
    completed once the script sees the cyan ship icon in the top left corner
    of the client window, indicating a session change has just ocurred."""
    logging.info('undocking')
    pag.keyDown('ctrl')
    time.sleep(float(random.randint(100, 800)) / 1000)
    keyboard.keypress('u')
    time.sleep(float(random.randint(100, 800)) / 1000)
    pag.keyUp('ctrl')

    # Wait for the 'undock' button to change to 'undocking', indicating the
    # undock action has been confirmed.
    undocking = pag.locateCenterOnScreen('./img/buttons/undocking.bmp',
                                         confidence=0.90, region=(
                                        originx, originy, windowx,
                                        windowy))
    tries = 0
    while undocking is not None and tries <= 25:
        tries += 1
        logging.debug('waiting for session change to begin' + (str(tries)))
        time.sleep(int((random.randint(1000, 2000) / 1000)))
        undocking = pag.locateCenterOnScreen('./img/buttons/undocking.bmp',
                                                 confidence=0.90, region=(
                                                 originx, originy, windowx,
                                                 windowy))
    if undocking is None and tries <= 25:
        logging.debug('session change underway ' + (str(tries)))

        # Now wait for the undock to complete by looking for the session
        # change indicator.
        session_change = pag.locateCenterOnScreen(
            './img/indicators/session_change_undocked.bmp',
            confidence=0.55,
            region=(originx, originy, windowx, windowy))
        tries = 0

        while session_change is None and tries <= 30:
            tries += 1
            time.sleep(int((random.randint(1000, 2000) / 1000)))
            logging.debug('waiting for session change to complete ' +
                          (str(tries)))
            session_change = pag.locateCenterOnScreen(
                './img/indicators/session_change_undocked.bmp',
                confidence=0.55,
                region=(originx, originy, windowx, windowy))
        if session_change is not None and tries <= 30:
            logging.debug('undock completed ' + (str(tries)))
            return 1
        # If script times out waiting for the session change icon, simply
        # look for the undock button instead since ship has likely completed
        # an undock, but at this point the session change icon is probably
        # gone.
        else:
            if docked_check() == 1:
                logging.error('still docked')
                sys.exit()
            elif docked_check() == 0:
                logging.warning('undock tentatively completed')
                return 1
    else:
        logging.error('timed out waiting for session change')
        sys.exit()
