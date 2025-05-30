class Crossroad:
    def get_description(self):
        return {
            "image": "assets/images/crossroad.jpg",
            "interactables": [
                {
                    "id": "path_left",
                    "x_percent": 0.14,
                    "y_percent": 0.24,
                    "w_percent": 0.15,
                    "h_percent": 0.60,
                    "label": ""
                },
                {
                    "id": "path_middle",
                    "x_percent": 0.40,
                    "y_percent": 0.24,
                    "w_percent": 0.15,
                    "h_percent": 0.60,
                    "label": ""
                },
                {
                    "id": "path_right",
                    "x_percent": 0.75,
                    "y_percent": 0.24,
                    "w_percent": 0.15,
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
                    "image": "assets/icons/arrow_back.png"
                }
            ],
            "text": (
                "Jsi na rozcestí . Kam teď?. "
            )
        }

    def handle_click(self, area_id):
        if area_id == "path":
            return Crossroad()
        elif area_id == "back":
            return "back"
        elif area_id == "___nothing___":
            return None
        else:
            print("Tímto směrem nemůžeš jít.")
            return None