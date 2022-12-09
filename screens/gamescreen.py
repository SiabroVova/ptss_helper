from kivy import platform
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty, ListProperty
from kivy.resources import resource_find
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivymd.uix.screen import MDScreen

Builder.load_file('screens/gamescreen.kv')


class EmdrBall(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class EmdrPlace(Widget):

    ball = ObjectProperty()
    volume = NumericProperty()
    size_ball = ListProperty()
    speed_ball = ListProperty()

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = self.speed_ball
        self.ball.size = self.size_ball

    def play_sound(self):
        # if platform == 'android':
        sound_file = resource_find('sound/boop.wav')
        sound = SoundLoader.load(sound_file)
        if sound:
            sound.volume = self.volume
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


class GameScreen(MDScreen):

    game = ObjectProperty()
    game_schedule = ObjectProperty()
    speed = ListProperty([3, 3])
    size_ball = ListProperty([20, 20])
    volume = NumericProperty(1)

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

    @staticmethod
    def main_screen():
        """ Return to main screen """
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def start_game(self):
        """ Add widget and start game"""
        self.game = EmdrPlace()
        self.game.size_ball = self.size_ball
        self.game.speed_ball = self.speed
        self.game.volume = self.volume
        self.game.serve_ball()
        self.add_widget(self.game)
        self.game_schedule = Clock.schedule_interval(self.game.update, 1.0 / 60.0)

    def on_touch_down(self, touch):
        """ If touch to screen """
        self.stop_game()

    def stop_game(self):
        """ Cancel schedule event. Remove game widget. Switch to main screen"""
        self.game_schedule.cancel()
        self.remove_widget(self.game)
        self.main_screen()
