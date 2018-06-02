from curses.textpad import rectangle
import curses


ORIGIN_Y, ORIGIN_X = 5,2


class EditorManager:
    def __init__(self,std_scr):
        self.std_scr = std_scr
        self.height, self.width = self.std_scr.getmaxyx()
        self.origin_y, self.origin_x = 5, 2
        self.canvas_height, self.canvas_width = self.height//4-1, self.width//4-4
        self.all_editors = {}
        self.is_global_state = False
        self.navigator = None
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def left(self):
        pass

    def right(self):
        pass

    def up(self):
        pass

    def down(self):
        pass

    def run(self):
        pass

    def show_title(self):
        self.std_scr.addstr(self.origin_y, self.origin_x+1, "Open Editors")
        self.std_scr.addstr(self.origin_y, self.canvas_width-3, "▼")
        rectangle(self.std_scr, self.origin_y - 1, self.origin_x - 1, self.origin_y + 1, self.width // 4 - 4)

    def show_content(self):
        self.all_editors = {}
        for i, editor in enumerate(self.navigator.context["Manager"].get_all_editor_names()):
            self.all_editors[i] = editor
        rectangle(self.std_scr, self.origin_y+1,self.origin_x-1,self.canvas_height, self.canvas_width)
        for i, editor in self.all_editors.items():
            if i==0:
                self.std_scr.addstr(self.origin_y + i + 2, self.origin_x + 1, editor, curses.color_pair(2))
            else:
                self.std_scr.addstr(self.origin_y+i+2, self.origin_x+1, editor)

    def display(self):
        self.show_title()
        self.show_content()

    def update_global_status(self,status):
        self.is_global_state = status

    def set_navigator(self, navigator):
        self.navigator = navigator