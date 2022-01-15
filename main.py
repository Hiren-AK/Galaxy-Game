from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from tracemalloc import start
from turtle import speed
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.core.window import Window
from kivy.properties import Clock
from kivy import platform
import time

class MainWidget(Widget):
    perspectivePointX = NumericProperty(0)
    perspectivePointY = NumericProperty(0)
    V_num_lines = 14
    V_spacing_lines = 0.2       #10% of screen width
    vertical_lines = []
    H_num_lines = 10
    H_spacing_lines = 0.2       #10% of screen height
    horizontal_lines = []
    current_offset_y = 0
    speed = 1
    start_time = time.time()
    level = 20
    current_speed_x = 0
    speed_x = 10
    current_offset_x = 0

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()

        if self.touch_or_key():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down = self.on_keyboard_down)
            self._keyboard.bind(on_key_up = self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0/60)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self.on_keyboard_down)
        self._keyboard.unbind(on_key_up = self.on_keyboard_up)
        self._keyboard = None
    
    def touch_or_key(self):
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def on_parent(self, widget, parent):
        pass

    def on_size(self, *args):
        self.update_verticle_lines()
        self.update_horizontal_lines()

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_num_lines):
                self.vertical_lines.append(Line())

    def update_verticle_lines(self):
        x_center_line = self.width/2
        offset = -int(self.V_num_lines/2)+0.5
        spacing = self.V_spacing_lines * self.width

        for i in range(self.V_num_lines):
            x_line = int(x_center_line + offset * spacing + self.current_offset_x)
            x1, y1 = self.transform(x_line, 0)
            x2, y2 = self.transform(x_line, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_num_lines):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        x_center_line = self.width/2
        offset = -int(self.V_num_lines/2)+0.5
        spacing = self.V_spacing_lines * self.width
        x_min = x_center_line + (offset * spacing) + self.current_offset_x
        x_max = x_center_line - (offset * spacing) + self.current_offset_x

        spacing_y = self.H_spacing_lines * self.height
        for i in range(self.H_num_lines):
            y_line = i*spacing_y - self.current_offset_y
            x1, y1 = self.transform(x_min, y_line)
            x2, y2 = self.transform(x_max, y_line)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        #return self.transform2D(x, y)
        return self.transform_perspective(x, y)

    def transform2D(self, x, y):
        return x, y

    def transform_perspective(self, x, y):
        y_transformation = (y * self.perspectivePointY)/self.height
        if y_transformation > self.perspectivePointY:
            y_transformation = self.perspectivePointY

        diff_x = x - self.perspectivePointX
        diff_y = self.perspectivePointY - y_transformation
        y_proportion = (diff_y/self.perspectivePointY)**3

        x_transformation = self.perspectivePointX + (diff_x * y_proportion)
        y_transformation = (1 - y_proportion) * self.perspectivePointY

        return int(x_transformation), int(y_transformation)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.speed_x
        elif keycode[1] == 'right':
            self.current_speed_x = -self.speed_x

        return True
    
    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x = 0
        return True
    
    def on_touch_down(self, touch):
        if touch.x < self.width/2:
            self.current_speed_x = self.speed_x
        else:
            self.current_speed_x = -self.speed_x

    def on_touch_up(self, touch):
        self.current_speed_x = 0
    
    def update(self, dt):
        self.update_horizontal_lines()
        self.update_verticle_lines()
        time_factor = dt * 60
        self.current_offset_y += self.speed * time_factor

        if(int(time.time()-self.start_time) != 0 and int(time.time()-self.start_time)%self.level == 0 and self.speed < 5):
            self.level *= 2
            print(int(time.time()-self.start_time))
            self.speed += 1
            self.speed_x += 4

        spacing_y = self.H_spacing_lines * self.height

        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y
        
        self.current_offset_x += self.current_speed_x * time_factor

class GalaxyGame(App):
    pass

def main():
    GalaxyGame().run()

if __name__=="__main__":
    main()