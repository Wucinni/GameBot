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
from tkinter import ttk
from win10toast import ToastNotifier
import win32gui


# Development
admin = True # True - Run script as administrator;  False - do not run script as administrator(can affect mouse and keyboard input)
debug = False # Logger not yet implemented
time_to_die_in_seconds = 999999 # Default 6 hours (21600); when the script will terminate itself

# Script and window variables
window_position = (0, 0, 1920, 1080)
file_name = os.path.basename(__file__)
path = os.path.abspath(__file__)
window_position = None
options = [] # List of handles
hwnd = None # Current handle

# Global thread variables to indicate if the function should run or not; Default not running
f1_state, f2_state, f3_state, f4_state = False, False, False, False
k1_state, k2_state, k3_state, k4_state = False, False, False, False
pickup_state = False
revive_state = False
running_state = False

# Container for the tkinter box response
message_box_response = None

# Location set by user for the attack button
attack_button_location = None


def is_admin():
    '''
    Function returns whether the script is run as administrator or not
    input - None
    output - Integer based boolean: 0 or 1
    '''
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception.args:
        return 0


def add_hwnd_option(new_option):
    '''
    Function appends a new integer value for the window handle to the dropdown selecetion list
    input - new window handle; type INT
    output - None
    '''
    if new_option:
        options.append(new_option)
        dropdown['values'] = tuple(options)


def get_window_handles():
    '''
    Function wraps all the window handles for the Windows API
    input - None
    output - None
    '''
    def get_handles(hwnd, *args):
        if win32gui.GetWindowText(hwnd) == "METIN2" and hwnd not in options:
            add_hwnd_option(hwnd)
        return hwnd
    
    win32gui.EnumWindows(get_handles, None)


def get_window_size_and_location(hwnd):
    '''
    Function retrieves window physical details
    input - window handle; Type INT
    output - position, height, width; type INT Tuple
    '''
    rectangle = win32gui.GetWindowRect(hwnd)
    x = rectangle[0]
    y = rectangle[1]
    width = rectangle[2] - x
    height = rectangle[3] - y
    win32gui.SetForegroundWindow(hwnd)

    return x, y, width, height


def on_dropdown_select(event):
    '''
    Function handles the Tkinter dropdown even in GUI
    input - Tkinter event
    output - None
    '''
    selected_value = hwnd = selected_option.get()
    get_window_handles()
    window_position = get_window_size_and_location(selected_value)


def search_image_and_get_coordinates(image_path, search_area=None):
    '''
    Function detects an image on the screen and retrieves it's center coordinates
    input - image path; Type STR
          - search_area; Type INT LIST
    output - image center; type INT TUPLE or None
    '''
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


def get_to_foreground():
    '''
    Function sends window to the foreground
    input - None
    output - None 
    '''
    while running_state:
        try:
            # If window is not in foreground, send it to foreground
            if not ctypes.windll.user32.GetForegroundWindow() == int(hwnd):
                win32gui.SetForegroundWindow(hwnd)
        except Exception as e:
            pass
        time.sleep(1)


def run_threads():
    '''
    Function starts threads for all the functionalities: keyboard input, mouse input and image detection
    input - None
    output - None
    '''
    # Window Thread
    window_thread = Thread(target=get_to_foreground)
    window_thread.start()

    # Keyboard Threads; buttons f1-f4, 1-4, z
    f1_thread, f2_thread, f3_thread, f4_thread = Thread(target=button_thread, args=("f1", )),Thread(target=button_thread, args=("f2", )), Thread(target=button_thread, args=("f3", )), Thread(target=button_thread, args=("f4", ))
    k1_thread, k2_thread, k3_thread, k4_thread = Thread(target=button_thread, args=("k1", )), Thread(target=button_thread, args=("k2", )), Thread(target=button_thread, args=("k3", )), Thread(target=button_thread, args=("k4", ))
    pickup_thread = Thread(target=button_thread, args=("pickup", ))

    # Revive Thread; includes image detection, mouse movement and keyboard input
    revive_thread = Thread(target=revive)

    # Create Thread list and start them
    thread_list = [f1_thread, f2_thread, f3_thread, f4_thread,
                   k1_thread, k2_thread, k3_thread, k4_thread,
                   pickup_thread, revive_thread]

    for thread in thread_list:
        thread.daemon = True
        thread.start()


