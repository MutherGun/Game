from item import Item

class HealthPotion(Item):
    def __init__(self):
        super().__init__("Health Potion", "Obnoví 20 HP.")

    def use(self, player):

        healed = min(20, player.max_health - player.health)

        player.health += healed

        print(f"Použil jsi Lektvar zdraví a obnovil {healed} životů! "
              f"Nyní máš {player.health}/{player.max_health} HP.")
