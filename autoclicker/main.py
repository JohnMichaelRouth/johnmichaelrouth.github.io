import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import math
import random

# Optional imports with fallbacks
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("Warning: NumPy not available. Using built-in random functions.")

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False
    print("Warning: PyAutoGUI not available. Click simulation disabled.")

try:
    from pynput import keyboard
    from pynput.keyboard import Key, Listener
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False
    print("Warning: pynput not available. Hotkey functionality disabled.")

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Auto Clicker")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # State variables
        self.is_clicking = False
        self.hotkey = None
        self.hotkey_listener = None
        self.click_thread = None
        
        # Configuration variables
        self.abs_delay_min = tk.DoubleVar(value=20)
        self.abs_delay_max = tk.DoubleVar(value=80)
        self.delay_target = tk.DoubleVar(value=50)
        self.delay_deviation = tk.DoubleVar(value=5)
        self.weighted_distribution = tk.BooleanVar(value=False)
        self.hotkey_text = tk.StringVar(value="Not set")
        
        self.setup_ui()
        self.start_hotkey_listener()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced Auto Clicker", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Hotkey section
        hotkey_frame = ttk.LabelFrame(main_frame, text="Toggle Hotkey", padding="10")
        hotkey_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.hotkey_label = ttk.Label(hotkey_frame, textvariable=self.hotkey_text)
        self.hotkey_label.grid(row=0, column=0, padx=(0, 10))
        
        set_hotkey_btn = ttk.Button(hotkey_frame, text="Set Hotkey", command=self.set_hotkey)
        set_hotkey_btn.grid(row=0, column=1)
        
        # Delay configuration
        delay_frame = ttk.LabelFrame(main_frame, text="Delay Configuration (milliseconds)", padding="10")
        delay_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Absolute Delay Min
        ttk.Label(delay_frame, text="Absolute Delay Min:").grid(row=0, column=0, sticky=tk.W, pady=2)
        min_spinbox = ttk.Spinbox(delay_frame, from_=1, to=10000, textvariable=self.abs_delay_min, width=10)
        min_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Absolute Delay Max
        ttk.Label(delay_frame, text="Absolute Delay Max:").grid(row=1, column=0, sticky=tk.W, pady=2)
        max_spinbox = ttk.Spinbox(delay_frame, from_=1, to=10000, textvariable=self.abs_delay_max, width=10)
        max_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Delay Target
        ttk.Label(delay_frame, text="Delay Target:").grid(row=2, column=0, sticky=tk.W, pady=2)
        target_spinbox = ttk.Spinbox(delay_frame, from_=1, to=10000, textvariable=self.delay_target, width=10)
        target_spinbox.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Delay Deviation
        ttk.Label(delay_frame, text="Delay Deviation:").grid(row=3, column=0, sticky=tk.W, pady=2)
        deviation_spinbox = ttk.Spinbox(delay_frame, from_=0.1, to=1000, textvariable=self.delay_deviation, width=10)
        deviation_spinbox.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Weighted Distribution
        weighted_check = ttk.Checkbutton(delay_frame, text="Use Weighted Distribution", variable=self.weighted_distribution)
        weighted_check.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=10)
        
        # Distribution explanation
        explanation_frame = ttk.LabelFrame(main_frame, text="Distribution Info", padding="10")
        explanation_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        explanation_text = ("Standard: Normal gaussian distribution (bell curve)\n"
                          "Weighted: Right-shifted distribution (log-normal)\n"
                          "Target is the peak value, deviation controls spread")
        ttk.Label(explanation_frame, text=explanation_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Status: Stopped", foreground="red")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.start_stop_btn = ttk.Button(button_frame, text="Start Clicking", command=self.toggle_clicking)
        self.start_stop_btn.grid(row=0, column=0, padx=5)
        
        test_btn = ttk.Button(button_frame, text="Test Delay", command=self.test_delay)
        test_btn.grid(row=0, column=1, padx=5)
        
        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="Next Click Delay Preview", padding="10")
        preview_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.preview_label = ttk.Label(preview_frame, text="Click 'Test Delay' to see sample delays")
        self.preview_label.grid(row=0, column=0, sticky=tk.W)
        
    def set_hotkey(self):
        """Set a new hotkey for toggling the autoclicker"""
        if not HAS_PYNPUT:
            messagebox.showwarning("Feature Unavailable", 
                                 "Hotkey functionality requires the 'pynput' library.\n"
                                 "Install with: pip install pynput")
            return
            
        dialog = HotkeyDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.hotkey = dialog.result
            self.hotkey_text.set(f"Key: {self.hotkey}")
            self.restart_hotkey_listener()
    
    def start_hotkey_listener(self):
        """Start listening for hotkey presses"""
        if not HAS_PYNPUT:
            return
            
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        
        def on_press(key):
            try:
                if self.hotkey and str(key) == self.hotkey:
                    self.toggle_clicking()
            except AttributeError:
                if self.hotkey and hasattr(key, 'char') and key.char and key.char == self.hotkey:
                    self.toggle_clicking()
        
        self.hotkey_listener = Listener(on_press=on_press)
        self.hotkey_listener.start()
    
    def restart_hotkey_listener(self):
        """Restart the hotkey listener with new hotkey"""
        self.start_hotkey_listener()
    
    def generate_delay(self):
        """Generate a delay value based on the current distribution settings"""
        min_delay = self.abs_delay_min.get()
        max_delay = self.abs_delay_max.get()
        target = self.delay_target.get()
        deviation = self.delay_deviation.get()
        weighted = self.weighted_distribution.get()
        
        if weighted:
            # Log-normal distribution (right-shifted)
            if HAS_NUMPY:
                # Convert target to log space parameters
                mu = math.log(target)
                sigma = deviation / target  # Relative deviation
                # Generate log-normal sample
                delay = np.random.lognormal(mu, sigma)
            else:
                # Fallback: approximate log-normal with exponential bias
                normal_val = random.gauss(target, deviation)
                # Apply exponential skew to simulate log-normal
                skew_factor = random.expovariate(1.0 / (deviation * 0.1))
                delay = normal_val + skew_factor
        else:
            # Normal gaussian distribution
            if HAS_NUMPY:
                delay = np.random.normal(target, deviation)
            else:
                delay = random.gauss(target, deviation)
        
        # Clamp to absolute bounds
        delay = max(min_delay, min(max_delay, delay))
        
        return delay / 1000.0  # Convert to seconds
    
    def test_delay(self):
        """Generate and display sample delays"""
        samples = [self.generate_delay() * 1000 for _ in range(10)]
        avg_delay = sum(samples) / len(samples)
        
        preview_text = f"Sample delays (ms): {[round(d, 1) for d in samples[:5]]}...\nAverage: {avg_delay:.1f}ms"
        self.preview_label.config(text=preview_text)
    
    def click_loop(self):
        """Main clicking loop"""
        while self.is_clicking:
            delay = self.generate_delay()
            time.sleep(delay)
            
            if self.is_clicking:  # Check again in case it was stopped during delay
                if HAS_PYAUTOGUI:
                    try:
                        pyautogui.click()
                    except:
                        pass  # Ignore click errors
                else:
                    # Simulate click for testing
                    print(f"Simulated click (delay: {delay*1000:.1f}ms)")
    
    def toggle_clicking(self):
        """Toggle the autoclicker on/off"""
        if self.is_clicking:
            self.stop_clicking()
        else:
            self.start_clicking()
    
    def start_clicking(self):
        """Start the autoclicker"""
        if not self.is_clicking:
            # Validate settings
            if self.abs_delay_min.get() >= self.abs_delay_max.get():
                messagebox.showerror("Error", "Minimum delay must be less than maximum delay")
                return
            
            if not (self.abs_delay_min.get() <= self.delay_target.get() <= self.abs_delay_max.get()):
                messagebox.showwarning("Warning", "Target delay is outside min/max range")
            
            self.is_clicking = True
            self.status_label.config(text="Status: Running", foreground="green")
            self.start_stop_btn.config(text="Stop Clicking")
            
            # Start clicking in a separate thread
            self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
            self.click_thread.start()
    
    def stop_clicking(self):
        """Stop the autoclicker"""
        self.is_clicking = False
        self.status_label.config(text="Status: Stopped", foreground="red")
        self.start_stop_btn.config(text="Start Clicking")
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_clicking()
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.root.destroy()

