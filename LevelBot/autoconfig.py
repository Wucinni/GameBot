import sys
import subprocess

module_list = ["pywin32", "pydirectinput", "opencv-python", "tk", "thread6", "keyboard", "pyautogui", "win32gui", "datetime", "pynput", "win10toast"]

for module in module_list:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
    except:
        pass
