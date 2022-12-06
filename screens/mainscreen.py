from kivy.app import App
from kivy.lang import Builder
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

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    @staticmethod
    def game_screen():
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
        self.game_screen()
        game_screen = self.get_game_screen()
        game_screen.start_game()

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
