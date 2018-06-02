from helper.functions import check_navigation
from curses import wrapper
from ui.menu import Menu
from explorer import Explorer
# from canvas.editor import Editor
from canvas.manager import Manager
from termineditor import Termineditor
import curses

CTRL_X = 24


def main(std_scr):
    last_key_pressed = 0
    files = ["Untitled.txt","Untitled(1).txt","Untitled(2).txt"]
    context = {"Menu": Menu(std_scr),"Explorer": Explorer(std_scr),"Manager": Manager(std_scr,files)}
    navigator = Termineditor(std_scr=std_scr,context=context,current_state=context["Manager"])

    while last_key_pressed!=CTRL_X:
        std_scr.clear()
        navigator.display_all_states()
        if not navigator.get_last_came_from() is context["Manager"]:
            last_key_pressed = std_scr.getch()
        else:
            curses.curs_set(False)
            navigator.set_last_came_from(None)
        check_navigation(navigator, last_key_pressed,curses)
        if navigator.get_current_state() is context["Manager"]:
            curses.curs_set(True)

if __name__ == '__main__':
    wrapper(main)