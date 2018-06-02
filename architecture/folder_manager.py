from curses.textpad import rectangle
import curses


ORIGIN_Y, ORIGIN_X = 5,2


class FolderManager:
    def __init__(self,std_scr):
        self.std_scr = std_scr
        self.height, self.width = self.std_scr.getmaxyx()
        self.origin_y, self.origin_x = 5, 2
        self.canvas_height, self.canvas_width = self.height-1, self.width//4-4
        self.is_global_state = False
        self.navigator = None

    def left(self):
        self.current_state.left()

    def right(self):
        self.current_state.right()

    def up(self):
        self.current_state.up()

    def down(self):
        self.current_state.down()

    def run(self):
        self.current_state.run()

    def display(self):
        pass

    def update_global_status(self,status):
        self.is_global_state = status

    def set_navigator(self, navigator):
        self.navigator = navigator