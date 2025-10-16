# main.py
"""
The main game loop and user interface for the text-based RPG.
"""
from character import Character
from quest import Quest
import time

# Liste verfügbarer Quests
AVAILABLE_QUESTS = [
    "Rette eine Prinzessin aus einem anderen Schloss",
    "Sammle 10 leere Flaschen für den Alchemisten",
    "Polere die Rüstung des Königs (ohne Bezahlung)",
    "Entwirre die Kopfhörer des Barden",
    "Finde das Rezept für ewige Jugend (und verliere es wieder)"
]

def main():
    """The main function to run the game."""
    print("--- Willkommen bei Progress Quest 2.0 ---")

    # Charaktererstellung
    player_name = input("Gib den Namen deines Helden ein: ")
    player_class = input("Wähle eine Klasse (z.B. 'Mächtiger Barbar', 'Verwirrter Zauberer'): ")
    player = Character(player_name, player_class)

    print(f"\nDein Abenteuer als {player.name}, der {player.klasse}, beginnt!")

    # Spielschleife
    while True:
        player.display_status()

        print("\nWas möchtest du tun?")
        print("1: Neue Quest beginnen")
        print("2: Gegenstand ausrüsten")
        print("3: Spiel beenden")

        choice = input("> ")

        if choice == '1':
            # Quest starten
            import random
            quest_description = random.choice(AVAILABLE_QUESTS)
            current_quest = Quest(quest_description)

            print(f"\nNeue Quest gestartet: {quest_description}")

            # Quest automatisch abschließen
            while not current_quest.is_complete():
                gold, item = current_quest.advance()
                if gold is not None:
                    player.add_loot(gold, item)
                    # Simuliert ein Level-Up nach jeder Quest
                    player.level += 1
                    print(f"Glückwunsch! Du hast Level {player.level} erreicht!")

        elif choice == '2':
            # Gegenstand ausrüsten
            if not player.inventory:
                print("\nDein Inventar ist leer.")
                continue

            try:
                item_index = int(input("Gib die Inventarnummer des Gegenstands an, den du ausrüsten möchtest: "))
                player.equip(item_index)
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Zahl ein.")

        elif choice == '3':
            # Spiel beenden
            print("Auf Wiedersehen, Abenteurer!")
            break
        else:
            print("Ungültige Auswahl. Bitte versuche es erneut.")

        # Kurze Pause, damit der Spieler die Ausgabe lesen kann
        time.sleep(1.5)

if __name__ == "__main__":
    main()