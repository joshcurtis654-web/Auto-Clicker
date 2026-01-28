import time
import threading
from pynput import keyboard, mouse
import tkinter as tk

running = False
interval = 1


mainScreen = tk.Tk()

mainScreen.title("Dark Auto Clicker V1.0")
mainScreen.geometry("450x200")
mainScreen.resizable(False, False)

timeFrame = tk.Frame(mainScreen)
timeFrame.pack(pady=30)

hourTextBox = tk.Entry(timeFrame, width=5)
hourTextBox.pack(side="left")
hourTextBox.insert(0, "0")
hourTextLabel = tk.Label(timeFrame, text="Hour(s)")
hourTextLabel.pack(side="left")

minuteTextBox = tk.Entry(timeFrame, width=5)
minuteTextBox.pack(side="left")
minuteTextBox.insert(0, "0")
minuteTextLabel = tk.Label(timeFrame, text="Minute(s)")
minuteTextLabel.pack(side="left")

secondTextBox = tk.Entry(timeFrame, width=5)
secondTextBox.pack(side="left")
secondTextBox.insert(0, "1")
secondTextLabel = tk.Label(timeFrame, text="Second(s)")
secondTextLabel.pack(side="left")

startLabel = tk.Button(mainScreen, text="Start/Stop (Tab)", width=15, height=2)
startLabel.pack(pady=10)

def calculateInterval():
    hours = int(hourTextBox.get())
    minutes = int(minuteTextBox.get())
    seconds = int(secondTextBox.get())
    totalSeconds = hours * 3600 + minutes * 60 + seconds

    print(totalSeconds)
    return totalSeconds

def on_press(key): 
    global running
    global interval
    if key == keyboard.Key.tab:
        running = not running
        if running:
            interval = calculateInterval()
            threading.Thread(target=startClick).start()

def startClick():
    global running
    global interval
    mouseController = mouse.Controller()
    while running:
        mouseController.click(mouse.Button.left, 1)
        print("Clicked")
        time.sleep(interval)

def run_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()


mainScreen.mainloop()
mainScreen.after(100, run_listener)

if __name__ == "__main__":
    mainScreen.mainloop()