class HotkeyDialog:
    def __init__(self, parent):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Set Hotkey")
        self.dialog.geometry("300x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        frame = ttk.Frame(self.dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Press any key to set as hotkey:").pack(pady=10)
        
        self.key_label = ttk.Label(frame, text="Waiting for key...", font=("Arial", 12, "bold"))
        self.key_label.pack(pady=10)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Hotkey", command=self.clear_hotkey).pack(side=tk.LEFT, padx=5)
        
        self.dialog.bind('<KeyPress>', self.on_key_press)
        self.dialog.focus_set()
    
    def on_key_press(self, event):
        key_name = event.keysym
        if key_name not in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R']:
            self.result = f"'{key_name}'"
            self.key_label.config(text=f"Selected: {key_name}")
            self.dialog.after(1000, self.dialog.destroy)
    
    def cancel(self):
        self.result = None
        self.dialog.destroy()
    
    def clear_hotkey(self):
        self.result = "None"
        self.dialog.destroy()

def main():
    # Check and warn about missing dependencies
    missing_deps = []
    if not HAS_NUMPY:
        missing_deps.append("numpy")
    if not HAS_PYAUTOGUI:
        missing_deps.append("pyautogui")
    if not HAS_PYNPUT:
        missing_deps.append("pynput")
    
    if missing_deps:
        print(f"\nWarning: Missing optional dependencies: {', '.join(missing_deps)}")
        print("For full functionality, install with:")
        print(f"pip install {' '.join(missing_deps)}")
        print("\nThe application will run with limited functionality.\n")
    
    # Disable pyautogui's fail-safe if available
    if HAS_PYAUTOGUI:
        pyautogui.FAILSAFE = True
    
    root = tk.Tk()
    app = AutoClicker(root)
    
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()