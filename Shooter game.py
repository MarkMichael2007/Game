import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
import random

kivy.require('1.11.1')

class Bullet(Image):
    def __init__(self, **kwargs):
        super(Bullet, self).__init__(**kwargs)
        self.source = 'bullet.png'
        self.size = (20, 20)
        self.velocity = (0, 5)

    def move(self):
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])

class Enemy(Image):
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)
        self.source = 'enemy.jfif'
        self.size = (50, 50)
        self.velocity = (0, -2)

    def move(self):
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])

class Shooter(Image):
    def __init__(self, **kwargs):
        super(Shooter, self).__init__(**kwargs)
        self.source = 'OIP.jfif'
        self.size = (50, 50)
        self.center_x = Window.width / 2
        self.center_y = 50

    def move(self, direction):
        if direction == 'left':
            self.center_x -= 10
        elif direction == 'right':
            self.center_x += 10

class ShootingGame(Widget):
    def __init__(self, **kwargs):
        super(ShootingGame, self).__init__(**kwargs)
        self.shooter = Shooter()
        self.bullets = []
        self.enemies = []
        self.add_widget(self.shooter)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'a':
            self.shooter.move('left')
        elif keycode[1] == 'd':
            self.shooter.move('right')

    def on_key_up(self, keyboard, keycode):
        if keycode[1] in ['a', 'd']:
            self.shooter.move('stop')

    def on_touch_down(self, touch):
        bullet = Bullet(pos=(self.shooter.center_x - 10, self.shooter.center_y + 25))
        self.bullets.append(bullet)
        self.add_widget(bullet)

    def update(self, dt):
        for bullet in self.bullets:
            bullet.move()
            if bullet.y > Window.height:
                self.remove_widget(bullet)
                self.bullets.remove(bullet)

        if random.random() < 0.02:
            enemy = Enemy(pos=(random.randint(0, Window.width - 50), Window.height))
            self.enemies.append(enemy)
            self.add_widget(enemy)

        for enemy in self.enemies:
            enemy.move()
            if enemy.y < 0:
                self.remove_widget(enemy)
                self.enemies.remove(enemy)

            for bullet in self.bullets:
                if bullet.collide_widget(enemy):
                    self.remove_widget(bullet)
                    self.bullets.remove(bullet)
                    self.remove_widget(enemy)
                    self.enemies.remove(enemy)

class ShootingApp(App):
    def build(self):
        game = ShootingGame()
        keyboard = Window.request_keyboard(self.keyboard_closed, game)
        keyboard.bind(on_key_down=game.on_key_down)
        keyboard.bind(on_key_up=game.on_key_up)
        return game

    def keyboard_closed(self):
        pass

if __name__ == '__main__':
    ShootingApp().run()
