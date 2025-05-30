from kivy.core.audio import SoundLoader

class GameEngine:
    def __init__(self, start_room):

        self.current_room = start_room
        self.room_history = []
        self.is_running = True
        self.currect_sound = None
        self.play_room_music()

    def get_current_description(self):

        return self.current_room.get_description()

    def process_command(self, command):
        """
        Zpracovává textový příkaz od hráče (např. 'exit', 'porozhlednout').
        Pokud dojde ke změně místnosti, uloží předchozí do historie.
        """
        if command in ["exit", "quit"]:
            self.is_running = False
            return "Ukončuji hru. Díky za hraní!"

        result = self.current_room.handle_command(command)

        if isinstance(result, str):
            return result  # odpověď ze stejné místnosti (např. 'nic zde není')
        elif result:
            self.room_history.append(self.current_room)  # uloží aktuální místnost do historie
            self.current_room = result                   # přepne na novou místnost
            self.play_room_music()                       # přehraje hudbu nové místnosti
            return self.current_room.get_description()
        else:
            return "Neplatný příkaz. Zkus to znovu."

    def handle_click(self, area_id):
        result = self.current_room.handle_click(area_id)

        if result == "back":
            self.go_back()
        elif isinstance(result, str):
            return result
        elif result:
            self.room_history.append(self.current_room)
            self.current_room = result
            self.play_room_music()

        return self.current_room.get_description()

    def go_back(self):
        if self.room_history:
            self.current_room = self.room_history.pop()
            self.play_room_music()

    def play_room_music(self):
        if self.currect_sound:
            self.currect_sound.stop()

        description = self.current_room.get_description()
        music_path = description.get("music")

        if music_path:
            self.currect_sound = SoundLoader.load(music_path)
            if self.currect_sound:
                self.currect_sound.loop = True
                self.currect_sound.play()
