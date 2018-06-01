from curses.textpad import rectangle, Textbox
from helper.functions import CTRL_T, CTRL_B, LEFT, ENTER, UP
import curses


CTRL_X = 24
CTRL_D = 4
BAR_OFFSET = 1

class Editor:
    def __init__(self,std_scr):
        self.std_scr = std_scr
        self.is_global_state = False
        self.number_toolbar_width = 6
        self.height, self.width = self.std_scr.getmaxyx()
        self.origin_x, self.origin_y = self.width//4+self.number_toolbar_width, 4
        self.canvas_height = self.height-1-self.origin_y-1
        self.canvas_width = self.width-2-self.origin_x-1
        self.navigator = None
        self.cursor_x = self.cursor_y = self.last_key_pressed = 0
        self.exit = False
        self.data = [""]

    def analyser(self):
        if self.last_key_pressed == curses.KEY_UP:
            self.cursor_y = self.cursor_y-1 if self.cursor_y >=0 else -1
            if self.cursor_y == -1:
                self.go_to_menu()
                return
            if self.data[self.cursor_y]=="":
                self.cursor_x=0
            elif len(self.data[self.cursor_y]) < len(self.data[self.cursor_y+1]):
                # to go to the back of line if the upper line doesn't have many characters
                self.cursor_x = len(self.data[self.cursor_y])
        elif self.last_key_pressed == curses.KEY_DOWN:
            if len(self.data)-1>self.cursor_y:
                self.cursor_y += 1
                if self.data[self.cursor_y]=="":
                    self.cursor_x=0
                elif len(self.data[self.cursor_y]) < len(self.data[self.cursor_y-1]):
                    # to go to the back of line if the lower line doesn't have many characters
                    self.cursor_x = len(self.data[self.cursor_y])
        elif self.last_key_pressed == curses.KEY_LEFT:
            if self.cursor_x > 0:
                self.cursor_x-=1
            elif self.cursor_y>0:
                # go to back of the last line if there is line above and trying to move left
                self.cursor_y-=1
                self.cursor_x = len(self.data[self.cursor_y])
        elif self.last_key_pressed == curses.KEY_RIGHT:
            if self.cursor_x < len(self.data[self.cursor_y]):
                self.cursor_x+=1
            elif self.cursor_y < len(self.data)-1:
                self.cursor_y+=1
                self.cursor_x=0
        elif 32 <= self.last_key_pressed <= 126:
            self.data[self.cursor_y]= self.data[self.cursor_y][:self.cursor_x]+chr(self.last_key_pressed)+self.data[self.cursor_y][self.cursor_x:]
            self.std_scr.addstr(self.cursor_y+self.origin_y,self.cursor_x+self.origin_x+BAR_OFFSET,self.data[self.cursor_y][self.cursor_x:])
            # update the cursors
            self.cursor_x += 1
        elif self.last_key_pressed == ENTER:
            # shorten the line of cursor at y
            y,x = self.cursor_y+self.origin_y,self.origin_x+self.cursor_x
            buffer_end_line = self.data[self.cursor_y][self.cursor_x:]

            # empty the next lines to easily refresh them
            for i in range(self.cursor_y+1,len(self.data)):
                self.std_scr.addstr(i+self.origin_y,self.origin_x+BAR_OFFSET," "*len(self.data[i]))

            self.data[self.cursor_y] = self.data[self.cursor_y][:self.cursor_x]
            self.data = self.data[:self.cursor_y+1]+[buffer_end_line]+self.data[self.cursor_y+1:]
            self.std_scr.addstr(y,x+1," "*len(buffer_end_line))
            self.std_scr.addstr(y+1,self.origin_x+BAR_OFFSET,self.data[self.cursor_y+1])
            # delete below the cursor y
            self.cursor_y += 1
            for i in range(self.cursor_y,len(self.data)):
                self.std_scr.addstr(i+self.origin_y,self.origin_x+BAR_OFFSET,self.data[i])
            self.update_number_toolbar()
            self.cursor_x = 0
        elif self.last_key_pressed == curses.KEY_BACKSPACE:
            if self.cursor_x==0:
                if len(self.data[self.cursor_y]) > 0:
                    self.data[self.cursor_y] = self.data[self.cursor_y][:-1]
                if self.cursor_y > 0:
                    # check if y is last and then delete to update the right numbering in the number toolbar
                    if self.cursor_y == len(self.data)-1:
                        y, x = self.origin_y+len(self.data)-1, self.origin_x-self.number_toolbar_width+1
                        for i in range(self.number_toolbar_width):
                            self.std_scr.addstr(y,x+i," ")
                        self.data = self.data[:-1]
                    self.std_scr.addstr(self.cursor_y+self.origin_y, self.cursor_x+self.origin_x," ")
                    self.cursor_y-=1
                    self.cursor_x = len(self.data[self.cursor_y])
            else:
                self.data[self.cursor_y] = self.data[self.cursor_y][:-1]
                self.std_scr.addch(self.cursor_y + self.origin_y, self.cursor_x + self.origin_x, " ")
                self.cursor_x-=1
        elif self.last_key_pressed == CTRL_X:
            import sys
            sys.exit(0)

    def update_number_toolbar(self):
        y,x = self.origin_y, self.origin_x-self.number_toolbar_width+1
        for line_num in range(len(self.data)):
            self.std_scr.addstr(y+line_num,x,str(line_num+1))
            self.std_scr.addstr(y+line_num,x+self.number_toolbar_width-2,"|")

    def update_existing_data(self):
        for y in range(len(self.data)):
            self.std_scr.addstr(y+self.origin_y,self.origin_x+BAR_OFFSET,self.data[y])


    def edit(self):
        self.update_existing_data()
        while not self.exit:
            self.update_number_toolbar()
            self.std_scr.move(self.origin_y+self.cursor_y,self.origin_x+self.cursor_x+BAR_OFFSET)
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
        rectangle(self.std_scr,3,self.width//4,self.height-1,self.width-2)
        self.std_scr.refresh()
        if self.is_global_state:
            self.edit()
        else:
            self.update_existing_data()
            self.update_number_toolbar()

    def set_exit(self,exit):
        self.exit = exit

    def reset(self):
        if self.cursor_y == -1:
            self.cursor_y=0
        self.set_exit(False)