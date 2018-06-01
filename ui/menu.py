from ui.help import Help
from ui.file import File
from ui.edit import Edit
from control.navigator import Navigator


class Menu(Navigator):
    def __init__(self,std_scr):
        self.std_scr = std_scr
        self.height, self.width = self.std_scr.getmaxyx()
        self.all_menu_states = {"File": File(self.std_scr),"Edit": Edit(self.std_scr),"Help": Help(self.std_scr)}
        self.menu_state = self.all_menu_states["File"]
        self.is_global_state = False

    def left(self):
        self.menu_state.left(menu=self, all_menu_states=self.all_menu_states)

    def right(self):
        self.menu_state.right(menu=self, all_menu_states=self.all_menu_states)

    def up(self):
        self.menu_state.up()

    def down(self):
        self.menu_state.down()

    def run(self):
        self.menu_state.run()

    def set_current_menu_state(self, menu_state):
        self.menu_state = menu_state

    def display(self):
        for state in self.all_menu_states.values():
            if self.is_global_state:
                if state is self.menu_state:
                    state.update_global_status(True)
                else:
                    state.update_global_status(False)
            else:
                state.update_global_status(False)
            state.display()

    def update_global_status(self,status):
        self.is_global_state = status

    def reset_menu_option(self):
        self.menu_state.reset()