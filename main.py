from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.popup import Popup
import json
import os
from functools import partial

from engine.game_engine import GameEngine
from rooms.crossroad import Crossroad
from rooms.start_room import StartRoom
from rooms.hallway import Hallway
from utils.global_music import GlobalMusicPlayer
from utils.menu_overlay import MenuOverlay
from utils.player import player

Builder.load_file("kv/menu.kv")
Builder.load_file("kv/start_room.kv")


class MenuScreen(Screen):
    def on_enter(self):
        if not hasattr(self, 'music'):
            self.music = SoundLoader.load("assets/sounds/background.mp3")
            if self.music:
                self.music.loop = True
                self.music.play()

    def start_new_game(self):
        if hasattr(self, 'music') and self.music:
            self.music.stop()
        self.manager.transition.direction = "left"
        self.manager.current = "game"
        self.manager.get_screen("game").start_game()

        GlobalMusicPlayer().play_music("assets/sounds/dungeon.mp3")

    def continue_game(self):
        if not os.path.exists("savegame.json"):
            return

        with open("savegame.json", "r") as f:
            save_data = json.load(f)

        room_name = save_data.get("room", "StartRoom")

        room_map = {
            "StartRoom": StartRoom,
            "Hallway": Hallway,
            "Crossroad": Crossroad,
        }

        room_class = room_map.get(room_name, StartRoom)
        self.manager.get_screen("game").start_game_from_room(room_class())

        if hasattr(self, 'music') and self.music:
            self.music.stop()

        self.manager.transition.direction = "left"
        self.manager.current = "game"

        GlobalMusicPlayer().play_music("assets/sounds/dungeon.mp3")


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = None
        self.image_widget = None
        self.room_history = []

    def start_game(self):
        self.room_history = []
        self.engine = GameEngine(StartRoom())
        Clock.schedule_once(lambda dt: self.show_current_room(), 0.1)

    def start_game_from_room(self, room_instance):
        self.room_history = []
        self.engine = GameEngine(room_instance)
        Clock.schedule_once(lambda dt: self.show_current_room(), 0.1)

    def show_current_room(self):
        description = self.engine.get_current_description()
        container = self.ids.container
        container.clear_widgets()

        self.image_widget = Image(
            source=description["image"],
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )
        container.add_widget(self.image_widget)

        bg_button = Button(
            background_normal='',
            background_color=(1, 1, 1, 0),
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            on_release=lambda instance: self.handle_interaction("__nothing__")
        )
        container.add_widget(bg_button)

        for item in description["interactables"]:
            button_kwargs = {
                "size_hint": (item["w_percent"], item["h_percent"]),
                "pos_hint": {"x": item["x_percent"], "y": item["y_percent"]},
                "on_release": partial(self.handle_interaction_with_area, item["id"])
            }

            if "image" in item:
                button_kwargs["background_normal"] = item["image"]
                button_kwargs["background_down"] = item["image"]
                button_kwargs["background_color"] = (1, 1, 1, 1)
            else:
                button_kwargs["background_normal"] = ''
                button_kwargs["background_color"] = (1, 1, 1, 0)

            button = Button(**button_kwargs)
            container.add_widget(button)

        menu_overlay = MenuOverlay(save_callback=self.save_game)
        container.add_widget(menu_overlay)

        self.ids.output_label.text = description["text"]
        self.engine.play_room_music()

    def handle_interaction_with_area(self, area_id, instance):
        self.handle_interaction(area_id)

    def handle_interaction(self, area_id):
        current_room = self.engine.current_room
        result = current_room.handle_click(area_id)

        if isinstance(result, str):
            if result == "back":
                if self.room_history:
                    self.engine.current_room = self.room_history.pop()
                    self.show_current_room()
                else:
                    self.ids.output_label.text = "Nemáš se kam vrátit."
            else:
                self.ids.output_label.text = result
        elif result:
            self.room_history.append(self.engine.current_room)
            self.engine.current_room = result
            self.show_current_room()
        else:
            self.ids.output_label.text = "Tady není nic zajímavého."

    def save_game(self):
        room_class_name = self.engine.current_room.__class__.__name__

        save_data = {
            "room": room_class_name
        }

        with open("savegame.json", "w") as f:
            json.dump(save_data, f)

        popup = Popup(
            title="Uloženo",
            content=Button(text='Hra byla uložena!'),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()


class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        return sm


if __name__ == "__main__":
    GameApp().run()
