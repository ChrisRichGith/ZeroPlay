# trader_gui.py
"""
Defines the GUI for the Trader window.
"""
import tkinter as tk
from tkinter import ttk, messagebox

class TraderWindow:
    """Manages the trader GUI window."""

    def __init__(self, parent, player, trader, on_close_callback):
        """
        Initializes the trader window.

        Args:
            parent: The parent window (main GUI).
            player (Character): The player character instance.
            trader (Trader): The trader instance.
            on_close_callback: A function to call when the window is closed.
        """
        self.parent = parent
        self.player = player
        self.trader = trader
        self.on_close_callback = on_close_callback

        # Create a Toplevel window that exists on top of the main window
        self.window = tk.Toplevel(parent)
        self.window.title("Händler")
        self.window.geometry("500x400")
        self.window.minsize(400, 300)

        # Ensure closing the window calls our custom function
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        # Grab focus
        self.window.transient(parent)
        self.window.grab_set()

        self._setup_vars()
        self.create_widgets()
        self.update_display()

    def _setup_vars(self):
        """Sets up tkinter StringVars for the trader window."""
        self.player_gold_var = tk.StringVar()
        self.upgrade_cost_var = tk.StringVar()

    def create_widgets(self):
        """Creates the widgets for the trader window."""
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Top frame for player gold and upgrade button
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(top_frame, text="Dein Gold:").pack(side=tk.LEFT)
        ttk.Label(top_frame, textvariable=self.player_gold_var).pack(side=tk.LEFT, padx=5)

        self.upgrade_button = ttk.Button(top_frame, text="Inventar erweitern", command=self.buy_upgrade)
        self.upgrade_button.pack(side=tk.RIGHT)
        ttk.Label(top_frame, textvariable=self.upgrade_cost_var).pack(side=tk.RIGHT, padx=5)

        # Inventory list
        inv_frame = ttk.LabelFrame(main_frame, text="Inventar zum Verkaufen", padding="10")
        inv_frame.grid(row=1, column=0, sticky="nsew")
        inv_frame.rowconfigure(0, weight=1)
        inv_frame.columnconfigure(0, weight=1)

        self.sell_listbox = tk.Listbox(inv_frame)
        self.sell_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(inv_frame, orient=tk.VERTICAL, command=self.sell_listbox.yview)
        self.sell_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bottom frame for sell button
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        self.sell_button = ttk.Button(bottom_frame, text="Ausgewählten Gegenstand verkaufen", command=self.sell_item)
        self.sell_button.pack()

    def update_display(self):
        """Updates all display elements in the trader window."""
        self.player_gold_var.set(self.player.gold)
        self.upgrade_cost_var.set(f"Kosten: {self.trader.get_upgrade_cost()} Gold")

        self.sell_listbox.delete(0, tk.END)
        for item in self.player.inventory:
            self.sell_listbox.insert(tk.END, str(item))

        # Disable button if player can't afford it
        can_afford = self.player.gold >= self.trader.get_upgrade_cost()
        self.upgrade_button.config(state=tk.NORMAL if can_afford else tk.DISABLED)

    def sell_item(self):
        """Sells the selected item."""
        selected_indices = self.sell_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Verkaufen", "Bitte wähle einen Gegenstand zum Verkaufen aus.", parent=self.window)
            return

        item_index = selected_indices[0]
        item_name = self.player.inventory[item_index].name
        item_value = self.player.inventory[item_index].value

        sold = self.trader.sell_item(self.player, item_index)
        if sold:
            messagebox.showinfo("Verkauft!", f"'{item_name}' für {item_value} Gold verkauft.", parent=self.window)
            self.update_display()

    def buy_upgrade(self):
        """Buys an inventory upgrade."""
        cost = self.trader.get_upgrade_cost()
        upgraded = self.trader.buy_inventory_upgrade(self.player)
        if upgraded:
            messagebox.showinfo("Upgrade erfolgreich!", f"Inventar für {cost} Gold erweitert!", parent=self.window)
            self.update_display()
        else:
            messagebox.showerror("Nicht genug Gold", "Du kannst dir dieses Upgrade nicht leisten.", parent=self.window)

    def close_window(self):
        """Handles the window closing event."""
        self.on_close_callback() # Notify the main GUI
        self.window.destroy()