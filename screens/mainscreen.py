from kivy.app import App
from kivy.lang import Builder
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from const import SIZE_BALL, SPEED_BALL, \
    BACKGROUND_BUTTON_COLOR_PASSIVE, BACKGROUND_BUTTON_COLOR_ACTIVE


Builder.load_file('screens/mainscreen.kv')

menu_dict = {
    "menu_1": {
        "name": "Що таке EMDR?",
        "content": "EMDR (Eye Movement Desensibilization and Reprocessing) – перекладається, як десенсибілізація та "
                   "репроцесуалізація (опрацювання травми) рухом очей. Метод EMDR був створений в 1987 році др. "
                   "Френсін Шапіро (психолог, старший науковий співробітник Науково-дослідного інституту Психічних "
                   "досліджень в Пало-Альто, США). Це інноваційне клінічне лікування, з емпірично встановленою "
                   "ефективністю, яке успішно допомогло більше як одному мільйону людей в різних куточках земної кулі, "
                   "що зазнали психологічних труднощів внаслідок пережитого травматичного досвіду – від жертв ДТП, "
                   "домашнього насильства до потерпілих від тероризму, стихійного лиха і т.п.."
        },
    "menu_2": {
        "name": "Як це працює",
        "content": "Терапія EMDR використовує біполярні (по горизонтально осі) стимулюючі руху очей, або ж "
                   "(поплескування або дотик) послідовну подачу звуків. В результаті подібної стимуляції, "
                   "психіка травмованої особи звільняє себе від заблокованості спогадів викликаних психотравмою."
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
    game_screen = None

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.numeric_button_tup = ('button_numeric_1', 'button_numeric_2', 'button_numeric_3')
        self.volume_button_tup = ('button_volume_off', 'button_volume_high')
        self.blank_circle_tup = ('button_circle_size_12', 'button_circle_size_18', 'button_circle_size_26')

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

    def press_button_numeric(self, icon: str):
        """ On release one of button speed """
        self.game_screen = self.get_game_screen()
        if icon == 'numeric-1':
            self.change_button_color('button_numeric_1', 'numeric')
            self.game_screen.speed = SPEED_BALL[0]

        elif icon == 'numeric-2':
            self.change_button_color('button_numeric_2', 'numeric')
            self.game_screen.speed = SPEED_BALL[1]

        elif icon == 'numeric-3':
            self.change_button_color('button_numeric_3', 'numeric')
            self.game_screen.speed = SPEED_BALL[2]

    def press_button_volume(self, icon: str):
        """ On release one of button volume """
        self.game_screen = self.get_game_screen()
        if icon == 'volume-off':
            self.change_button_color('button_volume_off', 'volume')
            self.game_screen.volume = 0
        else:
            self.change_button_color('button_volume_high', 'volume')
            self.game_screen.volume = 1

    def press_button_blank_circle(self, icon_size: int):
        """ On release one of button size """
        self.game_screen = self.get_game_screen()
        if icon_size == 12:
            self.change_button_color('button_circle_size_12')
            self.game_screen.size_ball = SIZE_BALL[0]
        elif icon_size == 18:
            self.change_button_color('button_circle_size_18')
            self.game_screen.size_ball = SIZE_BALL[1]
        else:
            self.change_button_color('button_circle_size_26')
            self.game_screen.size_ball = SIZE_BALL[2]

    def change_button_color(self, button_id: str, button=None):
        """ Change background color for buttons speed, volume, size """
        if button == 'numeric':
            list_for_remove = list(self.numeric_button_tup)
        elif button == 'volume':
            list_for_remove = list(self.volume_button_tup)
        else:
            list_for_remove = list(self.blank_circle_tup)

        list_for_remove.remove(button_id)
        if self.ids[f'{button_id}'].md_bg_color != BACKGROUND_BUTTON_COLOR_ACTIVE:
            self.ids[f'{button_id}'].md_bg_color = BACKGROUND_BUTTON_COLOR_ACTIVE
            for button in list_for_remove:
                self.ids[f'{button}'].md_bg_color = BACKGROUND_BUTTON_COLOR_PASSIVE

    def press_color_button(self, color: str):
        """ On release one of button color """
        self.game_screen = self.get_game_screen()
        if color == 'yellow':
            if self.ids.button_color_yellow.md_bg_color == [1, 1, 0, 0.05]:
                self.game_screen.color_ball = [1, 1, 0, 0.65]
                self.ids.button_color_yellow.md_bg_color = [1, 1, 0, 0.65]
                self.ids.button_color_yellow.icon_color = [1, 1, 0, 1]

                self.ids.button_color_red.md_bg_color = [1, 0, 0, 0.05]
                self.ids.button_color_red.icon_color = [1, 0, 0, 0.2]

                self.ids.button_color_blue.md_bg_color = [0.21, 0.098, 1, 0.05]
                self.ids.button_color_blue.icon_color = [0.21, 0.098, 1, 0.2]

        elif color == 'red':
            if self.ids.button_color_red.md_bg_color == [1, 0, 0, 0.05]:
                self.game_screen.color_ball = [1, 0, 0, 0.65]
                self.ids.button_color_red.md_bg_color = [1, 0, 0, 0.65]
                self.ids.button_color_red.icon_color = [1, 0, 0, 1]

                self.ids.button_color_yellow.md_bg_color = [1, 1, 0, 0.05]
                self.ids.button_color_yellow.icon_color = [1, 1, 0, 0.2]

                self.ids.button_color_blue.md_bg_color = [0.21, 0.098, 1, 0.05]
                self.ids.button_color_blue.icon_color = [0.21, 0.098, 1, 0.2]

        elif color == 'blue':
            if self.ids.button_color_blue.md_bg_color == [0.21, 0.098, 1, 0.05]:
                self.game_screen.color_ball = [0.21, 0.098, 1, 0.65]
                self.ids.button_color_blue.md_bg_color = [0.21, 0.098, 1, 0.65]
                self.ids.button_color_blue.icon_color = [0.21, 0.098, 1, 1]

                self.ids.button_color_yellow.md_bg_color = [1, 1, 0, 0.05]
                self.ids.button_color_yellow.icon_color = [1, 1, 0, 0.2]

                self.ids.button_color_red.md_bg_color = [1, 0, 0, 0.05]
                self.ids.button_color_red.icon_color = [1, 0, 0, 0.2]
