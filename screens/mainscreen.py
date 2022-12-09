from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

Builder.load_file('screens/mainscreen.kv')


class MD3Card(MDCard, CommonElevationBehavior):
    """Implements a material design v3 card."""


class MainScreen(MDScreen):
    """ Main screen for aplication """

    test_dialog = None
    game_screen = None

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.numeric_button_tup = ('button_numeric_1', 'button_numeric_2', 'button_numeric_3')
        self.volume_button_tup = ('button_volume_off', 'button_volume_high')
        self.blank_circle_tup = ('button_circle_size_12', 'button_circle_size_18', 'button_circle_size_26')

    @staticmethod
    def switch_game_screen():
        """ Switch to game screen """
        app = App.get_running_app()
        app.root.current = 'game_screen'

    @staticmethod
    def get_game_screen():
        """ Get game screen """
        app = App.get_running_app()
        get_screen = app.root.get_screen('game_screen')
        return get_screen

    def press_start_game(self):
        """ On presss start switch to game screen and start game"""
        self.switch_game_screen()
        self.game_screen = self.get_game_screen()
        self.game_screen.start_game()

    def show_test_dialog(self):
        """ Tests dialog window """
        if not self.test_dialog:
            self.test_dialog = MDDialog(
                title="Popup Window",
                text=f"[color=ace3cd]Тестовий ПОПАП :)[/color]",
                # content_cls=ClassForData(), якщо потрібно взяти розмітку з файлу KV у твому випадку то P()
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.close_test_dialog
                    ),
                ],
            )
            self.test_dialog.open()

    def close_test_dialog(self, dt=0):
        """ Close dialog window"""
        self.test_dialog.dismiss()
        del self.test_dialog

    def press_button_numeric(self, icon):
        self.game_screen = self.get_game_screen()
        if icon == 'numeric-1':
            self.change_button_color('button_numeric_1', 'numeric')
            self.game_screen.speed = 3, 3

        elif icon == 'numeric-2':
            self.change_button_color('button_numeric_2', 'numeric')
            self.game_screen.speed = 6, 6

        elif icon == 'numeric-3':
            self.change_button_color('button_numeric_3', 'numeric')
            self.game_screen.speed = 10, 10

    def press_button_volume(self, icon):
        self.game_screen = self.get_game_screen()
        if icon == 'volume-off':
            self.change_button_color('button_volume_off', 'volume')
        else:
            self.change_button_color('button_volume_high', 'volume')

    def press_button_blank_circle(self, icon_size):
        self.game_screen = self.get_game_screen()
        if icon_size == 12:
            self.change_button_color('button_circle_size_12')
        elif icon_size == 18:
            self.change_button_color('button_circle_size_18')
        else:
            self.change_button_color('button_circle_size_26')

    def change_button_color(self, button_id, button=None):
        if button == 'numeric':
            list_for_remove = list(self.numeric_button_tup)
        elif button == 'volume':
            list_for_remove = list(self.volume_button_tup)
        else:
            list_for_remove = list(self.blank_circle_tup)

        list_for_remove.remove(button_id)
        if self.ids[f'{button_id}'].md_bg_color != [1, 1, 1, .8]:
            self.ids[f'{button_id}'].md_bg_color = [1, 1, 1, .8]
            for button in list_for_remove:
                self.ids[f'{button}'].md_bg_color = [1, 1, 1, .3]
