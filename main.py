"""
    зібрати додаток - buildozer -v android debug
    зібрати та запустити - buildozer -v android debug deploy run

"""
import os
os.environ['KIVY_TEXT'] = 'sdl2'
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
os.environ['KIVY_WINDOW'] = 'sdl2'
os.environ["KIVY_AUDIO"] = "ffpyplayer"

from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy import Config
from kivy.utils import platform
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from screens.mainscreen import MainScreen
from screens.gamescreen import GameScreen


if platform not in ('android', 'ios'):
    Config.set('graphics', 'resizable', '0')
    Window.size = (400, 800)

# На помилку не звертати увагу. Все буде працювати))
elif platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE,
                         Permission.INTERNET])


class ScreenManage(ScreenManager):
    main_screen = MainScreen
    game_screen = GameScreen


class EmdrApp(MDApp):
    """ Тільки точка входу """

    manager = ObjectProperty()

    def __init__(self, **kwargs):
        super(EmdrApp, self).__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.material_style = "M3"
        self.manager = ScreenManage()
        self. manager.transition.duration = 0
        self.manager.current = 'main_screen'
        return self.manager

    def on_start(self):
        pass


if __name__ == '__main__':
    EmdrApp().run()
