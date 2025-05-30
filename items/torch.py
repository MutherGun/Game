from items.item import Item

class Torch(Item):
    def __init__(self):
        super().__init__("Pochodeň", "svítí")
    def use(self, player):
        if hasattr(player, "gamma"):
            player.gamma += 1
            print("Aaah konečně trochu světla:", player.gamma)
        else:
            return None