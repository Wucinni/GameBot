#############################################
#                                           #
#   This script creates a GUI for a game    #
#               automation                  #
#                                           #
#   It handles mouse, keyboard, windows and #
#       implements image detection          #
#                                           #
#############################################

import ctypes
import datetime
import keyboard
import os
import pyautogui
import pydirectinput
from pynput import mouse
import sys
from threading import *
import time
import tkinter.messagebox
import tkinter as tk
import win32gui


# Script and window variables
window_position = (0, 0, 1920, 1080)
file_name = os.path.basename(__file__)
path = os.path.abspath(__file__)
options = []

# Game variables
npc_location = [0, 0]

# Default keys for buttons
buy_key = "1"
craft_key = "2"


def is_admin():
    """
        Function returns whether the script is run as administrator or not
        input - None
        output - Integer based boolean: 0 or 1
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception.args:
        return False


def add_hwnd_option(new_option):
    """
        Function appends a new integer value for the window handle to the dropdown selection list
        input - new window handle; type INT
        output - None
    """
    if new_option:
        options.append(new_option)
        dropdown['values'] = tuple(options)


def get_window_handles():
    """
        Function wraps all the window handles for the Windows API
        input - None
        output - None
    """

    def get_handles(hwnd, *args):
        if win32gui.GetWindowText(hwnd) == "METIN2" and hwnd not in options:
            add_hwnd_option(hwnd)
        return hwnd

    win32gui.EnumWindows(get_handles, None)


def get_window_size_and_location(hwnd):
    """
        Function retrieves window physical details
        input - window handle; Type INT
        output - position, height, width; type INT Tuple
    """
    rectangle = win32gui.GetWindowRect(hwnd)
    x = rectangle[0]
    y = rectangle[1]
    width = rectangle[2] - x
    height = rectangle[3] - y

    win32gui.SetForegroundWindow(hwnd)

    return x, y, width, height


def on_dropdown_select(event):
    """
        Function handles the Tkinter dropdown event in GUI
        input - Tkinter event
        output - None
    """
    selected_value = selected_option.get()
    get_window_handles()
    window_position = get_window_size_and_location(selected_value)


def search_image_and_get_coordinates(image_path, search_area=None):
    """
            Function detects an image on the screen and retrieves its center coordinates
            input - image path; Type STR
                  - search_area; Type INT LIST
            output - image center; type INT TUPLE or None
    """
    screenshot = pyautogui.screenshot()
    x, y, w, z = 0, 0, 0, 0

    # Search image on screen
    if search_area:
        if search_area[0] > 0:
            x = search_area[0]
        if search_area[1] > 0:
            y = search_area[1]
        if search_area[2] > 0:
            w = search_area[2]
        if search_area[3] > 0:
            z = search_area[3]
        search_zone = (x, y, w, z)
        location = pyautogui.locateOnScreen(image_path, region=search_zone, confidence=0.8)
    else:
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)

    # If image was found, return center coordinates
    if location is not None:
        x, y, width, height = location
        center_x = x + width // 2
        center_y = y + height // 2
        return center_x, center_y

    # In case of fail return None
    else:
        return None


def buy(button, start_logo, stop_logo):
    """
        This function will buy(right click) a specific item when the NPC window is open
        input - None
        output - None
    """
    running = False

    def buy_item():
        """
            This function will detect a specific item on screen and right-click on it
            input - None
            output - None
        """
        while running:
            try:
                # If window is on screen and item was detected right click on it every 0.5 seconds
                if search_image_and_get_coordinates(path[:len(path)-len(file_name)] + "assets\\shop.png", window_position):
                    if knife_location := search_image_and_get_coordinates(path[:len(path)-len(file_name)] + "assets\\knife.png", window_position):
                        pyautogui.moveTo(knife_location[0], knife_location[1], 0.05)
                        pyautogui.click(button='right')
                        time.sleep(0.5)
            except:
                pass  # Solve error when function can't find object on screen

    while True:
        keyboard.wait(str(buy_key))

        # If not running, start thread and change button image
        if not running:
            running = True
            button.config(image=stop_logo)

            mouse_thread = Thread(target=buy_item)
            mouse_thread.daemon = True
            mouse_thread.start()

        # If running, stop and change button image
        else:
            running = False
            button.config(image=start_logo)


def craft(button, start_logo, stop_logo):
    """
        This function will detect the NPC and move the item on it
        input - None
        output - None
    """
    running = False

    def craft_item():
        while running:
            try:
                # If knife was found place it on NPC and press enter twice
                if knife_location := search_image_and_get_coordinates(path[:len(path)-len(file_name)] + "assets\\knife.png", window_position):
                    pyautogui.moveTo(knife_location[0], knife_location[1], 0.2)
                    pyautogui.click(button='left')

                    pyautogui.moveTo(npc_location[0], npc_location[1], 0.2)
                    pyautogui.click(button='left')

                    time.sleep(0.3)
                    pydirectinput.press("enter")
                    time.sleep(0.2)
                    pydirectinput.press("enter")
            except:
                pass  # Solve error when function can't find object on screen


    while True:
        keyboard.wait(str(craft_key))

        # If not running, start thread and change button image
        if not running:
            running = True
            button.config(image=stop_logo)

            mouse_thread = Thread(target=craft_item)
            mouse_thread.daemon = True
            mouse_thread.start()

        # If running, stop and change button image
        else:
            running = False
            button.config(image=start_logo)


def change_buy_key(label):
    """
        Function changes the key required to run buy function
        input - None
        output - None
    """
    global buy_key
    buy_key = keyboard.read_key()

    buy_key_text = tk.StringVar()
    buy_key_text.set(buy_key)
    label.config(textvariable=buy_key_text)


def change_craft_key(label):
    """
        Function changes the key required to run craft function
        input - None
        output - None
    """
    global craft_key
    craft_key = keyboard.read_key()

    craft_key_text = tk.StringVar()
    craft_key_text.set(craft_key)
    label.config(textvariable=craft_key_text)


def set_npc_location():
    """
        Function will display pop-up window on screen and then save next left-click location
        input - None
        output - None
    """
    tk.messagebox.showinfo(message="Click NPC location on screen.")

    # Save next left click location
    def on_click(x, y, button, pressed):
        global npc_location
        if button == mouse.Button.left:
            npc_location = [x, y]
            return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    # Display saved location
    tk.messagebox.showinfo(message=f"Location: {npc_location[0]}, {npc_location[1]}.")


def main():
    admin = True
    # Run whole app as admininstrator if privileges are set to 0
    if not is_admin() and admin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
        return

    global dropdown, selected_option

    # Main window Characteristics
    root = tk.Tk()
    root.title("Energy Hack")
    root.geometry("300x225")

    # Strings for the labels
    selected_option = tk.StringVar()

    # Keys which are needed to be pressed
    buy_key_text = tk.StringVar()
    buy_key_text.set(buy_key)

    craft_key_text = tk.StringVar()
    craft_key_text.set(craft_key)

    # Names, labels for the keys
    buy_text = tk.StringVar()
    buy_text.set("Buy Key")

    craft_text = tk.StringVar()
    craft_text.set("Craft Key")

    # Button Logos
    start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\start_button.png")
    start_logo = start_image.subsample(7, 7)

    stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\stop_button.png")
    stop_logo = stop_image.subsample(7, 7)

    npc_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\alchemist.png")
    npc_logo = npc_image.subsample(2, 2)

    # Dropdown for picking window
    dropdown = tk.ttk.Combobox(root, textvariable=selected_option, values=options, state="readonly")
    get_window_handles()
    dropdown.place(x=75, y=30)
    dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

    # Buttons
    buy_button = tk.Button(root, image=start_logo)
    buy_button.place(x=35, y=90)
    buy_button.config(command=lambda: change_buy_key(buy_key_label))

    craft_button = tk.Button(root, image=start_logo)
    craft_button.place(x=125, y=90)
    craft_button.config(command=lambda: change_craft_key(craft_key_label))

    npc_button = tk.Button(root, image=npc_logo)
    npc_button.place(x=205, y=95)
    npc_button.config(command=set_npc_location)

    # Labels
    dropdown_label = tk.Label(root, text="Choose Client:")
    dropdown_label.place(x=105, y=5)

    buy_text_label = tk.Label(root, textvariable=buy_text, borderwidth=1, relief="solid")
    buy_text_label.place(x=45, y=165)

    craft_text_label = tk.Label(root, textvariable=craft_text, borderwidth=1, relief="solid")
    craft_text_label.place(x=130, y=165)

    buy_key_label = tk.Label(root, textvariable=buy_key_text)
    buy_key_label.place(x=60, y=190)

    craft_key_label = tk.Label(root, textvariable=craft_key_text)
    craft_key_label.place(x=150, y=190)

    # Threads
    buy_thread = Thread(target=buy, args=(buy_button, start_logo, stop_logo))
    buy_thread.start()

    craft_thread = Thread(target=craft, args=(craft_button, start_logo, stop_logo))
    craft_thread.start()

    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    try:
        # Creates a batch file to run the script from command line
        with open('start.bat', 'w') as f:
            f.write(f'cd /\ncd {path[0:-8]}\npython main.py')

        main()
    except Exception as error:
        # Get error type, file and line
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        # Write error to log file
        f = open("logerror.txt", "a")
        f.write(str(datetime.datetime.now()) + ": " + str(exc_type) + " FILE:" + str(fname) + " Line:" + str(
            exc_tb.tb_lineno) + "\n")
        f.close()
