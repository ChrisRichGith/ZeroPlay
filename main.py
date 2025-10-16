# main.py
"""
The main entry point for the text-based RPG.
This script now launches the graphical user interface.
"""

def main():
    """
    Launches the GUI version of the RPG and handles potential import errors.
    """
    try:
        # We import here to catch the error immediately
        from rpg_gui import start_game_with_character_creation
        print("GUI-Modul erfolgreich geladen. Starte grafische Oberfläche...")
        start_game_with_character_creation()
    except ImportError as e:
        print("--- FEHLER BEIM STARTEN DER GUI ---")
        print(f"Details: {e}")
        print("\nEs scheint, als ob die GUI-Komponente nicht gefunden werden konnte.")
        print("Stelle sicher, dass die Datei 'rpg_gui.py' im selben Verzeichnis liegt.")
    except Exception as e:
        # This will catch other errors, like the TclError if tkinter is not set up correctly
        print("--- EIN UNERWARTETER FEHLER IST AUFGETRETEN ---")
        print(f"Fehlertyp: {type(e).__name__}")
        print(f"Details: {e}")
        print("\nMögliche Ursachen:")
        print("1. Deine Python-Installation enthält möglicherweise kein 'tkinter'-Modul.")
        print("   (Bei Linux kann dies oft mit 'sudo apt-get install python3-tk' nachinstalliert werden).")
        print("2. Du führst das Skript in einer Umgebung ohne grafische Oberfläche aus (z.B. über SSH ohne X-Forwarding).")

if __name__ == "__main__":
    main()