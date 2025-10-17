# quest.py
"""
Defines the Quest class, which handles quest progression and rewards.
"""
import random
import time
from item import Item

# Vordefinierte Liste möglicher Items als Loot
# In einer größeren Anwendung würde dies aus einer Datenbank oder Konfigurationsdatei geladen
POSSIBLE_LOOT = [
    Item("Verfluchte Geige", "Waffe", {"Intelligenz": 5, "Glück": -2}, value=50),
    Item("Helm des Wahnsinns", "Kopf", {"Stärke": 3, "Intelligenz": -1}, value=35),
    Item("Rostige Brustplatte", "Brust", {"Stärke": 1}, value=10),
    Item("Glücksfeder", "Kopf", {"Glück": 2}, value=25),
    Item("Schwert der Mittelmäßigkeit", "Waffe", {"Stärke": 2}, value=20),
    Item("Seidenschal der Diplomatie", "Kopf", {"Intelligenz": 2}, value=22),
    Item("Solide Lederweste", "Brust", {"Stärke": 2}, value=18),
]

class Quest:
    """Represents a quest that automatically progresses and grants rewards."""

    def __init__(self, description, duration=10):
        """
        Initializes a new quest.

        Args:
            description (str): The description of the quest.
            duration (int): The number of 'ticks' required to complete the quest.
        """
        self.description = description
        self.duration = duration
        self.progress = 0

    def is_complete(self):
        """Checks if the quest is complete."""
        return self.progress >= self.duration

    def advance(self):
        """
        Advances the quest progress by one tick.

        Returns:
            A tuple (gold, item) if the quest is completed on this tick, otherwise (None, None).
        """
        if not self.is_complete():
            self.progress += 1
            self._display_progress_bar()
            time.sleep(0.2)  # Kurze Pause, um den Fortschritt zu simulieren

            if self.is_complete():
                print(f"\nQuest '{self.description}' abgeschlossen!")
                return self._generate_reward()

        return None, None

    def _display_progress_bar(self):
        """Displays a simple text-based progress bar in the console."""
        percentage = (self.progress / self.duration) * 100
        bar_length = 25
        filled_length = int(bar_length * self.progress // self.duration)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r{self.description}: [{bar}] {percentage:.0f}%", end="", flush=True)

    def _generate_reward(self):
        """
        Generates random gold, XP, and a random item as a reward.

        Returns:
            tuple: A tuple containing gold, xp, and an Item object (or None).
        """
        # Belohnungen skalieren leicht mit der Quest-Dauer
        gold_reward = random.randint(10, 50) + self.duration
        xp_reward = random.randint(20, 40) + self.duration * 2

        # 70% Chance auf ein Item als Belohnung
        if random.random() < 0.7:
            item_reward = random.choice(POSSIBLE_LOOT)
        else:
            item_reward = None

        return gold_reward, xp_reward, item_reward