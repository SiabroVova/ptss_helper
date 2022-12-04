from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


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

    def update(self, dt):
        self.ball.move()

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
            sound = SoundLoader.load('boop.wav')
            sound.play()

        # bounce ball off left or right
        if (self.ball.x < self.x) or (self.ball.right > self.right):
            self.ball.velocity_x *= -1
            sound = SoundLoader.load('boop.wav')
            sound.play()


class EmdrApp(App):
    def build(self):
        game = EmdrPlace()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    EmdrApp().run()