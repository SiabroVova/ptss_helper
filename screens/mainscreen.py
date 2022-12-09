from kivy.app import App
from kivy.lang import Builder
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar
from kivy.uix.popup import Popup


Builder.load_file('screens/mainscreen.kv')

menu_dict = {
    "menu_1": {
        "name": "Що таке EMDR?",
        "content": "EMDR (Eye Movement Desensibilization and Reprocessing) – перекладається, як десенсибілізація та репроцесуалізація (опрацювання травми) рухом очей. Метод EMDR був створений в 1987 році др. Френсін Шапіро (психолог, старший науковий співробітник Науково-дослідного інституту Психічних досліджень в Пало-Альто, США). Це інноваційне клінічне лікування, з емпірично встановленою ефективністю, яке успішно допомогло більше як одному мільйону людей в різних куточках земної кулі, що зазнали психологічних труднощів внаслідок пережитого травматичного досвіду – від жертв ДТП, домашнього насильства до потерпілих від тероризму, стихійного лиха і т.п.."
        },
    "menu_2": {
        "name": "Як це працює",
        "content": "Терапія EMDR використовує біполярні (по горизонтально осі) стимулюючі руху очей, або ж (поплескування або дотик) послідовну подачу звуків. В результаті подібної стимуляції, психіка травмованої особи звільняє себе від заблокованості спогадів викликаних психотравмою."
    },
    "menu_3": {
        "name": "Контакти",
        "content": "Чат пітоністів)))"
    }
}

class MD3Card(MDCard, CommonElevationBehavior):
    """Implements a material design v3 card."""


class MainScreen(MDScreen):
    """ Main screen for aplication """

    test_dialog = None

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{item[1]['name']}",
                "height": dp(56),
                "on_release": lambda x=f"{item[1]['content']}": self.menu_callback(x),
            } for item in menu_dict.items()
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
        )

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, text_item):
        self.menu.dismiss()
        self.show_test_dialog(text_item)

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

    def show_test_dialog(self, content):
        """ Tests dialog window """
        if not self.test_dialog:
            self.test_dialog = MDDialog(
                title="Popup Window",
                text=f"[color=ace3cd] {content} [/color]",
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
