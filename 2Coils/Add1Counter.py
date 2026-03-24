import keyboard

counter = 0

def on_space(event):
    global counter
    counter += 1
    print(f"Counter: {counter}")

print("Press SPACE to increment the counter. Press ESC to exit.")

# Bind the space bar, suppress so no space is typed in console
keyboard.on_press_key("space", on_space, suppress=True)

# Exit when ESC is pressed
keyboard.wait("esc")
print("Exiting program.")
