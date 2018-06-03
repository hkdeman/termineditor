from curses.textpad import rectangle, Textbox
from helper.functions import CTRL_T, CTRL_B, LEFT, ENTER, UP
import curses
from pathlib import Path


CTRL_X = 24
CTRL_D = 4
BAR_OFFSET = 1
VERTICAL_START_POS = 5
ALT_RIGHT = 558
ALT_LEFT = 543
SHIFT_LEFT = 393
SHIFT_RIGHT = 402
SHIFT_UP = 337
SHIFT_DOWN = 336


class Editor:
    clipboard = ""
    def __init__(self,std_scr, file_path):
        self.std_scr = std_scr
        self.file_path = Path(file_path)
        self.is_global_state = False
        self.number_toolbar_width = 6
        self.height, self.width = self.std_scr.getmaxyx()
        self.origin_x, self.origin_y = self.width//4+self.number_toolbar_width, VERTICAL_START_POS
        self.relative_x, self.relative_y = 0, 0
        self.canvas_height = self.height-1-self.origin_y-1
        self.canvas_width = self.width-2-self.origin_x-1
        self.navigator = None
        self.cursor_x = self.cursor_y = self.last_key_pressed = 0
        self.exit = False
        self.shift_buffer = []
        if self.file_path.exists():
            self.data = open(self.file_path).read().splitlines()
        else:
            self.data = [""]

    def analyser(self):
        if self.last_key_pressed == curses.KEY_UP:
            self.reset_shift_curses()
            if self.cursor_y - self.relative_y == 0 and self.relative_y > 0:
                self.relative_y -= 1
                self.cursor_y = self.cursor_y - 1 if self.cursor_y > 0 else 0
                self.update_number_toolbar()
                self.update_existing_data()
            else:
                self.cursor_y = self.cursor_y - 1 if self.cursor_y > 0 else 0
            if self.data[self.cursor_y]=="":
                self.cursor_x=0
            elif len(self.data[self.cursor_y]) < len(self.data[self.cursor_y+1]) and self.cursor_x > len(self.data[self.cursor_y]):
                # to go to the back of line if the upper line doesn't have many characters
                self.cursor_x = len(self.data[self.cursor_y])
                self.relative_x = self.cursor_x - self.canvas_width + 1 if self.cursor_x > self.canvas_width else 0
                self.update_existing_data()
        elif self.last_key_pressed == SHIFT_UP:
            if self.cursor_y - self.relative_y == 0 and self.relative_y > 0:
                self.relative_y -= 1
                self.cursor_y = self.cursor_y - 1 if self.cursor_y > 0 else 0
                for y in range(self.cursor_y, self.cursor_y+2):
                    for x in range(self.cursor_x, len(self.data[y])):
                        self.shift_buffer = [(y, x)] + self.shift_buffer
                self.update_number_toolbar()
                self.update_existing_data()
            else:
                self.cursor_y = self.cursor_y - 1 if self.cursor_y > 0 else 0
                if self.data[self.cursor_y] == "":
                    self.cursor_x = 0
                elif len(self.data[self.cursor_y]) < len(self.data[self.cursor_y + 1]) and self.cursor_x > len(
                        self.data[self.cursor_y]):
                    # to go to the back of line if the upper line doesn't have many characters
                    self.cursor_x = len(self.data[self.cursor_y])
                    self.relative_x = self.cursor_x - self.canvas_width + 1 if self.cursor_x > self.canvas_width else 0
                    self.update_existing_data()
                start_index = self.cursor_x
                for y in range(self.cursor_y, self.cursor_y+2):
                    end_index = len(self.data[y])
                    if y != self.cursor_y:
                        start_index = 0
                    if end_index == 0:
                        self.shift_buffer = [(y, start_index)] + self.shift_buffer
                    else:
                        for x in range(start_index, end_index):
                            self.shift_buffer = [(y, x)] + self.shift_buffer
                self.update_existing_data()
                if len(self.shift_buffer) > 0:
                    self.navigator.get_curses().curs_set(False)
                return

            if self.data[self.cursor_y]=="":
                self.cursor_x=0
            elif len(self.data[self.cursor_y]) < len(self.data[self.cursor_y+1]) and self.cursor_x > len(self.data[self.cursor_y]):
                # to go to the back of line if the upper line doesn't have many characters
                self.cursor_x = len(self.data[self.cursor_y])
                self.relative_x = self.cursor_x - self.canvas_width + 1 if self.cursor_x > self.canvas_width else 0
                self.update_existing_data()
            if len(self.shift_buffer) > 0:
                self.navigator.get_curses().curs_set(False)
        elif self.last_key_pressed == curses.KEY_DOWN:
            self.reset_shift_curses()
            if len(self.data)-1 > self.cursor_y:
                if self.cursor_y - self.relative_y == self.canvas_height:
                    self.relative_y += 1
                    self.cursor_y = self.cursor_y + 1 if self.cursor_y < len(self.data)-1 else len(self.data)-1
                    self.update_number_toolbar()
                    self.update_existing_data()
                else:
                    self.cursor_y = self.cursor_y + 1 if self.cursor_y < len(self.data)-1 else len(self.data)-1
                    if self.data[self.cursor_y]=="":
                        self.cursor_x=0
                    elif len(self.data[self.cursor_y]) < len(self.data[self.cursor_y-1]) and self.cursor_x > len(self.data[self.cursor_y]):
                        # to go to the back of line if the lower line doesn't have many characters
                        self.cursor_x = len(self.data[self.cursor_y])
                        self.relative_x = self.cursor_x - self.canvas_width + 1 if self.cursor_x > self.canvas_width else 0
                        self.update_existing_data()
        elif self.last_key_pressed == curses.KEY_LEFT:
            self.reset_shift_curses()
            if self.cursor_x > 0:
                self.cursor_x-=1
            elif self.cursor_y>0:
                # go to back of the last line if there is line above and trying to move left
                self.cursor_y -= 1
                self.cursor_x = len(self.data[self.cursor_y])
                if self.cursor_y - self.relative_y <= self.canvas_height-3 and self.relative_y >0:
                    self.relative_y -= 1
                self.relative_x = self.cursor_x - self.canvas_width + 1 if self.cursor_x > self.canvas_width else 0
                self.update_existing_data()

            # check when it comes to more than the window size in x axis
            if self.cursor_x - self.relative_x == self.canvas_width - 4 and self.relative_x > 0:
                self.relative_x -= 1
                self.update_existing_data()
        elif self.last_key_pressed == SHIFT_LEFT:
            if self.cursor_x > 0:
                self.cursor_x -= 1
                point = (self.cursor_y,self.cursor_x)
                if len(self.shift_buffer) > 0 and point == self.shift_buffer[-1]:
                    self.shift_buffer = self.shift_buffer[:-1]
                    self.std_scr.chgat(self.cursor_y+self.origin_y - self.relative_y, self.cursor_x + self.origin_x + BAR_OFFSET - self.relative_x, 1, curses.A_NORMAL)
                else:
                    self.shift_buffer = [point]+self.shift_buffer
                    self.std_scr.chgat(self.cursor_y+self.origin_y - self.relative_y, self.cursor_x + self.origin_x + BAR_OFFSET - self.relative_x, 1, curses.A_REVERSE)
            elif self.cursor_y > 0:
                # go to back of the last line if there is line above and trying to move left
                self.cursor_y -= 1
                self.cursor_x = len(self.data[self.cursor_y])-1
                if len(self.data[self.cursor_y])==0:
                    self.cursor_x += 1
                point = (self.cursor_y, self.cursor_x)
                if len(self.shift_buffer) > 0 and point == self.shift_buffer[-1]:
                    self.shift_buffer = self.shift_buffer[:-1]
                else:
                    self.shift_buffer = [point] + self.shift_buffer
                if self.cursor_y - self.relative_y <= self.canvas_height - 3 and self.relative_y > 0:
                    self.relative_y -= 1
                self.relative_x = self.cursor_x - self.canvas_width + 1 if self.cursor_x > self.canvas_width else 0
                self.update_existing_data()

            # check when it comes to more than the window size in x axis
            if self.cursor_x - self.relative_x == self.canvas_width - 4 and self.relative_x > 0:
                self.relative_x -= 1
                self.update_existing_data()

            if len(self.shift_buffer) > 0:
                self.navigator.get_curses().curs_set(False)
        elif self.last_key_pressed == curses.KEY_RIGHT:
            self.reset_shift_curses()
            if self.cursor_x < len(self.data[self.cursor_y]):
                self.cursor_x+=1
            elif self.cursor_y < len(self.data)-1:
                self.cursor_y+=1
                self.cursor_x=0
                self.relative_x=0
                if self.cursor_y - self.relative_y == self.canvas_height+1:
                    self.relative_y+=1
            if self.cursor_x - self.relative_x == self.canvas_width - 1:
                self.relative_x += 1
            self.update_existing_data()
        elif self.last_key_pressed == SHIFT_RIGHT:
            if self.cursor_x < len(self.data[self.cursor_y]):
                point = (self.cursor_y, self.cursor_x)
                if len(self.shift_buffer) > 0 and point == self.shift_buffer[0]:
                    self.shift_buffer = self.shift_buffer[1:]
                elif self.cursor_x < len(self.data[self.cursor_y]):
                    self.shift_buffer = self.shift_buffer + [point]
                self.cursor_x += 1
            elif self.cursor_y < len(self.data) - 1:
                point = (self.cursor_y, self.cursor_x)
                if len(self.shift_buffer) > 0 and point == self.shift_buffer[0]:
                    self.shift_buffer = self.shift_buffer[1:]
                elif self.cursor_x < len(self.data[self.cursor_y]):
                    self.shift_buffer = self.shift_buffer + [point]
                if self.cursor_y - self.relative_y == self.canvas_height + 1:
                    self.relative_y += 1
                self.cursor_y += 1
                self.cursor_x = 0
                self.relative_x = 0
            if self.cursor_x - self.relative_x == self.canvas_width - 1:
                self.relative_x += 1
            self.update_existing_data()
            if len(self.shift_buffer) > 0:
                self.navigator.get_curses().curs_set(False)
        elif 32 <= self.last_key_pressed <= 126:
            y, x = self.cursor_y+self.origin_y-self.relative_y, self.cursor_x+self.origin_x+BAR_OFFSET-self.relative_x
            self.data[self.cursor_y]= self.data[self.cursor_y][:self.cursor_x]+chr(self.last_key_pressed)+self.data[self.cursor_y][self.cursor_x:]

            # when add more characters, it needs to simulate a horizontal scroll
            if self.cursor_x - self.relative_x == self.canvas_width-1:
                self.relative_x+=1
            self.update_existing_data()

            # update the cursors
            self.cursor_x += 1
        elif self.last_key_pressed == ENTER:
            # shorten the line of cursor at y
            y,x = self.cursor_y+self.origin_y-self.relative_y,self.origin_x+self.cursor_x-self.relative_x
            buffer_end_line = self.data[self.cursor_y][self.cursor_x:]

            self.data[self.cursor_y] = self.data[self.cursor_y][:self.cursor_x]
            self.data = self.data[:self.cursor_y + 1] + [buffer_end_line] + self.data[self.cursor_y + 1:]
            self.std_scr.addstr(y, x + 1, " " * len(buffer_end_line))
            if self.cursor_y-self.relative_y<self.canvas_height-1:
                self.std_scr.addstr(y + 1, self.origin_x + BAR_OFFSET, self.data[self.cursor_y + 1])

            if self.cursor_y - self.relative_y == self.canvas_height:
                self.relative_y += 1

            self.cursor_y += 1
            self.cursor_x = 0
            self.relative_x = 0
            self.update_existing_data()
            self.update_number_toolbar()
        elif self.last_key_pressed == curses.KEY_BACKSPACE:
            if self.cursor_x == 0:
                if len(self.data[self.cursor_y]) > 0:
                    self.data[self.cursor_y] = self.data[self.cursor_y][:-1]
                elif self.cursor_y > 0:
                    # delete the line as it contains nothing
                    del self.data[self.cursor_y]
                    if self.cursor_y - self.relative_y <= self.canvas_height-3 and self.relative_y > 0:
                        self.relative_y -= 1
                    self.cursor_y = self.cursor_y - 1 if self.cursor_y > 0 else 0
                    self.cursor_x = len(self.data[self.cursor_y])
                    self.relative_x = self.cursor_x - self.canvas_width+1 if self.cursor_x > self.canvas_width else 0
                    self.update_number_toolbar()
                    self.update_existing_data()
            else:
                self.std_scr.addstr(self.cursor_y+self.origin_y, self.origin_x+BAR_OFFSET," "*self.canvas_width)
                self.data[self.cursor_y] = self.data[self.cursor_y][:self.cursor_x][:-1] \
                                           + self.data[self.cursor_y][self.cursor_x:]
                self.std_scr.addstr(self.cursor_y+self.origin_y, self.origin_x+BAR_OFFSET,
                                    self.data[self.cursor_y][self.relative_x:self.relative_x+self.canvas_width])
                self.cursor_x = self.cursor_x - 1 if self.cursor_x > 0 else 0

            if self.cursor_x - self.relative_x <= self.canvas_width-4 and self.relative_x > 0:
                self.relative_x -= 1
                self.update_existing_data()
        elif self.last_key_pressed == CTRL_X:
            import sys
            sys.exit(0)
        elif self.last_key_pressed == ALT_LEFT:
            self.previous_tab()
        elif self.last_key_pressed == ALT_RIGHT:
            self.next_tab()

    def empty_number_toolbar(self):
        y, x = self.origin_y, self.origin_x-self.number_toolbar_width+1
        for i in range(self.canvas_height+1):
            self.std_scr.addstr(y+i,x," "*(self.number_toolbar_width-1))

    def empty_canvas(self):
        y, x = self.origin_y, self.origin_x+BAR_OFFSET
        for i in  range(self.canvas_height+1):
            self.std_scr.addstr(y+i,x," "*(self.canvas_width))

    def update_number_toolbar(self):
        self.empty_number_toolbar()
        y,x = self.origin_y-self.relative_y, self.origin_x-self.number_toolbar_width+1
        height_index = 0
        line_num = self.relative_y
        while line_num < len(self.data):
            self.std_scr.addstr(y+line_num,x,str(line_num+1))
            self.std_scr.addstr(y+line_num,x+self.number_toolbar_width-2,"|")
            line_num += 1
            if height_index == self.canvas_height:
                break
            else:
                height_index += 1

    def update_shift_buffer_highlighting(self):
        for char in self.shift_buffer:
            if 0 <= char[0] - self.relative_y < self.canvas_height and 0 <= char[1] - self.relative_x < self.canvas_width:
                y, x = self.origin_y+char[0]-self.relative_y, self.origin_x+char[1]+BAR_OFFSET-self.relative_x
                if len(self.data[char[0]]) == 0 or char[1] == len(self.data[char[0]])-1 and self.shift_buffer[-1] != char:
                    # last character to be able to get full line
                    self.std_scr.chgat(y, x, self.canvas_width - x + self.origin_x, curses.A_REVERSE)
                else:
                    self.std_scr.chgat(y, x , 1, curses.A_REVERSE)

    def update_existing_data(self):
        self.empty_canvas()
        y,x = self.origin_y-self.relative_y, self.origin_x+BAR_OFFSET
        height_index = 0
        line_num = self.relative_y
        while line_num < len(self.data):
            self.std_scr.addstr(line_num+y,x,self.data[line_num][self.relative_x:self.relative_x+self.canvas_width])
            line_num += 1
            if height_index == self.canvas_height:
                break
            else:
                height_index += 1

        self.update_shift_buffer_highlighting()

    def edit(self):
        self.update_existing_data()
        while not self.exit:
            self.update_number_toolbar()
            self.std_scr.move(self.origin_y+self.cursor_y-self.relative_y,self.origin_x+self.cursor_x-self.relative_x+BAR_OFFSET)
            self.last_key_pressed = self.std_scr.getch()
            self.analyser()

    def update_global_status(self,status):
        self.is_global_state = status

    def left(self):
        if self.cursor_x==0:
            self.go_to_explorer()

    def right(self):
        pass

    def up(self):
        if self.cursor_y == 0:
            self.go_to_menu()

    def down(self):
        pass

    def set_navigator(self,navigator):
        self.navigator = navigator

    def go_to_menu(self):
        self.navigator.set_current_state(self.navigator.context["Menu"])
        self.exit = True

    def go_to_explorer(self):
        self.navigator.set_current_state(self.navigator.context["Explorer"])
        self.exit = True

    def display(self):
        self.empty_canvas()
        self.empty_number_toolbar()
        rectangle(self.std_scr,self.origin_y-1,self.origin_x-self.number_toolbar_width-1,
                  self.height-1,self.width-2)
        self.std_scr.refresh()
        if self.is_global_state:
            self.edit()
        else:
            self.update_existing_data()
            self.update_number_toolbar()

    def set_exit(self, exit):
        self.exit = exit

    def __len__(self):
        return len(self.file_path)

    def get_file_name(self):
        return str(self.file_path)

    def next_tab(self):
        self.navigator.context["Manager"].right()
        self.exit = True
        self.navigator.context["Explorer"].get_editor_manager().show_content()
        self.navigator.context["Manager"].reset_and_display()

    def previous_tab(self):
        self.navigator.context["Manager"].left()
        self.exit = True
        self.navigator.context["Explorer"].get_editor_manager().show_content()
        self.navigator.context["Manager"].reset_and_display()

    def reset_shift_curses(self):
        self.shift_buffer = []
        self.navigator.get_curses().curs_set(True)
        self.update_existing_data()