import tkinter as tk
import pyautogui



class GameOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Game Assistant")
        self.label = tk.Label(root, text="Mouse Position: ", font=("Arial", 14))
        self.label.pack(pady=10)
        self.region = None
        self.region_label = tk.Label(root, text="Region: Not Set", font=("Arial", 12))
        self.region_label.pack()

        self.set_region_btn = tk.Button(root, text="Set Region", command=self.set_region)
        self.set_region_btn.pack(pady=10)

        self.update_mouse_position()


    def update_mouse_position(self):
        x, y = pyautogui.position()
        self.label.config(text=f"Mouse Position: {x}, {y}")
        self.root.after(100, self.update_mouse_position)

    def set_region(self):
        self.region_label.config(text="Now Ctrl+Click top-left and bottom-right of game region...")
        self.root.after(100, self.capture_region)

    def capture_region(self):
        def on_activate():
            pass
        # Wait until two Ctrl+Clicks are detected (you can implement this via keyboard/mouse hooks)
        pass  # Placeholder for actual region detection logic
