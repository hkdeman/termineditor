from curses.textpad import rectangle
from canvas.editor import Editor
import curses

PADDING = 3
LINE_HEIGHT = 1
VERTICAL_START_POS = 3

class Manager:
    def __init__(self, std_scr, files):
        self.std_scr = std_scr
        self.height, self.width = self.std_scr.getmaxyx()
        self.origin_x, self.origin_y = self.width//4-1, VERTICAL_START_POS
        self.editors_length = len(files)
        self.all_editors = {}
        for i, file in enumerate(files):
            self.all_editors[i] = Editor(self.std_scr, file)
        self.all_editors_display_names = dict((y.get_file_name(),x) for x,y in self.all_editors.items())
        self.current_editor = 0 if self.editors_length!=0 else None
        self.navigator = None
        self.is_global_state = False
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)

    def right(self):
        self.current_editor = self.current_editor + 1 if self.current_editor < self.editors_length else max(self.all_editors.keys())

    def left(self):
        self.current_editor = self.current_editor - 1 if self.current_editor > 0 else 0

    def up(self):
        pass

    def down(self):
        pass

    def run(self):
        pass

    def show_all_headers(self):
        total_sum_x = 0
        active_total_sum_x = 0
        for i, file_name in enumerate(self.all_editors_display_names):
            if self.all_editors_display_names[file_name] == self.current_editor:
                active_total_sum_x = total_sum_x
                total_sum_x += PADDING * 2 + len(file_name)
                continue
            rectangle(self.std_scr,self.origin_y-1,self.origin_x+total_sum_x,
                      self.origin_y+1,self.origin_x+total_sum_x+PADDING*2+len(file_name))
            self.std_scr.addstr(self.origin_y,self.origin_x+total_sum_x+PADDING,file_name+" ×")
            total_sum_x += PADDING*2+len(file_name)

        # draw the active so it looks active
        current_file_name = self.all_editors[self.current_editor].get_file_name()
        rectangle(self.std_scr, self.origin_y - 1, self.origin_x + active_total_sum_x,
                  self.origin_y + 1, self.origin_x + active_total_sum_x + PADDING * 2 + len(current_file_name))
        self.std_scr.addstr(self.origin_y, self.origin_x + active_total_sum_x + PADDING, current_file_name + " ×",
                            curses.color_pair(1))

    def display(self):
        self.show_all_headers()
        if self.is_global_state:
            self.all_editors[self.current_editor].update_global_status(True)
        else:
            self.all_editors[self.current_editor].update_global_status(False)
        self.all_editors[self.current_editor].display()

    def set_navigator(self, navigator):
        self.navigator = navigator

    def update_global_status(self, state):
        self.is_global_state = state