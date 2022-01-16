from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.core.window import Window
from kivy.properties import Clock
from kivy import platform
from kivy.graphics.vertex_instructions import Quad
from kivy.graphics.vertex_instructions import Triangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from random import randint
import time

Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    menu_widget = ObjectProperty()
    perspectivePointX = NumericProperty(0)
    perspectivePointY = NumericProperty(0)
    V_num_lines = 14
    V_spacing_lines = 0.3       #30% of screen width
    vertical_lines = []
    H_num_lines = 10
    H_spacing_lines = 0.2       #20% of screen height
    horizontal_lines = []
    current_offset_y = 0
    current_y_loop = 0
    speed = 4
    start_time = None
    current_speed_x = 0
    speed_x = 10
    current_offset_x = 0

    space_ship = None
    ship_width = 0.07
    ship_height = 0.05
    ship_gap = 0.05
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    num_tiles = 13
    tiles = []
    tile_coordinates = []

    game_over = False
    game_started = False

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.start_tiles()
        self.init_tiles()
        self.init_space_ship()
        self.tile_coordinate_generator()
        self.start_time = time.time()

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

    def init_space_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.space_ship = Triangle()
    
    def update_space_ship(self):
        center_x = self.width/2
        base_y = self.ship_gap * self.height
        half_ship_width = (self.ship_width * self.width) / 2
        ship_height = self.ship_height * self.height
        
        x1, y1 = self.transform(center_x - half_ship_width, base_y)
        x2, y2 = self.transform(center_x, base_y + ship_height)
        x3, y3 = self.transform(center_x + half_ship_width, base_y)

        self.ship_coordinates[0] = (x1, y1)
        self.ship_coordinates[1] = (x2, y2)
        self.ship_coordinates[2] = (x3, y3)

        self.space_ship.points = [x1, y1, x2, y2, x3, y3]

    def on_size(self, *args):
        self.update_verticle_lines()
        self.update_horizontal_lines()
    
    def check_collison_tiles(self):
        for i in range(0, len(self.tile_coordinates)):
            x_tile, y_tile = self.tile_coordinates[i]
            if y_tile > self.current_y_loop + 1:
                return False
            if self.check_collision(x_tile, y_tile):
                return True
        
        return False

    def check_collision(self, tile_x, tile_y):
        x_min, y_min = self.get_tile_coordinates(tile_x, tile_y)
        x_max, y_max = self.get_tile_coordinates(tile_x + 1, tile_y + 1)

        for i in range(0, 3):
            x_coor, y_coor = self.ship_coordinates[i]
            if (x_coor >= x_min and x_coor <= x_max) and (y_coor >= y_min and y_coor <= y_max):
                return True
        
        return False

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.num_tiles):
                self.tiles.append(Quad())
    
    def start_tiles(self):
        for i in range(0, 4):
            self.tile_coordinates.append((0, i))

    def tile_coordinate_generator(self):
        last_x = 0
        last_y = 0
        for i in range(len(self.tile_coordinates)-1, -1, -1):
            if self.tile_coordinates[i][1] < self.current_y_loop:
                del self.tile_coordinates[i]

        if len(self.tile_coordinates) > 0:
            last_coordinates = self.tile_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1


        for i in range(len(self.tile_coordinates)-1, self.num_tiles):
            rand = randint(-1, 1)
            start_index = -int(self.V_num_lines/2) + 1
            end_index = start_index + self.V_num_lines - 2

            if last_x <= start_index:
                rand = 1
            elif last_x >= end_index:
                rand = -1

            self.tile_coordinates.append((last_x, last_y))
            if rand == 1:
                last_x += 1
                self.tile_coordinates.append((last_x, last_y))
                last_y += 1
                self.tile_coordinates.append((last_x, last_y))
            elif rand == -1:
                last_x -= 1
                self.tile_coordinates.append((last_x, last_y))
                last_y += 1
                self.tile_coordinates.append((last_x, last_y))
            last_y += 1

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_num_lines):
                self.vertical_lines.append(Line())

    def get_line_x(self, index):
        x_center_line = self.perspectivePointX
        offset = index - 0.5
        spacing = self.V_spacing_lines * self.width
        line_x = x_center_line + (offset * spacing) + self.current_offset_x
        return line_x
    
    def get_line_y(self, index):
        spacing_y = self.H_spacing_lines * self.height
        y_line = index * spacing_y - self.current_offset_y
        return y_line

    def get_tile_coordinates(self, tile_x, tile_y):
        tile_y = tile_y - self.current_y_loop
        x = self.get_line_x(tile_x)
        y = self.get_line_y(tile_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.num_tiles):
            tile = self.tiles[i]
            tile_coordinate = self.tile_coordinates[i]
            x_min, y_min = self.get_tile_coordinates(tile_coordinate[0], tile_coordinate[1])
            x_max, y_max = self.get_tile_coordinates(tile_coordinate[0] + 1, tile_coordinate[1] + 1)
            
            x1, y1  = self.transform(x_min, y_min)
            x2, y2 = self.transform(x_min, y_max)
            x3, y3 = self.transform(x_max, y_max)
            x4, y4 = self.transform(x_max, y_min)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

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
            y_line = (i * spacing_y) - self.current_offset_y
            x1, y1 = self.transform(x_min, y_line)
            x2, y2 = self.transform(x_max, y_line)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def transform(self, x, y):
        return self.transform_perspective(x, y)

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
        if not self.game_over and self.game_started:
            if touch.x < self.width/2:
                self.current_speed_x = self.speed_x
            else:
                self.current_speed_x = -self.speed_x
        
        return super(RelativeLayout, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        self.current_speed_x = 0
    
    def update(self, dt):
        self.update_horizontal_lines()
        self.update_verticle_lines()
        self.update_tiles()
        self.update_space_ship()
        time_factor = dt * 60

        if not self.game_over and self.game_started:
            speed_y = (self.speed * self.height)/1000
            self.current_offset_y += speed_y * time_factor

            if((time.time() - self.start_time) > 15 and self.speed < 5):
                self.start_time = time.time()
                self.speed += 1
                self.speed_x += 1

            spacing_y = self.H_spacing_lines * self.height

            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.tile_coordinate_generator()
        
            speed_x = (self.current_speed_x * self.width)/1000
            self.current_offset_x += speed_x * time_factor

        if not self.check_collison_tiles() and not self.game_over:
            self.game_over = True
    
    def on_menu_button_pressed(self):
        print("button") 
        self.game_started = True  
        self.menu_widget.opacity = 0

class GalaxyGame(App):
    pass

def main():
    GalaxyGame().run()

if __name__=="__main__":
    main()