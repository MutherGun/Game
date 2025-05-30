class Player:
    def __init__(self, name="Hráč"):
        self.name = name
        self.inventory = []
        self.gamma = 1

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{item.name} byl přidán do inventáře.")

    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            print(f"{item.name} byl odstraněn z inventáře.")
        else:
            print(f"{item.name} není v inventáři.")

    def use_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                item.use(self)
                return
        print(f"Předmět '{item_name}' nebyl nalezen v inventáři.")

player = Player()
