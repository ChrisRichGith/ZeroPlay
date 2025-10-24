# rpg_gui.py
"""
Defines the main game GUI frame.
"""
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random
from PIL import Image, ImageTk

from character import Character
from quest import Quest
from trader import Trader
from trader_gui import TraderWindow
from save_load_system import save_game
from utils import format_currency, center_window

# Liste verfügbarer Quests
AVAILABLE_QUESTS = [
    "Rette eine Prinzessin aus einem anderen Schloss",
    "Sammle 10 leere Flaschen für den Alchemisten",
    "Poliere die Rüstung des Königs (ohne Bezahlung)",
    "Entwirre die Kopfhörer des Barden",
    "Finde das Rezept für ewige Jugend (und verliere es wieder)",
    "Bringe dem königlichen Papagei das Fluchen bei",
    "Zähle alle Sandkörner am Strand",
    "Sortiere die Bibliothek nach der Farbe der Buchrücken",
    "Überzeuge einen Drachen, dass er nur ein überdimensionierter Wellensittich ist",
    "Finde heraus, warum Goblins immer so schlechte Laune haben",
    "Eskortiere eine sehr langsame Schildkröte über eine sehr breite Straße",
    "Störe eine wichtige Zeremonie durch lautes Kauen"
]

class RpgGui(ttk.Frame):
    """Manages the main game GUI frame."""

    def __init__(self, parent, character, callbacks):
        """Initializes the GUI with a character object."""
        super().__init__(parent)
        self.callbacks = callbacks

        self.player = character
        self.trader = Trader()
        self.current_quest = None
        self.is_auto_questing = False
        self.game_over = False

        self._setup_string_vars()
        self.create_widgets()
        self.update_display()

    def _setup_string_vars(self):
        """Creates tkinter StringVars to link data to labels."""
        self.char_name_var = tk.StringVar()
        self.char_level_var = tk.StringVar()
        self.char_gold_var = tk.StringVar()
        self.stats_vars = {stat: tk.StringVar() for stat in ['Stärke', 'Intelligenz', 'Glück']}
        self.equipment_vars = {slot: tk.StringVar() for slot in ['Kopf', 'Brust', 'Waffe']}
        self.lp_label_var = tk.StringVar()
        self.mp_label_var = tk.StringVar()
        self.xp_label_var = tk.StringVar()

    def create_widgets(self):
        """Creates and places all the widgets in the window."""
        # Main layout grid
        self.columnconfigure(0, weight=1, uniform="char_inv_group") # Character status
        self.columnconfigure(1, weight=0) # Actions (narrow)
        self.columnconfigure(2, weight=1, uniform="char_inv_group") # Inventory
        self.rowconfigure(0, weight=1) # Top area
        self.rowconfigure(1, weight=0) # Bottom area for the log

        # Create main frames for each section
        char_frame_container = ttk.Frame(self)
        char_frame_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        actions_frame = ttk.Frame(self)
        actions_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        inventory_frame = ttk.Frame(self)
        inventory_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        inventory_frame.rowconfigure(0, weight=1)
        inventory_frame.columnconfigure(0, weight=1)


        log_frame = ttk.Frame(self)
        log_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=(0, 10))

        # Populate the frames
        self._create_character_frame(char_frame_container)
        self._create_actions_frame(actions_frame)

        # Create and populate the notebook for equipment and inventory
        notebook = ttk.Notebook(inventory_frame)
        notebook.grid(row=0, column=0, sticky="nsew")
        equipment_tab = ttk.Frame(notebook)
        inventory_tab = ttk.Frame(notebook)
        notebook.add(equipment_tab, text='Ausrüstung')
        notebook.add(inventory_tab, text='Inventar')

        self._create_equipment_frame(equipment_tab)
        self._create_inventory_frame(inventory_tab)

        self._create_log_frame(log_frame)

    def _create_character_frame(self, parent):
        char_frame = ttk.LabelFrame(parent, text="Charakterstatus", padding="10")
        char_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10), anchor='n')
        char_frame.columnconfigure(2, weight=1) # Allow portrait column to expand

        # --- Left side: Stats ---
        labels = {"Name:": self.char_name_var, "Level:": self.char_level_var, "Gold:": self.char_gold_var}
        for i, (text, var) in enumerate(labels.items()):
            ttk.Label(char_frame, text=text).grid(row=i, column=0, sticky="w")
            ttk.Label(char_frame, textvariable=var).grid(row=i, column=1, sticky="w")

        attr_frame = ttk.LabelFrame(char_frame, text="Attribute", padding="5")
        attr_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        for i, (stat, var) in enumerate(self.stats_vars.items()):
            ttk.Label(attr_frame, text=f"{stat}:").grid(row=i, column=0, sticky="w")
            ttk.Label(attr_frame, textvariable=var).grid(row=i, column=1, sticky="w", padx=5)

        for i, (text, var_name) in enumerate([("Lebenspunkte", "lp"), ("Manapunkte", "mp"), ("Erfahrung", "xp")]):
            frame = ttk.LabelFrame(char_frame, text=text, padding=5)
            frame.grid(row=4+i, column=0, columnspan=2, sticky="ew", pady=(5, 0))
            bar = ttk.Progressbar(frame, orient='horizontal', mode='determinate')
            bar.pack(fill=tk.X, expand=True)
            label_var = getattr(self, f"{var_name}_label_var")
            ttk.Label(frame, textvariable=label_var, anchor="center").pack()
            setattr(self, f"{var_name}_bar", bar)

        # --- Right side: Portrait ---
        self.portrait_label = ttk.Label(char_frame)
        self.portrait_label.grid(row=0, column=2, rowspan=7, sticky="nsew", padx=(20, 0))

        try:
            if self.player.image_path:
                img = Image.open(self.player.image_path)
                img.thumbnail((220, 280))  # Resize image to fit
                photo_img = ImageTk.PhotoImage(img)

                self.portrait_label.config(image=photo_img)
                # Keep a reference to the image to prevent it from being garbage collected
                self.portrait_label.image = photo_img
        except FileNotFoundError:
            self.portrait_label.config(text=f"Bild nicht\ngefunden:\n{self.player.image_path}")
        except Exception as e:
            self.portrait_label.config(text=f"Fehler beim\nLaden des Bildes:\n{e}")

    def _create_actions_frame(self, parent):
        actions_frame = ttk.LabelFrame(parent, text="Aktionen", padding="10")
        actions_frame.pack(fill=tk.Y, expand=False, anchor='n')

        self.quest_button = ttk.Button(actions_frame, text="Neue Quest beginnen", command=self.start_quest)
        self.quest_button.pack(fill=tk.X, pady=5)
        self.auto_quest_button = ttk.Button(actions_frame, text="Auto-Quest starten", command=self.toggle_auto_quest)
        self.auto_quest_button.pack(fill=tk.X, pady=5)
        self.trader_button = ttk.Button(actions_frame, text="Händler besuchen", command=self.open_trader_window)
        self.trader_button.pack(fill=tk.X, pady=5)
        self.equip_button = ttk.Button(actions_frame, text="Gegenstand ausrüsten", command=self.equip_item)
        self.equip_button.pack(fill=tk.X, pady=5)
        self.use_button = ttk.Button(actions_frame, text="Gegenstand benutzen", command=self.use_item)
        self.use_button.pack(fill=tk.X, pady=5)
        self.progress_bar = ttk.Progressbar(actions_frame, orient='horizontal', mode='determinate', length=120)
        self.progress_bar.pack(fill=tk.X, pady=(10, 5))

        self.loot_status_text = tk.Text(actions_frame, height=2, wrap=tk.WORD, bg="lightgrey", relief="flat", fg="gray")
        self.loot_status_text.pack(fill=tk.X, pady=5)
        self.loot_status_text.config(state=tk.DISABLED)

    def _create_log_frame(self, parent):
        """Creates the quest log text widget."""
        log_labelframe = ttk.LabelFrame(parent, text="Log", padding="10")
        log_labelframe.pack(fill=tk.X, expand=True)

        log_labelframe.rowconfigure(0, weight=1)
        log_labelframe.columnconfigure(0, weight=1)

        self.quest_log = tk.Text(log_labelframe, height=10, wrap=tk.WORD, bg="#2B2B2B", fg="white", relief="flat")
        self.quest_log.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_labelframe, orient=tk.VERTICAL, command=self.quest_log.yview)
        self.quest_log.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.quest_log.config(state=tk.DISABLED)

    def _create_equipment_frame(self, parent):
        parent.columnconfigure(1, weight=1)
        equip_frame = ttk.LabelFrame(parent, text="Angelegte Ausrüstung", padding="10")
        equip_frame.pack(fill=tk.X, padx=10, pady=10)
        for i, (slot, var) in enumerate(self.equipment_vars.items()):
            ttk.Label(equip_frame, text=f"{slot}:").grid(row=i, column=0, sticky="w")
            ttk.Label(equip_frame, textvariable=var).grid(row=i, column=1, sticky="w", padx=5)

    def _create_inventory_frame(self, parent):
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.inv_frame = ttk.LabelFrame(parent, text="Rucksack", padding="10")
        self.inv_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.inv_frame.rowconfigure(0, weight=1)
        self.inv_frame.columnconfigure(0, weight=1)
        self.inventory_listbox = tk.Listbox(self.inv_frame, bg="#2B2B2B", fg="white", selectbackground="#0078D7")
        self.inventory_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(self.inv_frame, orient=tk.VERTICAL, command=self.inventory_listbox.yview)
        self.inventory_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.inventory_listbox.bind('<<ListboxSelect>>', self.update_button_states)
        self.inventory_listbox.bind('<Double-1>', self.on_item_double_click)

        self.tooltip = Tooltip(self.inventory_listbox, self.get_tooltip_text)

    def get_tooltip_text(self):
        """Callback function to get the text for the tooltip."""
        try:
            # Get the item under the mouse cursor
            _, y, _, _ = self.inventory_listbox.bbox(self.inventory_listbox.curselection()[0])
            index = self.inventory_listbox.nearest(y)
            item = self.player.inventory[index]

            # Format the text
            text = f"{item.name}\n"
            text += f"Typ: {item.item_type} ({item.slot})\n"
            text += f"Wert: {format_currency(item.value)}\n\n"
            for stat, value in item.stats_boost.items():
                text += f"{stat}: +{value}\n"
            return text.strip()
        except (IndexError, tk.TclError):
            return ""

    def update_display(self):
        self.char_name_var.set(f"{self.player.name} ({self.player.klasse})")
        self.char_level_var.set(self.player.level)
        self.char_gold_var.set(format_currency(self.player.copper))
        total_stats = self.player.get_total_stats()
        for stat, var in self.stats_vars.items():
            base = self.player.attributes.get(stat, 0)
            total = total_stats.get(stat, 0)
            bonus = total - base
            var.set(f"{total} ({base} {'+' if bonus >= 0 else ''}{bonus})") if bonus != 0 else var.set(total)
        for slot, var in self.equipment_vars.items():
            item = self.player.equipment.get(slot)
            var.set(item.name if item else "Leer")
        self.inv_frame.config(text=f"Inventar ({len(self.player.inventory)}/{self.player.max_inventory_size})")
        self.inventory_listbox.delete(0, tk.END)
        for i, item in enumerate(self.player.inventory):
            item_text = str(item)
            if self.player.is_upgrade(item):
                item_text = "⭐ " + item_text
            self.inventory_listbox.insert(tk.END, item_text)
            self.inventory_listbox.itemconfig(i, {'fg': item.color})

        self.lp_label_var.set(f"{self.player.current_lp} / {self.player.max_lp} LP")
        self.lp_bar['value'] = (self.player.current_lp / self.player.max_lp) * 100 if self.player.max_lp > 0 else 0
        self.mp_label_var.set(f"{self.player.current_mp} / {self.player.max_mp} MP")
        self.mp_bar['value'] = (self.player.current_mp / self.player.max_mp) * 100 if self.player.max_mp > 0 else 0
        self.xp_label_var.set(f"{self.player.xp} / {self.player.xp_to_next_level} XP")
        self.xp_bar['value'] = (self.player.xp / self.player.xp_to_next_level) * 100 if self.player.xp_to_next_level > 0 else 0
        self.update_button_states()
        self.update_idletasks()

    def add_to_log(self, message):
        self.quest_log.config(state=tk.NORMAL)
        self.quest_log.insert(tk.END, message + "\n")
        self.quest_log.see(tk.END)
        self.quest_log.config(state=tk.DISABLED)

    def set_loot_text(self, text):
        self.loot_status_text.config(state=tk.NORMAL)
        self.loot_status_text.delete("1.0", tk.END)
        self.loot_status_text.insert("1.0", text)
        self.loot_status_text.config(state=tk.DISABLED)

    def toggle_auto_quest(self):
        self.is_auto_questing = not self.is_auto_questing
        if self.is_auto_questing:
            self.auto_quest_button.config(text="Auto-Quest stoppen")
            self.set_loot_text("Auto-Quest Modus aktiv...")
            self.start_quest()
        else:
            self.auto_quest_button.config(text="Auto-Quest starten")
            self.set_loot_text("Auto-Quest Modus gestoppt.")

    def start_quest(self):
        if self.current_quest:
            if not self.is_auto_questing:
                messagebox.showwarning("Quest aktiv", "Bitte schließe erst die aktuelle Quest ab.")
            return
        if len(self.player.inventory) >= self.player.max_inventory_size:
            self.set_loot_text("Inventar voll! Auto-Quest gestoppt.")
            messagebox.showinfo("Inventar voll", "Dein Inventar ist voll. Besuche den Händler!")
            if self.is_auto_questing:
                self.toggle_auto_quest()
            return
        quest_desc = random.choice(AVAILABLE_QUESTS)
        self.current_quest = Quest(quest_desc)
        self.add_to_log(f"Neue Quest: {quest_desc}")
        self.progress_bar['value'] = 0
        self.update_display()
        self.advance_quest()

    def advance_quest(self):
        if self.current_quest is None: return
        event_message = self.current_quest.advance(self.player)
        # Only log the final message when the quest is complete
        if event_message and self.current_quest.is_complete():
            self.add_to_log(event_message)

        if self.player.current_lp <= 0:
            self.handle_game_over()
            return
        if self.player.current_lp / self.player.max_lp < 0.1:
            if self.is_auto_questing:
                self.toggle_auto_quest()
                messagebox.showwarning("Niedrige Lebenspunkte!", "Deine Lebenspunkte sind kritisch niedrig! Auto-Quest pausiert. Heile dich!")
        if self.current_quest.is_complete():
            gold, xp, item = self.current_quest.generate_reward(self.player)
            item_added = self.player.add_loot(gold, item)
            level_up_info = self.player.add_xp(xp)
            loot_message = f"Loot: {format_currency(gold)}, {xp} XP"
            if item:
                loot_message += f" und '{item.name}'" if item_added else f" (aber '{item.name}' passte nicht ins Inventar!)"
            self.set_loot_text(loot_message)
            if level_up_info:
                level_up_summary = f"Level Up! Du bist jetzt Level {self.player.level}!\n\nAttribut-Boni:\n" + "\n".join(level_up_info)
                CountdownDialog(self, title="Level Aufstieg!", message=level_up_summary)
            self.current_quest = None
            self.progress_bar['value'] = 0
            if self.is_auto_questing:
                self.master.after(1000, self.start_quest)
        else:
            progress_percent = (self.current_quest.progress / self.current_quest.duration) * 100
            self.progress_bar['value'] = progress_percent
            self.master.after(150, self.advance_quest)
        self.update_display()

    def equip_item(self):
        selected_indices = self.inventory_listbox.curselection()
        if not selected_indices: return
        item_index = selected_indices[0]
        self.player.equip(item_index)
        self.update_display()

    def use_item(self):
        selected_indices = self.inventory_listbox.curselection()
        if not selected_indices: return
        item_index = selected_indices[0]
        success, message = self.player.use_item(item_index)
        if not success:
            messagebox.showwarning("Fehler", message)
        self.update_display()

    def on_item_double_click(self, event=None):
        """Handles double-click events on the inventory listbox."""
        selected_indices = self.inventory_listbox.curselection()
        if not selected_indices:
            return

        item_index = selected_indices[0]
        selected_item = self.player.inventory[item_index]

        if selected_item.item_type == "Ausrüstung":
            self.equip_item()
        elif selected_item.item_type == "Verbrauchsgut":
            self.use_item()

    def update_button_states(self, event=None):
        is_questing = self.current_quest is not None
        selected_indices = self.inventory_listbox.curselection()
        self.quest_button.config(state=tk.DISABLED if is_questing else tk.NORMAL)
        self.trader_button.config(state=tk.DISABLED if is_questing else tk.NORMAL)
        self.auto_quest_button.config(state=tk.DISABLED if is_questing and not self.is_auto_questing else tk.NORMAL)
        if not selected_indices:
            self.equip_button.config(state=tk.DISABLED)
            self.use_button.config(state=tk.DISABLED)
            return
        item_index = selected_indices[0]
        selected_item = self.player.inventory[item_index]
        if selected_item.item_type == "Ausrüstung":
            self.equip_button.config(state=tk.NORMAL)
            self.use_button.config(state=tk.DISABLED)
        elif selected_item.item_type == "Verbrauchsgut":
            self.equip_button.config(state=tk.DISABLED)
            self.use_button.config(state=tk.NORMAL)
        else:
            self.equip_button.config(state=tk.DISABLED)
            self.use_button.config(state=tk.DISABLED)

    def open_trader_window(self):
        self.trader_button.config(state=tk.DISABLED)
        TraderWindow(self, self.player, self.trader, on_close_callback=self.on_trader_close)

    def on_trader_close(self):
        self.update_display()
        self.trader_button.config(state=tk.NORMAL)

    def handle_game_over(self):
        self.game_over = True
        messagebox.showerror("Game Over", f"Du bist auf Level {self.player.level} gestorben. Ein neuer Held wird rekrutiert.")
        if self.callbacks['game_over']:
            self.callbacks['game_over']()

