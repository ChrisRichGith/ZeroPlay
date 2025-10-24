# rpg_gui.py
"""
Defines the main game GUI frame.
"""
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random
import os
try:
    from PIL import Image, ImageTk
except ImportError:
    messagebox.showerror("Abhängigkeit fehlt", "Pillow ist nicht installiert. Bilder werden nicht angezeigt.\nBitte 'pip install Pillow' ausführen.")
    Image = None
    ImageTk = None

from character import Character
from quest import Quest
from trader import Trader
from trader_gui import TraderWindow
from save_load_system import save_game
from highscore_manager import save_highscore
from game_over_gui import GameOverWindow
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
        self.columnconfigure(0, weight=1, minsize=400)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        left_column_frame = ttk.Frame(self)
        left_column_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        left_column_frame.rowconfigure(1, weight=1)

        self._create_character_frame(left_column_frame)
        self._create_actions_frame(left_column_frame)

        right_column_frame = ttk.Frame(self)
        right_column_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_column_frame.rowconfigure(0, weight=3)
        right_column_frame.rowconfigure(1, weight=2)
        right_column_frame.columnconfigure(0, weight=1)

        self._create_portrait_frame(right_column_frame)

        notebook = ttk.Notebook(right_column_frame)
        notebook.grid(row=1, column=0, sticky="nsew", pady=(10,0))
        equipment_tab = ttk.Frame(notebook)
        inventory_tab = ttk.Frame(notebook)
        notebook.add(equipment_tab, text='Ausrüstung')
        notebook.add(inventory_tab, text='Inventar')
        self._create_equipment_frame(equipment_tab)
        self._create_inventory_frame(inventory_tab)

    def _create_portrait_frame(self, parent):
        portrait_frame = ttk.LabelFrame(parent, text="Porträt", padding="10")
        portrait_frame.grid(row=0, column=0, sticky="nsew")
        portrait_frame.columnconfigure(0, weight=1)
        portrait_frame.rowconfigure(0, weight=1)
        self.portrait_label = ttk.Label(portrait_frame, anchor="center")
        self.portrait_label.grid(row=0, column=0, sticky="nsew")

    def _create_character_frame(self, parent):
        char_frame = ttk.LabelFrame(parent, text="Charakterstatus", padding="10")
        char_frame.grid(row=0, column=0, sticky="ew")
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

    def _create_actions_frame(self, parent):
        actions_frame = ttk.LabelFrame(parent, text="Aktionen", padding="10")
        actions_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=2) # Give more space to the log

        # --- Button Column ---
        button_container = ttk.Frame(actions_frame)
        button_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        button_container.columnconfigure(0, weight=1)

        buttons = [("Neue Quest beginnen", self.start_quest), ("Auto-Quest starten", self.toggle_auto_quest),
                   ("Händler besuchen", self.open_trader_window), ("Gegenstand ausrüsten", self.equip_item),
                   ("Gegenstand benutzen", self.use_item)]
        for i, (text, command) in enumerate(buttons):
            button = ttk.Button(button_container, text=text, command=command)
            button.grid(row=i, column=0, sticky="ew", pady=2)
            setattr(self, f"{text.lower().replace(' ', '_')}_button", button)

        self.auto_quest_button = getattr(self, "auto-quest_starten_button")
        self.quest_button = getattr(self, "neue_quest_beginnen_button")
        self.trader_button = getattr(self, "händler_besuchen_button")
        self.equip_button = getattr(self, "gegenstand_ausrüsten_button")
        self.use_button = getattr(self, "gegenstand_benutzen_button")

        self.progress_bar = ttk.Progressbar(button_container, orient='horizontal', mode='determinate', length=200)
        self.progress_bar.grid(row=len(buttons), column=0, sticky="ew", pady=(10, 5))

        self.loot_status_text = tk.Text(button_container, height=2, wrap=tk.WORD, bg="#2B2B2B", fg="gold", relief="flat")
        self.loot_status_text.grid(row=len(buttons) + 1, column=0, sticky="ew", pady=(5, 0))
        self.loot_status_text.config(state=tk.DISABLED)

        # --- Quest Log Column ---
        log_frame = ttk.LabelFrame(actions_frame, text="Log", padding=5)
        log_frame.grid(row=0, column=1, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.quest_log = tk.Text(log_frame, wrap=tk.WORD, bg="#2B2B2B", fg="white", relief="flat")
        self.quest_log.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.quest_log.yview)
        self.quest_log.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.quest_log.config(state=tk.DISABLED)

    def _create_equipment_frame(self, parent):
        parent.columnconfigure(0, weight=1)
        equip_frame = ttk.LabelFrame(parent, text="Angelegte Ausrüstung", padding="10")
        equip_frame.grid(row=0, column=0, sticky="new", padx=10, pady=10)
        for i, (slot, var) in enumerate(self.equipment_vars.items()):
            ttk.Label(equip_frame, text=f"{slot}:").grid(row=i, column=0, sticky="w")
            ttk.Label(equip_frame, textvariable=var).grid(row=i, column=1, sticky="w", padx=5)

    def _create_inventory_frame(self, parent):
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.inv_frame = ttk.LabelFrame(parent, text="Rucksack", padding="10")
        self.inv_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
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

    def get_tooltip_text(self, index):
        try:
            item = self.player.inventory[index]
            text = f"{item.name} ({item.rarity})\n"
            if item.slot:
                text += f"Typ: {item.item_type} ({item.slot})\n"
            else:
                text += f"Typ: {item.item_type}\n"
            text += f"Wert: {format_currency(item.value)}\n"
            if item.stats_boost:
                text += "\n"
                for stat, value in item.stats_boost.items():
                    if item.item_type == "Verbrauchsgut":
                        text += f"Stellt {value} {stat} wieder her\n"
                    else:
                        text += f"{stat}: +{value}\n"
            return text.strip()
        except IndexError:
            return ""

    def _update_character_image(self, image_path):
        if not Image or not ImageTk:
            self.portrait_label.config(text="Bild-Bibliothek\nfehlt (Pillow)")
            return
        if not image_path or not os.path.exists(image_path):
            img = Image.new('RGBA', (220, 280), (60, 60, 60, 255))
        else:
            try:
                img = Image.open(image_path)
            except IOError:
                img = Image.new('RGBA', (220, 280), (255, 0, 0, 255))
        img.thumbnail((220, 280), Image.Resampling.LANCZOS)
        bg = Image.new('RGBA', (220, 280), (0, 0, 0, 0))
        paste_x = (bg.width - img.width) // 2
        paste_y = (bg.height - img.height) // 2
        bg.paste(img, (paste_x, paste_y))
        photo_img = ImageTk.PhotoImage(bg)
        self.portrait_label.config(image=photo_img)
        self.portrait_label.image = photo_img

    def update_display(self):
        self._update_character_image(self.player.image_path)
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
        if event_message:
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
        save_highscore(self.player)
        self._update_character_image('assets/tombstone.png')
        for widget in self.winfo_children():
            try:
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        child.config(state=tk.DISABLED)
            except tk.TclError:
                pass # Ignore errors for widgets that don't support 'state'
        GameOverWindow(self, self.player, on_close_callback=self.callbacks['game_over'])

