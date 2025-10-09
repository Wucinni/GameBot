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

def button_1():
    print("Button 1 thread started: Pressing '1' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('1', hold_min=0.05, hold_max=0.15)

def button_2():
    print("Button 2 thread started: Pressing '2' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('2', hold_min=0.05, hold_max=0.15)

def button_3():
    print("Button 3 thread started: Pressing '3' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('3', hold_min=0.05, hold_max=0.15)

def button_4():
    print("Button 4 thread started: Pressing '4' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('4', hold_min=0.05, hold_max=0.15)

def button_f1():
    print("Button f1 thread started: Pressing 'f1' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('f1', hold_min=0.05, hold_max=0.15)

def button_f2():
    print("Button f2 thread started: Pressing 'f2' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('f2', hold_min=0.05, hold_max=0.15)

def button_f3():
    print("Button f3 thread started: Pressing 'f3' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('f3', hold_min=0.05, hold_max=0.15)

def button_f4():
    print("Button f4 thread started: Pressing 'f4' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('f4', hold_min=0.05, hold_max=0.15)

def button_z():
    print("Button z thread started: Pressing 'z' every ~1 second.")
    min_interval = 0.9
    max_interval = 1.1
    
    while True:
        random_delay = random.uniform(min_interval, max_interval)
        time.sleep(random_delay)
        simulate_press('z', hold_min=0.05, hold_max=0.15)

if __name__ == "__main__":
    
    print("-" * 50)
    print("Starting automated input script in 5 seconds...")
    print("!!! Switch to your target application NOW !!!")
    print("Press Ctrl+C in this console to stop the script.")
    print("-" * 50)
    
    time.sleep(5)
    
    space_thread = threading.Thread(target=space_spammer, daemon=True)
    button_1_thread = threading.Thread(target=button_1, daemon=True)
    button_2_thread = threading.Thread(target=button_2, daemon=True)
    button_3_thread = threading.Thread(target=button_3, daemon=True)
    button_4_thread = threading.Thread(target=button_4, daemon=True)
    button_f1_thread = threading.Thread(target=button_f1, daemon=True)
    button_f2_thread = threading.Thread(target=button_f2, daemon=True)
    button_f3_thread = threading.Thread(target=button_f3, daemon=True)
    button_f4_thread = threading.Thread(target=button_f4, daemon=True)
    button_z_thread = threading.Thread(target=button_z, daemon=True)
    
    space_thread.start()
    button_1_thread.start()
    button_2_thread.start()
    button_3_thread.start()
    button_4_thread.start()
    button_f1_thread.start()
    button_f2_thread.start()
    button_f3_thread.start()
    button_f4_thread.start()
    button_z_thread.start()
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pydirectinput.keyUp('space')
        print("\nScript terminated by user (Ctrl+C). Exiting...")
