# main.py
"""
The main entry point for the text-based RPG.
This script now launches the graphical user interface.
"""

def main():
    """
    Launches the GUI version of the RPG in a loop to allow restarting.
    """
    while True:
        game_instance = None
        try:
            from rpg_gui import RpgGui, start_game_with_character_creation
            print("GUI-Modul erfolgreich geladen. Starte Charaktererstellung...")

            player_name, player_class = start_game_with_character_creation()

            if player_name is None or player_class is None:
                print("Charaktererstellung abgebrochen. Spiel wird beendet.")
                break # Exit the loop if user cancels creation

            import tkinter as tk
            root_window = tk.Tk()
            game_instance = RpgGui(root_window, player_name, player_class)
            root_window.mainloop()

            if not game_instance.game_over:
                # If window was closed manually, not via game over
                break

        except ImportError as e:
            print("--- FEHLER BEIM STARTEN DER GUI ---")
            print(f"Details: {e}")
            print("\nEs scheint, als ob die GUI-Komponente nicht gefunden werden konnte.")
            print("Stelle sicher, dass die Datei 'rpg_gui.py' im selben Verzeichnis liegt.")
            break # Exit loop on import error
        except Exception as e:
            # This will catch other errors, like the TclError if tkinter is not set up correctly
            print("--- EIN UNERWARTETER FEHLER IST AUFGETRETEN ---")
            print(f"Fehlertyp: {type(e).__name__}")
            print(f"Details: {e}")
            print("\nMögliche Ursachen:")
            print("1. Deine Python-Installation enthält möglicherweise kein 'tkinter'-Modul.")
            print("   (Bei Linux kann dies oft mit 'sudo apt-get install python3-tk' nachinstalliert werden).")
            print("2. Du führst das Skript in einer Umgebung ohne grafische Oberfläche aus (z.B. über SSH ohne X-Forwarding).")
            break # Exit loop on other critical errors

if __name__ == "__main__":
    main()