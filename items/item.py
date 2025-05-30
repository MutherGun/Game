class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def use(self, player):
        print(f"{self.name} nemá žádný speciální efekt.")