import time
from pynput import keyboard
import pandas as pd
import tkinter as tk
from collections import defaultdict

start_time = time.time()
keystrokes = []
key_count = 0
word_count = 0
errors = 0

key_freq = defaultdict(int)

# GUI Setup
root = tk.Tk()
root.title("Typing Analytics Dashboard")
root.geometry("400x300")

label_speed = tk.Label(root, text="WPM: 0", font=("Arial", 14))
label_speed.pack()

label_keys = tk.Label(root, text="Keys Pressed: 0", font=("Arial", 14))
label_keys.pack()

label_words = tk.Label(root, text="Words: 0", font=("Arial", 14))
label_words.pack()

label_top = tk.Label(root, text="Top Key: None", font=("Arial", 14))
label_top.pack()

def calculate_wpm():
    elapsed = time.time() - start_time
    return round((word_count / elapsed) * 60, 2) if elapsed > 0 else 0

def update_dashboard():
    wpm = calculate_wpm()
    label_speed.config(text=f"WPM: {wpm}")
    label_keys.config(text=f"Keys Pressed: {key_count}")
    label_words.config(text=f"Words: {word_count}")

    if key_freq:
        top_key = max(key_freq, key=key_freq.get)
        label_top.config(text=f"Top Key: {top_key}")

    root.after(1000, update_dashboard)

def on_press(key):
    global key_count, word_count, errors

    key_count += 1

    try:
        k = key.char
        keystrokes.append(k)
        key_freq[k] += 1

        if k == " ":
            word_count += 1

    except AttributeError:
        if key == keyboard.Key.backspace:
            errors += 1
        keystrokes.append(str(key))

def on_release(key):
    if key == keyboard.Key.esc:
        save_data()
        return False

def save_data():
    df = pd.DataFrame({
        "keystroke": keystrokes
    })
    df.to_csv("typing_data.csv", index=False)
    print("Data saved to typing_data.csv")

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

update_dashboard()
root.mainloop()