class Tooltip:
    def __init__(self, widget, text_callback):
        self.widget = widget
        self.text_callback = text_callback
        self.tip_window = None
        self.id = None
        self.last_index = -1
        self.widget.bind("<Motion>", self.on_motion)
        self.widget.bind("<Leave>", self.on_leave)

    def on_motion(self, event):
        try:
            index = self.widget.nearest(event.y)
            bbox = self.widget.bbox(index)
            if not (bbox[0] < event.x < bbox[0] + bbox[2] and bbox[1] < event.y < bbox[1] + bbox[3]):
                self.on_leave()
                return
        except (tk.TclError, IndexError):
            self.on_leave()
            return
        if index != self.last_index:
            self.unschedule()
            self.hidetip()
            self.last_index = index
            self.id = self.widget.after(500, lambda: self.showtip(event, index))

    def on_leave(self, event=None):
        self.unschedule()
        self.hidetip()
        self.last_index = -1

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def showtip(self, event, index):
        text = self.text_callback(index)
        if not text:
            return
        x = event.x_root + 25
        y = event.y_root + 20
        if self.tip_window is None:
            self.tip_window = tk.Toplevel(self.widget)
            self.tip_window.wm_overrideredirect(True)
            label = tk.Label(self.tip_window, text=text, justify=tk.LEFT,
                             background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                             font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)
        self.tip_window.wm_geometry(f"+{x}+{y}")

    def hidetip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class CountdownDialog(tk.Toplevel):
    """A modal dialog with a countdown timer that closes automatically."""
    def __init__(self, parent, title, message, countdown=5):
        super().__init__(parent)
        self.title(title)
        self.message = message
        self.countdown = countdown
        self.parent = parent
        self.transient(parent)
        self.grab_set()
        ttk.Label(self, text=self.message, wraplength=300, justify=tk.LEFT).pack(padx=20, pady=10)
        self.countdown_label = ttk.Label(self, text=f"Schließt in {self.countdown} Sekunden...")
        self.countdown_label.pack(pady=5)
        ok_button = ttk.Button(self, text="OK", command=self.destroy)
        ok_button.pack(pady=10, padx=20, fill=tk.X)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.update_idletasks()
        center_window(self)
        self.update_countdown()

    def update_countdown(self):
        if self.countdown > 0:
            self.countdown_label.config(text=f"Schließt in {self.countdown} Sekunden...")
            self.countdown -= 1
            self._after_id = self.after(1000, self.update_countdown)
        else:
            self.destroy()

    def destroy(self):
        if hasattr(self, '_after_id'):
            self.after_cancel(self._after_id)
        super().destroy()