"""
    зібрати додаток - buildozer -v android debug
    зібрати та запустити - buildozer -v android debug deploy run

"""
import os
os.environ["KIVY_AUDIO"] = "ffpyplayer"

from kivy.app import App
from kivymd.app import MDApp
from kivy import Config
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen

if platform not in ('android', 'ios'):
    Config.set('graphics', 'resizable', '0')
    Window.size = (400, 800)

# На помилку не звертати увагу. Все буде працювати))
elif platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE,
                         Permission.INTERNET])


class EmdrBall(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class EmdrPlace(Widget):

    ball = ObjectProperty(None)

    def serve_ball(self, vel=(3, 3)):
        self.ball.center = self.center
        self.ball.velocity = vel

    @staticmethod
    def play_sound():
        # if platform == 'android':
        sound = SoundLoader.load('sound/boop.wav')
        if sound:
            sound.play()

    def update(self, dt):
        self.ball.move()

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
            self.play_sound()

        # bounce ball off left or right
        if (self.ball.x < self.x) or (self.ball.right > self.right):
            self.ball.velocity_x *= -1
            self.play_sound()

    def on_touch_down(self, touch):
        app = App.get_running_app()
        app.stop_game()


class MainScreen(MDScreen):
    pass


class EmdrApp(MDApp):

    s_button = ObjectProperty()
    game = ObjectProperty()

    def __init__(self, **kwargs):
        super(EmdrApp, self).__init__(**kwargs)
        self.main_screen = MainScreen()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        return self.main_screen

    def center_button(self):
        self.s_button = MDRectangleFlatButton(text="Натисніть для старту",
                                              on_release=self.add_game_widget)
        self.s_button.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        return self.s_button

    def add_game_widget(self, dt=0):
        self.main_screen.clear_widgets()
        self.game = EmdrPlace()
        self.game.serve_ball()
        self.main_screen.add_widget(self.game)
        self.game_shudle = Clock.schedule_interval(self.game.update, 1.0 / 60.0)

    def stop_game(self):
        self.game_shudle.cancel()
        self.main_screen.remove_widget(self.game)
        self.main_screen.add_widget(self.center_button())

    def on_start(self):
        self.main_screen.add_widget(self.center_button())


if __name__ == '__main__':
    EmdrApp().run()
