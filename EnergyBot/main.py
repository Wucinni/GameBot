import ctypes
import keyboard
import os
import pyautogui
import pydirectinput
from pynput import mouse
import sys
from threading import *
import time
import tkinter as tk
import tkinter.messagebox
import win32gui


window_position = (0, 0, 1920, 1080)
path = os.path.abspath(__file__)

options = []
dropdown = None
selected_option = None

buy_status_button = None
craft_status_button = None
start_button_logo = None
stop_button_logo = None
buy_key_label = None
craft_key_label = None
alchemist_button = None
alchemist_location = [0, 0]

buy_status = 1
craft_status = 1
buy_key = "1"
craft_key = "2"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception.args:
        return False


def add_option(new_option):
    if new_option:
        options.append(new_option)
        dropdown['values'] = tuple(options)


def get_window_handles():
    global options

    def get_handles(hwnd, *args):

        if win32gui.GetWindowText(hwnd) == "METIN2" and hwnd not in options:
            add_option(hwnd)
        return hwnd
    win32gui.EnumWindows(get_handles, None)


def get_window_size_and_location(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\t    Size: (%d, %d)" % (w, h))
    win32gui.SetForegroundWindow(hwnd)

    return x, y, w, h


def on_dropdown_select(event):
    global window_position
    selected_value = selected_option.get()
    print(f"Selected option: {selected_value}")
    get_window_handles()
    window_position = get_window_size_and_location(selected_value)


def search_image_and_get_coordinates(image_path, search_area=None):
    screenshot = pyautogui.screenshot()
    x, y, w, z = 0, 0, 0, 0

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
        print("\nZone: ", search_zone, search_area, search_area[3], z, "\n")
        print(search_area[3], search_area[3]>0)
        location = pyautogui.locateOnScreen(image_path, region=search_zone, confidence=0.8)
    else:
        location = pyautogui.locateOnScreen(image_path, confidence=0.8)

    if location is not None:
        x, y, width, height = location
        center_x = x + width // 2
        center_y = y + height // 2
        return center_x, center_y
    else:
        return None


def buy():
    global buy_status_button, start_button_logo, stop_button_logo, buy_status, buy_key
    running = False

    def check_stop_buy():
        while running:
            if search_image_and_get_coordinates(path[0:-8] + "\\shop.png", window_position) is not None:
                knife_location = search_image_and_get_coordinates(path[0:-8] + "\\knife.png", window_position)

                if knife_location is not None:
                    pyautogui.moveTo(knife_location[0], knife_location[1], 0.05)
                    pyautogui.click(button='right')
                    time.sleep(0.5)

    buy_check_stop = Thread(target=check_stop_buy)
    buy_check_stop.start()

    while True:
        keyboard.wait(str(buy_key))

        if not running:
            running = True
            buy_status_button.config(image=stop_button_logo)
            mouse_thread = Thread(target=check_stop_buy)
            mouse_thread.start()
        else:
            running = False
            buy_status_button.config(image=start_button_logo)


def craft():
    global craft_status_button, start_button_logo, stop_button_logo, craft_status, craft_key
    running = False

    def check_stop_craft():
        while running:
                knife_location = None
                try:
                    knife_location = search_image_and_get_coordinates(path[0:-8] + "\\knife.png", window_position)
                except:
                    pass
                
                if knife_location is not None:
                    pyautogui.moveTo(knife_location[0], knife_location[1], 0.2)
                    pyautogui.click(button='left')

                    pyautogui.moveTo(alchemist_location[0], alchemist_location[1], 0.2)
                    pyautogui.click(button='left')
                    
                    time.sleep(0.3)
                    pydirectinput.press("enter")
                    time.sleep(0.2)
                    pydirectinput.press("enter")

    craft_check_stop = Thread(target=check_stop_craft)
    craft_check_stop.daemon = True
    craft_check_stop.start()

    while True:
        keyboard.wait(str(craft_key))

        if not running:
            running = True
            craft_status_button.config(image=stop_button_logo)
            mouse_thread = Thread(target=check_stop_craft)
            mouse_thread.start()
        else:
            running = False
            craft_status_button.config(image=start_button_logo)


def change_buy_key():
    global buy_key, buy_key_label
    buy_key = keyboard.read_key()

    buy_key_text = tk.StringVar()
    buy_key_text.set(buy_key)
    buy_key_label.config(textvariable=buy_key_text)


def change_craft_key():
    global craft_key, craft_key_label
    craft_key = keyboard.read_key()

    craft_key_text = tk.StringVar()
    craft_key_text.set(craft_key)
    craft_key_label.config(textvariable=craft_key_text)

def alchemist_button_location():
    tk.messagebox.showinfo(message="Click revive button location.")
    
    def on_click(x, y, button, pressed):
        global alchemist_location
        if button == mouse.Button.left:
            alchemist_location = [x, y]
            return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    tk.messagebox.showinfo(message=f"Location: {alchemist_location[0]}, {alchemist_location[1]}.")


def main():
    admin = True
    if not is_admin() and admin:
        # Re-run the script with administrator privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
        return

    global dropdown, selected_option, start_button_logo, stop_button_logo, buy_key, craft_key, buy_status_button
    global craft_status_button, buy_key, craft_key, buy_key_label, craft_key_label
    global alchemist_button

    # Main window Characteristics
    root = tk.Tk()
    root.title("Energy Hack")
    root.geometry("300x225")

    # Strings for the labels
    selected_option = tk.StringVar()

    print("Buy key:", buy_key)
    buy_key_text = tk.StringVar()
    buy_key_text.set(buy_key)

    print("Craft key:", craft_key)
    craft_key_text = tk.StringVar()
    craft_key_text.set(craft_key)

    buy_text = tk.StringVar()
    buy_text.set("Buy Key")

    craft_text = tk.StringVar()
    craft_text.set("Craft Key")

    # Start and stop Logos
    start_button_image = tk.PhotoImage(file=path[0:-7] + "\\start_button.png")
    start_button_logo = start_button_image.subsample(7, 7)

    stop_button_image = tk.PhotoImage(file=path[0:-8] + "\\stop_button.png")
    stop_button_logo = stop_button_image.subsample(7, 7)

    alchemist_image = tk.PhotoImage(file=path[0:-7] + "alchemist.png")
    alchemist_logo = alchemist_image.subsample(2, 2)

    # Dropdown for picking window
    dropdown = tk.ttk.Combobox(root, textvariable=selected_option, values=options, state="readonly")
    get_window_handles()
    dropdown.place(x=75, y=30)
    dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

    # Start and Stop Buttons
    buy_status_button = tk.Button(root, image=start_button_logo)
    buy_status_button.place(x=35, y=90)
    buy_status_button.config(command=change_buy_key)

    craft_status_button = tk.Button(root, image=start_button_logo)
    craft_status_button.place(x=125, y=90)
    craft_status_button.config(command=change_craft_key)

    alchemist_button = tk.Button(root, image=alchemist_logo)
    alchemist_button.place(x=205, y=95)
    alchemist_button.config(command=alchemist_button_location)

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

    # Value checking threads
    buy_key_wait_thread = Thread(target=buy)
    buy_key_wait_thread.start()

    craft_key_wait_thread = Thread(target=craft)
    craft_key_wait_thread.start()

    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    try:
        with open('start.bat', 'w') as f:
            f.write(f'cd /\ncd {path[0:-8]}\npython main.py')
        main()
    except Exception as e:
        print(e)
