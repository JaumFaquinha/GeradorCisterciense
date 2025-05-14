import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw

class CistercianNumerals:
    def __init__(self):
        # Directory where component images are stored
        self.components_dir = "cistercian_components"
        
        # Load all component images
        self.components = {
            'units': {},
            'tens': {},
            'hundreds': {},
            'thousands': {}
        }
        
        # Create directory if it doesn't exist
        if not os.path.exists(self.components_dir):
            os.makedirs(self.components_dir)
            messagebox.showwarning("Component Directory Created", 
                                  f"Please place your component images in: {os.path.abspath(self.components_dir)}")
        
        # Load component images
        self._load_components()
        
    def _load_components(self):
        """Load all component images from the components directory"""
        for digit in range(1, 10):
            # Try to load unit component (1-9)
            unit_path = os.path.join(self.components_dir, f"unit_{digit}.png")
            if os.path.exists(unit_path):
                self.components['units'][digit] = Image.open(unit_path)
            
            # Try to load ten component (10-90)
            ten_path = os.path.join(self.components_dir, f"ten_{digit}0.png")
            if os.path.exists(ten_path):
                self.components['tens'][digit] = Image.open(ten_path)
            
            # Try to load hundred component (100-900)
            hundred_path = os.path.join(self.components_dir, f"hundred_{digit}00.png")
            if os.path.exists(hundred_path):
                self.components['hundreds'][digit] = Image.open(hundred_path)
            
            # Try to load thousand component (1000-9000)
            thousand_path = os.path.join(self.components_dir, f"thousand_{digit}000.png")
            if os.path.exists(thousand_path):
                self.components['thousands'][digit] = Image.open(thousand_path)
    
    def generate_numeral(self, number):
        """Generate a Cistercian numeral image by combining component images"""
        if number < 1 or number > 9999:
            raise ValueError("Number must be between 1 and 9999")
            
        # Create a blank white image (200x200)
        img_size = 200
        final_img = Image.new("RGBA", (img_size, img_size), (255, 255, 255, 255))
        
        # Get each digit (thousands, hundreds, tens, units)
        digits = [int(d) for d in f"{number:04d}"]
        
        # Combine components in order (units on top)
        if digits[0] != 0 and digits[0] in self.components['thousands']:
            final_img = self._overlay_component(final_img, self.components['thousands'][digits[0]])
        
        if digits[1] != 0 and digits[1] in self.components['hundreds']:
            final_img = self._overlay_component(final_img, self.components['hundreds'][digits[1]])
        
        if digits[2] != 0 and digits[2] in self.components['tens']:
            final_img = self._overlay_component(final_img, self.components['tens'][digits[2]])
        
        if digits[3] != 0 and digits[3] in self.components['units']:
            final_img = self._overlay_component(final_img, self.components['units'][digits[3]])
        
        return final_img.convert("RGB")  # Convert to RGB for compatibility
    
    def _overlay_component(self, base_img, overlay_img):
        """Overlay a component image onto the base image"""
        # Resize overlay to match base if needed
        if overlay_img.size != base_img.size:
            overlay_img = overlay_img.resize(base_img.size)
        
        # Create a new image by pasting the overlay onto the base
        combined = Image.new("RGBA", base_img.size)
        combined.paste(base_img, (0, 0))
        combined.paste(overlay_img, (0, 0), overlay_img)
        return combined

   
    

class CistercianApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cistercian Numerals Converter (Component-Based)")
        
        self.cn = CistercianNumerals()
        
        # Create tabs
        self.tab_control = ttk.Notebook(root)
        
        self.tab_generate = ttk.Frame(self.tab_control)
        self.tab_recognize = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_generate, text="Generate Numeral")
        self.tab_control.pack(expand=1, fill="both")
        
        # Setup generate tab
        self.setup_generate_tab()
        
    def setup_generate_tab(self):
        """Setup the numeral generation tab"""
        frame = ttk.Frame(self.tab_generate)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Input field
        ttk.Label(frame, text="Enter Arabic number (1-9999):").grid(row=0, column=0, sticky="w")
        self.arabic_input = ttk.Entry(frame)
        self.arabic_input.grid(row=0, column=1, sticky="ew")
        
        # Generate button
        generate_btn = ttk.Button(frame, text="Generate", command=self.generate_numeral)
        generate_btn.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Result display
        self.result_frame = ttk.Frame(frame)
        self.result_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        # Configure grid weights
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
       
    def generate_numeral(self):
        """Generate and display the Cistercian numeral"""
        try:
            number = int(self.arabic_input.get())
            if number < 1 or number > 9999:
                raise ValueError("Number out of range")
                
            # Clear previous results
            for widget in self.result_frame.winfo_children():
                widget.destroy()
                
            # Generate the numeral image
            img = self.cn.generate_numeral(number)
            
            # Convert to Tkinter format
            tk_img = ImageTk.PhotoImage(img)
            
            # Display images side by side
            left_frame = ttk.Frame(self.result_frame)
            left_frame.pack(side="left", padx=10, pady=10)
            
            right_frame = ttk.Frame(self.result_frame)
            right_frame.pack(side="left", padx=10, pady=10)
            
            # Arabic number
            ttk.Label(left_frame, text=f"Arabic: {number}", font=("Arial", 14)).pack()
            
            # Cistercian numeral
            ttk.Label(left_frame, text="Cistercian:").pack()
            img_label = ttk.Label(left_frame, image=tk_img)
            img_label.image = tk_img  # Keep a reference
            img_label.pack()
            
            # Add location information
            ttk.Label(right_frame, text="Digit Components:", font=("Arial", 12, "bold")).pack(anchor="w")
            
            digits = [int(d) for d in f"{number:04d}"]
            positions = ["Thousands", "Hundreds", "Tens", "Units"]
            
            for i in range(4):
                if digits[i] != 0:
                    ttk.Label(right_frame, 
                             text=f"{positions[i]}: {digits[i] * (10 ** (3-i))}").pack(anchor="w")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            
    def browse_image(self):
        """Open a file dialog to select an image"""
        file_path = filedialog.askopenfilename(
            title="Select Cistercian Numeral Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        if file_path:
            self.image_path.set(file_path)
            

if __name__ == "__main__":
    root = tk.Tk()
    app = CistercianApp(root)
    root.mainloop()