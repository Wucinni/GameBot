import sys
import subprocess

module_list = ["datetime", "keyboard", "opencv-python", "pyautogui", "pydirectinput", "pynput", "pywin32", "thread6", "tk", "win32gui"]

for module in module_list:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
    except:
        pass
