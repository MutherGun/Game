from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from rooms.hallway import Hallway
from utils.menu_overlay import MenuOverlay


class StartRoom:
    def get_description(self):
        return {
            "image": "assets/images/start_room.jpg",
            "interactables": [
                {
                    "id": "door",
                    "x_percent": 0.68,
                    "y_percent": 0.24,
                    "w_percent": 0.20,
                    "h_percent": 0.60,
                    "label": ""
                },
                {
                    "id": "bed",
                    "x_percent": 0.20,
                    "y_percent": 0.20,
                    "w_percent": 0.30,
                    "h_percent": 0.30,
                    "label": ""
                },
                {
                    "id": "rat",
                    "x_percent": 0.68,
                    "y_percent": 0.09,
                    "w_percent": 0.10,
                    "h_percent": 0.10,
                    "label": ""
                }
            ],
            "text": (
                "Nacházíš se v temné cele. "
                "Jediné světlo sem proniká malým okénkem s mříží. "
            )
        }

    def handle_click(self, area_id):
        if area_id == "door":
            return Hallway()
        elif area_id == "bed":
            return "Stará postel"
        elif area_id == "rat":
            return "Pěkně vyžraná krysa"
        elif area_id == "___nothing___":
            return None
        else:
            return None


class GameScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        overlay = MenuOverlay(save_callback=self.save_game)
        self.add_widget(overlay)

    def save_game(self):
        popup = Popup(title="Uloženo", content=Label(text='Hra byla uložena!'),
                      size_hint=(None, None), size=(300, 200))
        popup.open()
