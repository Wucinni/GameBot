import threading
import time
import random
import pydirectinput

def simulate_press(key, hold_min=0.05, hold_max=0.15):
    try:
        pydirectinput.keyDown(key)
        hold_time = random.uniform(hold_min, hold_max)
        time.sleep(hold_time)
        pydirectinput.keyUp(key)

    except Exception as e:
        print(f"Error simulating press for key {key}: {e}")

def space_spammer():
    print("Space thread started: Holding 'space' indefinitely.")
    pydirectinput.keyDown('space')

def button_4_presser():
    print("Button 4 thread started: Pressing '4' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('4', hold_min=0.05, hold_max=0.15)


if __name__ == "__main__":
    
    print("-" * 50)
    print("Starting automated input script in 5 seconds...")
    print("!!! Switch to your target application NOW !!!")
    print("Press Ctrl+C in this console to stop the script.")
    print("-" * 50)
    
    time.sleep(5)
    
    space_thread = threading.Thread(target=space_spammer, daemon=True)
    button_4_thread = threading.Thread(target=button_4_presser, daemon=True)
    
    space_thread.start()
    button_4_thread.start()
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pydirectinput.keyUp('space')
        print("\nScript terminated by user (Ctrl+C). Exiting...")
