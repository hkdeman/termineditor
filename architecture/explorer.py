from curses.textpad import rectangle
import curses
from architecture.editor_manager import EditorManager
from architecture.folder_manager import FolderManager


ORIGIN_Y, ORIGIN_X = 5,2


class Explorer:
    def __init__(self,std_scr):
        self.std_scr = std_scr
        self.height, self.width = self.std_scr.getmaxyx()
        self.origin_y, self.origin_x = 5, 2
        self.canvas_height, self.canvas_width = self.height-1, self.width//4-4
        self.is_global_state = False
        self.navigator = None
        self.all_states = {0: EditorManager(std_scr), 1: FolderManager(std_scr)}
        self.current_state = 0

    def left(self):
        self.all_states[self.current_state].left()

    def right(self):
        self.all_states[self.current_state].right()

    def up(self):
        self.all_states[self.current_state].up()

    def down(self):
        self.all_states[self.current_state].down()

    def run(self):
        self.all_states[self.current_state].run()

    def display(self):
        for state in self.all_states:
            if self.current_state == state:
                self.all_states[state].update_global_status(True)
            else:
                self.all_states[state].update_global_status(False)
            self.all_states[state].display()

    def update_global_status(self,status):
        self.is_global_state = status

    def set_navigator(self, navigator):
        self.navigator = navigator
        for state in self.all_states:
            self.all_states[state].set_navigator(navigator)