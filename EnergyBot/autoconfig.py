import sys
import subprocess

module_list = ["keyboard", "pyautogui", "pydirectinput", "pynput", "thread6", "tk", "pywin32", "win32gui"]

for module in module_list:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
    except:
        pass
