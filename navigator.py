from menu import Menu
from explorer import Explorer
from editor import Editor


class Navigator:
    def __init__(self,std_scr,context,current_state=Menu):
        self.std_scr = std_scr
        height, width = self.std_scr.getmaxyx()
        self.height = height
        self.width = width
        self.context = context
        self.current_state = current_state()

    def set_current_state(self,current_state):
        self.current_state = current_state()

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

    def display_all_states(self):
        for state in self.all_states.values():
            state.display()