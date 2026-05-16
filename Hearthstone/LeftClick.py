import pyautogui
import time
import keyboard
import random

pyautogui.FAILSAFE = True

print("===AUTOCLICKER STARTED===")
print("Press Ctrl+C or 'q' to stop")
print("Starting in 3 Seconds...")
time.sleep(3)

try:
        while True:
#            if keyboard.is_pressed('q'):
#                print("\nScript stopped by user")
#                break

            pyautogui.click()
            delay = random.uniform(1.0,2.0)
#            time.sleep(1)
            time.sleep(delay)


except KeyboardInterrupt:
    print("\nScript stopped via terminal")


