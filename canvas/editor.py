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
            self.cursor_y = self.cursor_y-1 if self.cursor_y > 0 else 0
        elif self.last_key_pressed == curses.KEY_DOWN:
            if len(self.data)-1>self.cursor_y:
                self.cursor_y += 1
        elif self.last_key_pressed == curses.KEY_LEFT:
            self.cursor_x = self.cursor_x-1 if self.cursor_x > 0 else 0
        elif self.last_key_pressed == curses.KEY_RIGHT:
            self.cursor_x+=1
        elif 32 <= self.last_key_pressed <= 126:
            self.data[self.cursor_y]= self.data[self.cursor_y][:self.cursor_x]+chr(self.last_key_pressed)+self.data[self.cursor_y][self.cursor_x:]
            self.std_scr.addstr(self.cursor_y+self.origin_y,self.cursor_x+self.origin_x+BAR_OFFSET,self.data[self.cursor_y][self.cursor_x:])
            # update the cursors
            self.cursor_x += 1
        elif self.last_key_pressed == ENTER:

            self.cursor_y+=1
            self.cursor_x=0
            # y,x = self.cursor_y+self.origin_y, self.cursor_x+self.origin_x
            #
            # #THIS IS SO MUUCH FUNNNNNNNNNNN
            # # New line add the string and clear next lines and add characters respectively
            # for i,line in enumerate(self.data[self.cursor_y:]):
            #     self.std_scr.addstr(y+i+1,x," "*len(line))
            #     self.std_scr.addstr(y+i+2,x,self.data[self.cursor_y+i])
            #
            # self.data = self.data[:self.cursor_y]+[""]+self.data[self.cursor_y:]

            if len(self.data)-1<self.cursor_y:
                self.data.append("")
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

    def update_number_toolbar(self):
        y,x = self.origin_y, self.origin_x-self.number_toolbar_width+1
        for line_num in range(self.cursor_y+1):
            self.std_scr.addstr(y+line_num,x,str(line_num+1))
            self.std_scr.addstr(y+line_num,x+self.number_toolbar_width-2,"|")


    def edit(self):
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

    def go_to_explorer(self):
        self.navigator.set_current_state(self.navigator.context["Explorer"])

    def display(self):
        rectangle(self.std_scr,3,self.width//4,self.height-1,self.width-2)
        self.std_scr.refresh()
        if self.is_global_state:
            self.edit()