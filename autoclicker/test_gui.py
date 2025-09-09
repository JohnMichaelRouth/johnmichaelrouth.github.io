#!/usr/bin/env python3
"""
Simple test GUI to verify the basic tkinter interface works
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random

class SimpleAutoClickerTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker Test - Basic GUI")
        self.root.geometry("400x300")
        
        # State variables
        self.is_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Auto Clicker Test", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Min delay
        ttk.Label(config_frame, text="Min Delay (ms):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.min_delay_var = tk.DoubleVar(value=50)
        min_spinbox = ttk.Spinbox(config_frame, from_=1, to=5000, textvariable=self.min_delay_var, width=10)
        min_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Max delay
        ttk.Label(config_frame, text="Max Delay (ms):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.max_delay_var = tk.DoubleVar(value=200)
        max_spinbox = ttk.Spinbox(config_frame, from_=1, to=5000, textvariable=self.max_delay_var, width=10)
        max_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Status: Stopped", foreground="red")
        self.status_label.pack()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.start_stop_btn = ttk.Button(button_frame, text="Start Test", command=self.toggle_test)
        self.start_stop_btn.pack(side=tk.LEFT, padx=5)
        
        test_btn = ttk.Button(button_frame, text="Test Delay", command=self.test_delay)
        test_btn.pack(side=tk.LEFT, padx=5)
        
        # Output
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = tk.Text(output_frame, height=8, width=50)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
    def log_message(self, message):
        """Add a message to the output text"""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        
    def test_delay(self):
        """Test the delay generation"""
        min_delay = self.min_delay_var.get()
        max_delay = self.max_delay_var.get()
        
        if min_delay >= max_delay:
            messagebox.showerror("Error", "Min delay must be less than max delay")
            return
            
        # Generate some test delays
        delays = []
        for _ in range(10):
            delay = random.uniform(min_delay, max_delay)
            delays.append(round(delay, 1))
        
        avg_delay = sum(delays) / len(delays)
        self.log_message(f"Test delays: {delays}")
        self.log_message(f"Average: {avg_delay:.1f}ms")
        
    def test_loop(self):
        """Simulated clicking loop for testing"""
        click_count = 0
        while self.is_running and click_count < 20:  # Limited for testing
            min_delay = self.min_delay_var.get()
            max_delay = self.max_delay_var.get()
            delay = random.uniform(min_delay, max_delay) / 1000.0  # Convert to seconds
            
            time.sleep(delay)
            
            if self.is_running:
                click_count += 1
                self.log_message(f"Simulated click #{click_count} (delay: {delay*1000:.1f}ms)")
        
        if self.is_running:  # If we finished the loop naturally
            self.stop_test()
            self.log_message("Test completed (20 clicks)")
    
    def toggle_test(self):
        """Toggle the test on/off"""
        if self.is_running:
            self.stop_test()
        else:
            self.start_test()
    
    def start_test(self):
        """Start the test"""
        min_delay = self.min_delay_var.get()
        max_delay = self.max_delay_var.get()
        
        if min_delay >= max_delay:
            messagebox.showerror("Error", "Min delay must be less than max delay")
            return
        
        self.is_running = True
        self.status_label.config(text="Status: Running", foreground="green")
        self.start_stop_btn.config(text="Stop Test")
        
        self.log_message("Starting test...")
        
        # Start test in a separate thread
        test_thread = threading.Thread(target=self.test_loop, daemon=True)
        test_thread.start()
    
    def stop_test(self):
        """Stop the test"""
        self.is_running = False
        self.status_label.config(text="Status: Stopped", foreground="red")
        self.start_stop_btn.config(text="Start Test")
        self.log_message("Test stopped")

def main():
    root = tk.Tk()
    app = SimpleAutoClickerTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()