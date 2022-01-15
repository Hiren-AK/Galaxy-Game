from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

class MainWidget(Widget):
    perspectivePointX = NumericProperty(0)
    perspectivePointY = NumericProperty(0)
    V_num_lines = 9
    V_spacing_lines = 0.1       #10% of screen width
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
        offset = -int(self.V_num_lines/2)
        spacing = self.V_spacing_lines * self.width
        for i in range(self.V_num_lines):
            x_line = int(x_center_line + offset*spacing)
            self.vertical_lines[i].points = [x_line, 0, x_line, self.height]
            offset += 1

class GalaxyGame(App):
    pass

def main():
    GalaxyGame().run()
  
if __name__=="__main__":
    main()