import tkinter as tk
from tkinter import OptionMenu
from pynput import mouse, keyboard
from threading import Thread
import os
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import time
from Quartz.CoreGraphics import CGEventCreateKeyboardEvent, CGEventPost, kCGHIDEventTap


running = False
KSA = False

ssKeybind = 'e'

options = [1, 2, 3, 4, 5, 6]

roblox_number_keycodes = {
    '1': 18,
    '2': 19,
    '3': 20,
    '4': 21,
    '5': 23,
    '6': 22,
    '7': 26,
    '8': 28,
    '9': 25,
    '0': 29
}

mainScreen = tk.Tk()
mainScreen.title("FBG Level Macro V1.0 (By Dark)")
mainScreen.geometry("300x150")
mainScreen.resizable(False, False)

moveCount = tk.IntVar(value = options[0])

ssFrame = tk.Frame(mainScreen)
ssFrame.pack(pady=10)
ssButton = tk.Button(ssFrame, text=f"Start/Stop ({ssKeybind})", width=15, height=2, command=lambda: inputEvent(ssKeybind))
ssButton.pack(padx=15, side="left")
ssRebind = tk.Button(ssFrame, text="Rebind", height=2, width=5, command=lambda: rebind_key(ssKeybind, ssButton, f"Start/Stop"))
ssRebind.pack(side="left")

moveCountFrame = tk.Frame(mainScreen)
moveCountFrame.pack(pady=10)
moveCountLabel = tk.Label(moveCountFrame, text="Number of Moves:")
moveCountLabel.pack(side="left")
moveCountOM = tk.OptionMenu(moveCountFrame, moveCount, *options)
moveCountOM.pack(side="left")

statusLabel = tk.Label(mainScreen, text="Status: Stopped", font=("Arial", 14, "bold"))
statusLabel.pack(pady=10)
    
def rebind_key(targetVar, uiVar, uiText):
    global KSA
    global ssKeybind
    prompt = tk.Toplevel(mainScreen)
    prompt.title("Rebind Key")
    prompt.geometry("300x80")
    prompt.transient(mainScreen)
    tk.Label(prompt, text=f"Press new key for keybind...").pack(pady=10)
    prompt.focus_force()
    KSA = True

    def on_key(event):
        nonlocal targetVar
        nonlocal prompt
        newBind = event.keysym
        targetVar = newBind
        uiVar.config(text=f"{uiText} ({newBind})")
        prompt.destroy()
    KSA = False
    prompt.bind("<Key>", on_key)

def inputEvent(key):
    global running
    if KSA:
        return
    try:
        key = key.char
    except (TypeError, AttributeError):
        return
    if key == ssKeybind:
        if not running:
            running = True
            statusLabel.config(text="Status: Running")
            thread = Thread(target=startMacro, daemon=True)
            thread.start()
        else:
            running = False
            statusLabel.config(text="Status: Stopped")

KC = KeyboardController()
MC = MouseController()

def press_roblox_number(key_char):
    """Send a raw hardware key press using Quartz."""
    key_code = roblox_number_keycodes.get(key_char)
    if key_code is None:
        print(f"No keycode for {key_char}")
        return

    event_down = CGEventCreateKeyboardEvent(None, key_code, True)
    CGEventPost(kCGHIDEventTap, event_down)

    event_up = CGEventCreateKeyboardEvent(None, key_code, False)
    CGEventPost(kCGHIDEventTap, event_up)


def startMacro():
    global moveCount
    currentNumber = 1
    while running:
            press_roblox_number(str(currentNumber))
            time.sleep(.5)
            MC.click(mouse.Button.left, 1)
            currentNumber += 1
            if currentNumber > moveCount.get():
                currentNumber = 1

listener = keyboard.Listener(on_press=inputEvent)
listener.start()

mainScreen.mainloop()