def button_thread(button_name):
    '''
    Function sends keyboard input based on key name at a time interval
    input - button_name; Type STR
    output - None
    '''
    timer = time.time()
    while running_state:
        # If button_state(e.g f1_state)is True and timer indicates it passed the mark send key inputs
        if globals()[button_name + "_state"] and time.time() - timer > globals()[button_name + "_timers_slider"].get():
            if button_name[0] == "f":
                pydirectinput.press(button_name)
            elif button_name[0] == "k":
                pydirectinput.press(button_name[1])
            else:
                pydirectinput.press("z")
            timer = time.time()
        time.sleep(0.01)


def revive():
    '''
    Function revives the character by detecting revive button on screen and then sends key inputs
    input - None
    output - None
    '''

    global running_state
    found_revive_button = False

    '''
    The following timers represents last time the code was run and last time the detection was made:
        - timer -> will check if the loop was already ran once in the last # seconds
        - last_check -> will check if the button detection was already made in the last # seconds
        
    Inside loop will run as long as the revive button is detected and mouse input
    was unable to press on it, that is why 2 timers are needed
    '''
    timer = time.time()
    last_check = time.time()
    
    while running_state:
        if revive_state and time.time() - timer > 60 and time.time() - last_check > 10:
            try:
                # Run loop as long as the revive button is active on screen
                while revive_location := search_image_and_get_coordinates(path[:len(path)-len(file_name)] + "assets\\revive.png"):
                    found_revive_button = True
                    
                    # Set script state to False so threads won't run while character is dead
                    running_state = False

                    # Move mouse to revive button location and press
                    pyautogui.moveTo(revive_location[0], revive_location[1], 0.05)
                    pyautogui.click(button='left')
                    time.sleep(0.1)
                    pyautogui.moveTo(300, 300)

                    # Use health potion button and then wait 1 second for regeneration
                    for i in range(0, 5):
                        pydirectinput.press('1')
                        time.sleep(0.005)
                    time.sleep(1.025)

                    # If key threads are set to run send their key inputs
                    if k2_state:
                        pydirectinput.press('2')
                        time.sleep(0.01)
                    if k3_state:
                        pydirectinput.press('3')
                        time.sleep(0.01)
                    if k4_state:
                        pydirectinput.press('4')
                        time.sleep(0.01)
                    if f1_state:
                        pydirectinput.press('f1')
                        time.sleep(0.01)
                    if f2_state:
                        pydirectinput.press('f2')
                        time.sleep(0.01)
                    if f3_state:
                        pydirectinput.press('f3')
                        time.sleep(0.01)
                    if f4_state:
                        pydirectinput.press('f4')
                        time.sleep(0.01)

                    # Set script state to True so threads are able to run again
                    running_state = True
                    
                    # After revive detect auto-attack window and reset revive to False
                    attack_window = None
                    while attack_window is None and found_revive_button:
                        try:
                            attack_window = search_image_and_get_coordinates(path[:len(path)-len(file_name)] + "assets\\attack_window.png")
                        except:  
                            pydirectinput.press('k')
                            time.sleep(1)
                            pyautogui.moveTo(attack_button_location[0], attack_button_location[1], 0.333)
                            time.sleep(1)
                            pydirectinput.click()
                            time.sleep(0.5)
                            found_revive_button = False

                    # Reset timer for this loop
                    last_check = time.time()

                    # Run all active threads again
                    run_threads()
                    
            except Exception as error:
                print(error)
                print("Image was not found.")

            timer = time.time()
        time.sleep(0.01)


def windows_notification(message):
    try:
        toast = ToastNotifier()
        toast.show_toast(
        "LevelBot",
        message,
        duration = 5,
        icon_path = None,
        threaded = True,
        )
    except:
        pass # Implement notification error

def start(running_button, running_start_logo, running_stop_logo):
    '''
    Function starts all the threads while indicating changes by alternating running_button logo
    input - None
    output - None
    '''
    global running_state
    keyboard.wait("f5")
    # If not running -> run, start threads and start itself again
    if not running_state:
        windows_notification("Bot has started.")
        running_state = True
        running_button.config(image=running_start_logo)
        run_threads()
        start(running_button, running_start_logo, running_stop_logo)
    # If running -> set flag to False, all threads stop and run itself again
    else:
        windows_notification("Bot has stopped.")
        running_state = False
        running_button.config(image=running_stop_logo)
        start(running_button, running_start_logo, running_stop_logo)


