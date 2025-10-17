# rpg_gui.py
"""
Defines the main game GUI frame.
"""
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random

from character import Character
from quest import Quest
from trader import Trader
from trader_gui import TraderWindow
from save_load_system import save_game

# Liste verfügbarer Quests
AVAILABLE_QUESTS = [
    "Rette eine Prinzessin aus einem anderen Schloss",
    "Sammle 10 leere Flaschen für den Alchemisten",
    "Polere die Rüstung des Königs (ohne Bezahlung)",
    "Entwirre die Kopfhörer des Barden",
    "Finde das Rezept für ewige Jugend (und verliere es wieder)"
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
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left_pane = ttk.Frame(self, width=300)
        left_pane.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        right_pane = ttk.Frame(self)
        right_pane.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        right_pane.columnconfigure(0, weight=1)
        right_pane.rowconfigure(1, weight=1)

        self._create_character_frame(left_pane)
        self._create_actions_frame(left_pane)
        self._create_equipment_frame(right_pane)
        self._create_inventory_frame(right_pane)

    def _create_character_frame(self, parent):
        char_frame = ttk.LabelFrame(parent, text="Charakterstatus", padding="10")
        char_frame.pack(fill=tk.X, pady=(0, 10))
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
        actions_frame.pack(fill=tk.X)
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
        self.progress_bar = ttk.Progressbar(actions_frame, orient='horizontal', mode='determinate', length=200)
        self.progress_bar.pack(fill=tk.X, pady=(10, 5))

        # Quest Description Text Box
        self.quest_desc_text = tk.Text(actions_frame, height=3, wrap=tk.WORD, bg="lightgrey", relief="flat")
        self.quest_desc_text.pack(fill=tk.X, pady=5)
        self.quest_desc_text.config(state=tk.DISABLED)

        # Loot/Status Text Box
        self.loot_status_text = tk.Text(actions_frame, height=2, wrap=tk.WORD, bg="lightgrey", relief="flat", fg="gray")
        self.loot_status_text.pack(fill=tk.X, pady=5)
        self.loot_status_text.config(state=tk.DISABLED)

    def _create_equipment_frame(self, parent):
        equip_frame = ttk.LabelFrame(parent, text="Ausrüstung", padding="10")
        equip_frame.grid(row=0, column=0, sticky="new")
        for i, (slot, var) in enumerate(self.equipment_vars.items()):
            ttk.Label(equip_frame, text=f"{slot}:").grid(row=i, column=0, sticky="w")
            ttk.Label(equip_frame, textvariable=var).grid(row=i, column=1, sticky="w", padx=5)

    def _create_inventory_frame(self, parent):
        self.inv_frame = ttk.LabelFrame(parent, text="Inventar", padding="10")
        self.inv_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.inv_frame.rowconfigure(0, weight=1)
        self.inv_frame.columnconfigure(0, weight=1)
        self.inventory_listbox = tk.Listbox(self.inv_frame)
        self.inventory_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(self.inv_frame, orient=tk.VERTICAL, command=self.inventory_listbox.yview)
        self.inventory_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.inventory_listbox.bind('<<ListboxSelect>>', self.update_button_states)

    def update_display(self):
        """Updates all GUI elements with the current player data."""
        self.char_name_var.set(f"{self.player.name} ({self.player.klasse})")
        self.char_level_var.set(self.player.level)
        self.char_gold_var.set(self.player.gold)
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
            self.inventory_listbox.insert(tk.END, str(item))
            if self.player.is_upgrade(item):
                self.inventory_listbox.itemconfig(i, {'bg': '#90EE90'})
            else:
                self.inventory_listbox.itemconfig(i, {'bg': 'white'})
        self.lp_label_var.set(f"{self.player.current_lp} / {self.player.max_lp} LP")
        self.lp_bar['value'] = (self.player.current_lp / self.player.max_lp) * 100 if self.player.max_lp > 0 else 0
        self.mp_label_var.set(f"{self.player.current_mp} / {self.player.max_mp} MP")
        self.mp_bar['value'] = (self.player.current_mp / self.player.max_mp) * 100 if self.player.max_mp > 0 else 0
        self.xp_label_var.set(f"{self.player.xp} / {self.player.xp_to_next_level} XP")
        self.xp_bar['value'] = (self.player.xp / self.player.xp_to_next_level) * 100 if self.player.xp_to_next_level > 0 else 0
        self.update_button_states()
        self.update_idletasks()

    def set_text(self, text_widget, text):
        """Helper function to set text in a disabled Text widget."""
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", text)
        text_widget.config(state=tk.DISABLED)

    def toggle_auto_quest(self):
        self.is_auto_questing = not self.is_auto_questing
        if self.is_auto_questing:
            self.auto_quest_button.config(text="Auto-Quest stoppen")
            self.set_text(self.loot_status_text, "Auto-Quest Modus aktiv...")
            self.start_quest()
        else:
            self.auto_quest_button.config(text="Auto-Quest starten")
            self.set_text(self.loot_status_text, "Auto-Quest Modus gestoppt.")

    def start_quest(self):
        if self.current_quest:
            if not self.is_auto_questing:
                messagebox.showwarning("Quest aktiv", "Bitte schließe erst die aktuelle Quest ab.")
            return
        if len(self.player.inventory) >= self.player.max_inventory_size:
            self.set_text(self.loot_status_text, "Inventar voll! Auto-Quest gestoppt.")
            messagebox.showinfo("Inventar voll", "Dein Inventar ist voll. Besuche den Händler!")
            if self.is_auto_questing:
                self.toggle_auto_quest()
            return
        quest_desc = random.choice(AVAILABLE_QUESTS)
        self.current_quest = Quest(quest_desc)
        self.set_text(self.quest_desc_text, quest_desc)
        self.progress_bar['value'] = 0
        self.update_display()
        self.advance_quest()

    def advance_quest(self):
        if self.current_quest is None: return
        self.current_quest.advance(self.player)
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
            loot_message = f"Loot: {gold} Gold, {xp} XP"
            if item:
                loot_message += f" und '{item.name}'" if item_added else f" (aber '{item.name}' passte nicht ins Inventar!)"
            self.set_text(self.loot_status_text, loot_message)
            if level_up_info:
                level_up_summary = f"Level Up! Du bist jetzt Level {self.player.level}!\n\nAttribut-Boni:\n" + "\n".join(level_up_info)
                messagebox.showinfo("Level Aufstieg!", level_up_summary)
            self.current_quest = None
            self.set_text(self.quest_desc_text, "Keine aktive Quest.")
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