from rooms.crossroad import Crossroad
from utils.player import player
from items.torch import Torch

class Hallway:
    def __init__(self):
        self.torch_taken = "pochoden" in player.inventory  # načte stav z inventáře

    def get_description(self):
        image = "assets/images/hallway_1.jpg" if self.torch_taken else "assets/images/hallway.jpg"

        interactables = [
            {
                "id": "path",
                "x_percent": 0.36,
                "y_percent": 0.24,
                "w_percent": 0.30,
                "h_percent": 0.60,
                "label": ""
            },
            {
                "id": "back",
                "x_percent": 0.08,
                "y_percent": 0.08,
                "w_percent": 0.10,
                "h_percent": 0.10,
                "label": "Zpět",
                "image": "assets/icons/arrow_back.png"  #
            }
        ]

        if not self.torch_taken:
            interactables.append({
                "id": "torch_left",
                "x_percent": 0.20,
                "y_percent": 0.50,
                "w_percent": 0.08,
                "h_percent": 0.30,
                "label": "Pochodeň"
            })

        return {
            "image": image,
            "interactables": interactables,
            "text": "Nacházíš se v dlouhé, studené chodbě."
        }

    def handle_click(self, area_id):
        if area_id == "path":
            return Crossroad()
        elif area_id == "back":
            return "back"
        elif area_id == "torch_left":
            if "pochoden" not in player.inventory:
                player.inventory.append(Torch())
                self.torch_taken = True
            return self
        else:
            return None
