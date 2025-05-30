from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView


def get_item_from_inventory(inventory, item_name):
    for item in inventory:
        if item.name.lower() == item_name.lower():
            return item
    print(f"Položka '{item_name}' nebyla nalezena v inventáři.")
    return None


def remove_item_from_inventory(inventory, item_name):
    item = get_item_from_inventory(inventory, item_name)
    if item:
        inventory.remove(item)
        print(f"Předmět '{item_name}' byl odstraněn z inventáře.")
        return True
    return False


def list_inventory(inventory):
    return [(item.name, item.description) for item in inventory]


def use_item_from_inventory(player, item_name):
    item = get_item_from_inventory(player.inventory, item_name)
    if item:
        item.use(player)
        return True
    return False


class InventoryPopup(Popup):
    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.title = "Inventář"
        self.size_hint = (0.8, 0.8)
        self.player = player

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        item_box = BoxLayout(orientation='vertical', size_hint_y=None)
        item_box.bind(minimum_height=item_box.setter('height'))

        if not player.inventory:
            item_box.add_widget(Label(text="Inventář je prázdný."))
        else:
            for item in player.inventory:
                row = BoxLayout(size_hint_y=None, height=40)
                row.add_widget(Label(text=f"{item.name}: {item.description}", size_hint_x=0.7))
                btn = Button(text="Použít", size_hint_x=0.3)
                btn.bind(on_release=lambda instance, i=item: self.use_item(i))
                row.add_widget(btn)
                item_box.add_widget(row)

        scroll.add_widget(item_box)
        layout.add_widget(scroll)

        zavrit_btn = Button(text="Zavřít", size_hint_y=None, height=40)
        zavrit_btn.bind(on_release=self.dismiss)
        layout.add_widget(zavrit_btn)

        self.content = layout

    def use_item(self, item):
        item.use(self.player)
        self.dismiss()