def display_message_box():
    '''
    Function handles a GUI pop-up and saves mouse input location
    input - None
    output - None
    '''
    # Wait while user has not pressed pop-up button yet
    global message_box_response
    while message_box_response != "ok":
        pass

    # When pop-up button was pressed, save next left click location
    def on_click(x, y, button, pressed):
        global attack_button_location
        if button == mouse.Button.left:
            attack_button_location = [x, y]
            return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    # Display to user click location
    tk.messagebox.showinfo(message=f"Location: {attack_button_location[0]}, {attack_button_location[1]}.")

    # Reset box response for next use
    message_box_response = None


# def change_buttons_state(key_name):
def change_buttons_state(key_name, button, start_logo, stop_logo):
    '''
    Function changes threads state dynamically and alternates button logos
    input - key_name; Type STR
          - button; Type Tkinter.Button Object
          - start_logo; Type Tkinter PhotoImage object
          - stop_logo; Type Tkinter PhotoImage object
    output - None
    '''
    if not globals().get(key_name + "_state"):
        globals()[key_name + "_state"] = True
        button.config(image=start_logo)

        if key_name == "revive":
            global message_box_response
            message_box_thread = Thread(target=display_message_box)
            message_box_thread.start()
            message_box_response = tk.messagebox.showinfo(message="Click revive button location.")
    else:
        globals()[key_name + "_state"] = False
        button.config(image=stop_logo)

    


