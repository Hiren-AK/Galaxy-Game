from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

class MainWidget(Widget):
    perspectivePointX = NumericProperty(0)
    perspectivePointY = NumericProperty(0)
    V_num_lines = 6
    V_spacing_lines = 0.2       #10% of screen width
    vertical_lines = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
    
    def on_parent(self, widget, parent):
        pass

    def on_size(self, *args):
        self.update_verticle_lines()

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
            x_line = int(x_center_line + offset*spacing)
            x1, y1 = self.transform(x_line, 0)
            x2, y2 = self.transform(x_line, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

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
        y_proportion = diff_y/self.perspectivePointY
        x_transformation = self.perspectivePointX + (diff_x * y_proportion)
        return int(x_transformation), int(y_transformation)

class GalaxyGame(App):
    pass

def main():
    GalaxyGame().run()
  
if __name__=="__main__":
    main()