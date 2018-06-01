from curses.textpad import rectangle
from control.navigator import Navigator
from helper.functions import populate_positions, highlight


ORIGIN_X,ORIGIN_Y = 2,0


class Edit(Navigator):
    def __init__(self, std_scr):
        self.std_scr = std_scr
        self.fixed_x = 16
        self.max_options = 5
        self.all_options = {"Edit": 0,"Copy": 1, "Cut": 2, "Paste": 3, "Select All": 4, "Toggle Comments": 5}
        self.all_options_display_names = dict((y, x) for x, y in self.all_options.items())
        self.positions = populate_positions(self.fixed_x,self.all_options,ORIGIN_X,ORIGIN_Y)
        self.current_option = self.all_options["Edit"]
        self.hidden = True
        self.is_global_state = False

    @staticmethod
    def left(menu, all_menu_states):
        menu.set_current_menu_state(all_menu_states["File"])
        menu.reset_menu_option()

    @staticmethod
    def right(menu, all_menu_states):
        menu.set_current_menu_state(all_menu_states["Help"])
        menu.reset_menu_option()

    def up(self):
        self.set_current_option(self.current_option - 1 if self.current_option > 0 else self.current_option)
        if self.current_option == 0:
            self.hide()

    def down(self):
        if self.current_option == 0:
            self.show()
        self.set_current_option(self.current_option + 1 if self.current_option < self.max_options
                                else self.current_option)

    def set_current_option(self,current_option):
        self.current_option = current_option

    def display(self):
        self.std_scr.addstr(self.positions[self.all_options["Edit"]]["y"],
                            self.positions[self.all_options["Edit"]]["x"], "Edit")
        rectangle(self.std_scr, 0 + ORIGIN_Y, self.fixed_x-4 + ORIGIN_X, 2 + ORIGIN_Y, self.fixed_x+8+ ORIGIN_X)
        if self.is_global_state:
            if not self.hidden:
                for item in self.positions:
                    self.std_scr.addstr(self.positions[item]["y"],
                                        self.positions[item]["x"], self.all_options_display_names[item])
                rectangle(self.std_scr, 2 + ORIGIN_Y, self.fixed_x-4 + ORIGIN_X, self.max_options*2+2 + ORIGIN_Y, self.fixed_x+16+ ORIGIN_X)
            highlight(self.std_scr, self.positions[self.current_option]["y"], self.positions[self.current_option]["x"],
                      self.all_options_display_names[self.current_option])

    def run(self):
        if self.current_option == 0:
            if self.hidden:
                self.show()
            else:
                self.hide()
        else:
            # need to perform the specific task based on the option selected aka switch cases
            pass

    def show(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    def update_global_status(self,status):
        self.is_global_state = status

    def reset(self):
        self.current_option = self.all_options["Edit"]