from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.app import App

from utils.global_music import GlobalMusicPlayer
from utils.inventory import get_item_from_inventory
from utils.player import player
from utils.inventory import InventoryPopup


class MenuOverlay(BoxLayout):
    def __init__(self, save_callback, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (120, 60)
        self.pos_hint = {'left': 1.0, 'top': 1.0}
        self.padding = 5

        self.save_callback = save_callback

        self.menu_button = Button(
            text="☰ Menu",
            font_size=16,
            size_hint=(0.8, 0.8)
        )
        self.menu_button.bind(on_release=self.show_dropdown)
        self.add_widget(self.menu_button)

        self.dropdown = DropDown()

        inventory_btn = Button(text="🎒 Inventář", size_hint_y=None, height=44)
        inventory_btn.bind(on_release=self.open_inventory)
        self.dropdown.add_widget(inventory_btn)

        save_btn = Button(text="💾 Ulož hru", size_hint_y=None, height=44)
        save_btn.bind(on_release=self.save_and_close)
        self.dropdown.add_widget(save_btn)

        exit_btn = Button(text="❌ Ukončit", size_hint_y=None, height=44)
        exit_btn.bind(on_release=self.exit_game)
        self.dropdown.add_widget(exit_btn)

    def show_dropdown(self, instance):
        self.dropdown.open(instance)

    def save_and_close(self, instance):
        self.dropdown.dismiss()
        self.save_callback()

    def exit_game(self, instance):
        self.dropdown.dismiss()
        GlobalMusicPlayer().stop_music()
        App.get_running_app().stop()

    def open_inventory(self, instance):
        self.dropdown.dismiss()
        popup = InventoryPopup(player)
        popup.open()
