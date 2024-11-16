import pyautogui
import time

# Wait for 5 seconds before starting
time.sleep(5)

# The message you want to type
message = "Your message goes here. Replace this text with your actual message."

# Type the message
pyautogui.typewrite(message)