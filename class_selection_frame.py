# class_selection_frame.py
"""
Defines the GUI Frame for the class selection scene.
"""
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
from game_data import CLASSES

class ClassSelectionFrame(ttk.Frame):
    """Manages the class selection frame."""

    def __init__(self, parent, callbacks):
        super().__init__(parent)
        self.callbacks = callbacks # e.g., {'back': on_back, 'confirm': on_confirm}

        self.player_name = ""
        self.selected_class = None

        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the class selection frame."""
        ttk.Label(self, text="Charakter erstellen", font=("Helvetica", 16)).pack(pady=20)

        # Name Entry
        name_frame = ttk.Frame(self)
        name_frame.pack(pady=10)
        ttk.Label(name_frame, text="Name des Helden:").pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(name_frame, width=30)
        self.name_entry.pack(side=tk.LEFT)

        # Class Selection
        ttk.Label(self, text="Wähle deine Klasse:", font=("Helvetica", 12)).pack(pady=(20, 10))
        self.class_var = tk.StringVar()
        class_options_frame = ttk.Frame(self)
        class_options_frame.pack()
        for class_name in CLASSES.keys():
            rb = ttk.Radiobutton(class_options_frame, text=class_name, variable=self.class_var, value=class_name, command=self.show_class_info)
            rb.pack(side=tk.LEFT, padx=10)

        # Class Info - Reorganized to include an image
        self.info_frame = ttk.LabelFrame(self, text="Klasseninfo", padding="10")
        self.info_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)

        # Image Label on the left
        self.image_label = ttk.Label(self.info_frame)
        self.image_label.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.NW)
        self.character_image = None # To hold a reference to the PhotoImage

        # Text Info on the right
        text_info_frame = ttk.Frame(self.info_frame)
        text_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        self.desc_label = ttk.Label(text_info_frame, text="", wraplength=380)
        self.desc_label.pack(anchor=tk.W, pady=5)
        self.attr_label = ttk.Label(text_info_frame, text="", font=("Courier", 10))
        self.attr_label.pack(anchor=tk.W, pady=5)


        # Action Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)

        self.confirm_button = ttk.Button(button_frame, text="Abenteuer beginnen", command=self.confirm, state=tk.DISABLED)
        self.confirm_button.pack(side=tk.RIGHT)

        back_button = ttk.Button(button_frame, text="Zurück zum Hauptmenü", command=self.callbacks['back'])
        back_button.pack(side=tk.RIGHT, padx=(0, 10))

    def show_class_info(self):
        """Displays information and the image for the selected class."""
        class_name = self.class_var.get()
        if not class_name:
            return

        class_data = CLASSES[class_name]

        # Update text labels
        self.desc_label.config(text=class_data["description"])
        attr_text = "Start-Attribute:\n"
        for stat, value in class_data["attributes"].items():
            attr_text += f"  - {stat:<12}: {value}\n"
        self.attr_label.config(text=attr_text)

        # Update image
        try:
            img = Image.open(class_data["image_path"])
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            self.character_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.character_image)
        except (FileNotFoundError, KeyError):
            # If image is missing or path not defined, clear the label
            self.image_label.config(image='')
            self.character_image = None # Clear reference

        self.confirm_button.config(state=tk.NORMAL)

    def confirm(self):
        """Confirms the selection and calls the callback."""
        self.player_name = self.name_entry.get()
        if not self.player_name:
            simpledialog.messagebox.showwarning("Fehlender Name", "Bitte gib einen Namen für deinen Helden ein.", parent=self)
            return

        self.selected_class = self.class_var.get()
        if self.callbacks['confirm']:
            self.callbacks['confirm'](self.player_name, self.selected_class)