def main():
    # Run whole app as admininstrator if privileges are set to 0
    if not is_admin() and admin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 0)
        return

    global f1_timers_slider, f2_timers_slider, f3_timers_slider, f4_timers_slider
    global k1_timers_slider, k2_timers_slider, k3_timers_slider, k4_timers_slider
    global pickup_timers_slider
    global dropdown, selected_option


    # Main window Characteristics
    root = tk.Tk()
    root.title("Level Bot")
    root.geometry("330x400")

    # Strings for the labels
    selected_option = tk.StringVar()

    # Button Logos
    # Create images and then create logos from these images for the gui
    f1_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\f1_start.png")
    f1_start_logo = f1_start_image.subsample(1, 1)

    f1_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\f1_stop.png")
    f1_stop_logo = f1_stop_image.subsample(1, 1)

    f2_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\f2_start.png")
    f2_start_logo = f2_start_image.subsample(1, 1)

    f2_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\f2_stop.png")
    f2_stop_logo = f2_stop_image.subsample(1, 1)

    f3_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\f3_start.png")
    f3_start_logo = f3_start_image.subsample(1, 1)

    f3_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\f3_stop.png")
    f3_stop_logo = f3_stop_image.subsample(1, 1)

    f4_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\f4_start.png")
    f4_start_logo = f4_start_image.subsample(1, 1)

    f4_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\f4_stop.png")
    f4_stop_logo = f4_stop_image.subsample(1, 1)

    revive_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\revive_start.png")
    revive_start_logo = revive_start_image.subsample(1, 1)

    revive_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\revive_stop.png")
    revive_stop_logo = revive_stop_image.subsample(1, 1)

    k1_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\k1_start.png")
    k1_start_logo = k1_start_image.subsample(1, 1)

    k1_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\k1_stop.png")
    k1_stop_logo = k1_stop_image.subsample(1, 1)

    k2_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\k2_start.png")
    k2_start_logo = k2_start_image.subsample(1, 1)

    k2_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\k2_stop.png")
    k2_stop_logo = k2_stop_image.subsample(1, 1)

    k3_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\k3_start.png")
    k3_start_logo = k3_start_image.subsample(1, 1)

    k3_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\k3_stop.png")
    k3_stop_logo = k3_stop_image.subsample(1, 1)

    k4_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\k4_start.png")
    k4_start_logo = k4_start_image.subsample(1, 1)

    k4_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\k4_stop.png")
    k4_stop_logo = k4_stop_image.subsample(1, 1)

    pickup_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\pickup_start.png")
    pickup_start_logo = pickup_start_image.subsample(1, 1)

    pickup_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\pickup_stop.png")
    pickup_stop_logo = pickup_stop_image.subsample(1, 1)

    running_start_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\running_start.png")
    running_start_logo = running_start_image.subsample(7, 7)

    running_stop_image = tk.PhotoImage(file=path[:len(path)-len(file_name)] + "assets\\running_stop.png")
    running_stop_logo = running_stop_image.subsample(7, 7)

    # Dropdown for picking window
    dropdown = ttk.Combobox(root, textvariable=selected_option, values=options, state="readonly")
    get_window_handles()
    dropdown.place(x=75, y=30)
    dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

    # Buttons
    k1_button = tk.Button(root, image=k1_stop_logo)
    k1_button.place(x=5, y=70)
    k1_button.config(command=lambda: change_buttons_state("k1", k1_button, k1_start_logo, k1_stop_logo))

    k2_button = tk.Button(root, image=k2_stop_logo)
    k2_button.place(x=5, y=118)
    k2_button.config(command=lambda: change_buttons_state("k2", k2_button, k2_start_logo, k2_stop_logo))

    k3_button = tk.Button(root, image=k3_stop_logo)
    k3_button.place(x=5, y=166)
    k3_button.config(command=lambda: change_buttons_state("k3", k3_button, k3_start_logo, k3_stop_logo))

    k4_button = tk.Button(root, image=k4_stop_logo)
    k4_button.place(x=5, y=214)
    k4_button.config(command=lambda: change_buttons_state("k4", k4_button, k4_start_logo, k4_stop_logo))

    pickup_button = tk.Button(root, image=pickup_stop_logo)
    pickup_button.place(x=5, y=262)
    pickup_button.config(command=lambda: change_buttons_state("pickup", pickup_button, pickup_start_logo, pickup_stop_logo))

    f1_button = tk.Button(root, image=f1_stop_logo)
    f1_button.place(x=175, y=70)
    f1_button.config(command=lambda: change_buttons_state("f1", f1_button, f1_start_logo, f1_stop_logo))

    f2_button = tk.Button(root, image=f2_stop_logo)
    f2_button.place(x=175, y=118)
    f2_button.config(command=lambda: change_buttons_state("f2", f2_button, f2_start_logo, f2_stop_logo))

    f3_button = tk.Button(root, image=f3_stop_logo)
    f3_button.place(x=175, y=166)
    f3_button.config(command=lambda: change_buttons_state("f3", f3_button, f3_start_logo, f3_stop_logo))

    f4_button = tk.Button(root, image=f4_stop_logo)
    f4_button.place(x=175, y=214)
    f4_button.config(command=lambda: change_buttons_state("f4", f4_button, f4_start_logo, f4_stop_logo))

    revive_button = tk.Button(root, image=revive_stop_logo)
    revive_button.place(x=175, y=263)
    revive_button.config(command=lambda: change_buttons_state("revive", revive_button, revive_start_logo, revive_stop_logo))

    running_button = tk.Button(root, image=running_stop_logo)
    running_button.place(x=15, y=312)

    # Button Timers
    f1_timers_slider = tk.Scale(root, from_=1, to=180, orient='horizontal')
    f1_timers_slider.place(x=220, y=60)

    f2_timers_slider = tk.Scale(root, from_=1, to=60, orient='horizontal')
    f2_timers_slider.place(x=220, y=108)

    f3_timers_slider = tk.Scale(root, from_=1, to=60, orient='horizontal')
    f3_timers_slider.place(x=220, y=156)

    f4_timers_slider = tk.Scale(root, from_=1, to=60, orient='horizontal')
    f4_timers_slider.place(x=220, y=204)

    k1_timers_slider = tk.Scale(root, from_=1, to=3, orient='horizontal')
    k1_timers_slider.place(x=50, y=60)

    k2_timers_slider = tk.Scale(root, from_=1, to=60, orient='horizontal')
    k2_timers_slider.place(x=50, y=108)

    k3_timers_slider = tk.Scale(root, from_=1, to=120, orient='horizontal')
    k3_timers_slider.place(x=50, y=156)

    k4_timers_slider = tk.Scale(root, from_=1, to=1860, orient='horizontal')
    k4_timers_slider.place(x=50, y=204)

    pickup_timers_slider = tk.Scale(root, from_=0.167, to=60, orient='horizontal')
    pickup_timers_slider.place(x=50, y=252)

    # Labels
    dropdown_label = tk.Label(root, text="Choose Client:")
    dropdown_label.place(x=105, y=5)

    # Threads
    start_thread = Thread(target=start, args=(running_button, running_start_logo, running_stop_logo))
    start_thread.daemon = True
    start_thread.start()

    root.resizable(False, False)
    root.after(time_to_die_in_seconds * 1000, lambda: root.destroy()) # Destroy the widget after n seconds
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Get error type, file and line
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        # Write error to log file
        f = open("logerror.txt", "a")
        f.write(str(datetime.datetime.now()) + ": " + str(exc_type) + " FILE:" + str(fname) + " Line:" +  str(exc_tb.tb_lineno) + "\n")
        f.close()
