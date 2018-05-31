from navigator import Navigator
import curses

class Menu(Navigator):
    def __init__(self):
        self.all_menu_states = {"File": File(),"Edit": Edit(),"Help": Help()}
        self.menu_state = self.all_menu_states["File"]
        super().__init__()

    def left(self):
        self.menu_state.left()

    def right(self):
        self.menu_state.right()

    def up(self):
        pass

    def down(self):
        self.menu_state.expand()

    def run(self):
        self.menu_state.run()

    def display(self):
        for state in self.all_menu_states:
            state.display()
        # draw line under options

        self.std_scr.hline(1,0,curses.A_UNDERLINE,self.width-1)

    def set_current_menu_state(self, menu_state):
        self.menu_state = menu_state


class File(Menu):
    def __init__(self):
        self.all_options = {"File": 0,"Open": 1,"Open Folder": 2,"Save": 3,"Save As": 4}
        self.current_option = self.all_options["File"]
        self.hidden = True
        super().__init__()

    def left(self):
        pass

    def right(self):
        self.set_current_menu_state(Edit)

    def up(self):
        self.set_current_option(self.current_option-1 if self.current_option > 0 else self.current_option)
        if self.current_option == 0:
            self.hide()

    def down(self):
        self.set_current_state(self.current_option+1 if self.current_option < 4 else self.current_option)

    def set_current_option(self,current_option):
        self.current_option = current_option

    def run(self):
        if self.current_state == 0:
            if self.hidden:
                self.show()
            else:
                self.hide()
        else:
            # need to perform the specific task based on the option selected aka switch cases
            pass

    def expand(self):
        if self.hidden:
            self.show()

    def show(self):
        self.hidden = False
        pass

    def hide(self):
        self.hidden = True
        pass

    def display(self):
        pass


class Edit(Menu):
    def __init__(self):
        super().__init__()

    def left(self):
        self.set_current_menu_state(File)

    def right(self):
        self.set_current_menu_state(Help)

    def display(self):
        pass


class Help(Menu):
    def __init__(self):
        super().__init__()

    def left(self):
        self.set_current_menu_state(Edit)

    def right(self):
        pass

    def display(self):
        pass