class Tooltip:
    """
    Create a tooltip for a given widget.
    """
    def __init__(self, widget, text_callback):
        self.widget = widget
        self.text_callback = text_callback
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<Motion>", self.motion)

    def enter(self, event=None):
        # Store the mouse position
        self.x = event.x_root
        self.y = event.y_root
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def motion(self, event=None):
        # Update the mouse position
        self.x = event.x_root
        self.y = event.y_root
        # If the tooltip is already visible, move it
        if self.tip_window:
            self.tip_window.wm_geometry(f"+{self.x + 25}+{self.y + 20}")

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self):
        text = self.text_callback()
        if not text:
            return

        # Use the stored mouse coordinates
        x = self.x + 25
        y = self.y + 20

        # Create the tooltip window if it doesn't exist
        if self.tip_window is None:
            self.tip_window = tk.Toplevel(self.widget)
            self.tip_window.wm_overrideredirect(True)
            label = tk.Label(self.tip_window, text=text, justify=tk.LEFT,
                             background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                             font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)

        self.tip_window.wm_geometry(f"+{x}+{y}")

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

class CountdownDialog(tk.Toplevel):
    """A modal dialog with a countdown timer that closes automatically."""
    def __init__(self, parent, title, message, countdown=5):
        super().__init__(parent)
        self.title(title)
        self.message = message
        self.countdown = countdown
        self.parent = parent

        # Make window modal
        self.transient(parent)
        self.grab_set()

        # UI Elements
        ttk.Label(self, text=self.message, wraplength=300, justify=tk.LEFT).pack(padx=20, pady=10)

        self.countdown_label = ttk.Label(self, text=f"Schließt in {self.countdown} Sekunden...")
        self.countdown_label.pack(pady=5)

        ok_button = ttk.Button(self, text="OK", command=self.destroy)
        ok_button.pack(pady=10, padx=20, fill=tk.X)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Center the window
        self.update_idletasks()
        center_window(self)

        # Start the countdown
        self.update_countdown()

    def update_countdown(self):
        if self.countdown > 0:
            self.countdown_label.config(text=f"Schließt in {self.countdown} Sekunden...")
            self.countdown -= 1
            self._after_id = self.after(1000, self.update_countdown)
        else:
            self.destroy()

    def destroy(self):
        # Cancel the pending `after` call before destroying the window
        if hasattr(self, '_after_id'):
            self.after_cancel(self._after_id)
        super().destroy()