from navigator import Navigator
from helper import check_navigation
from curses import wrapper
from menu import Menu
from explorer import Explorer
from editor import Editor

CTRL_X = 24

def main(std_scr):
    last_key_pressed = 0
    context = {"Menu":Menu(),"Explorer":Explorer(),"Editor":Editor()}
    navigator = Navigator(std_scr=std_scr,context=context)

    while last_key_pressed!=CTRL_X:
        std_scr.clear()
        navigator.display_all_states()
        std_scr.refresh()
        last_key_pressed = std_scr.getch()
        check_navigation(navigator, last_key_pressed)

if __name__ == '__main__':
    wrapper(main)