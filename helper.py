import curses
from explorer import Explorer
from editor import Editor
from menu import Menu

CTRL_B = 2
CTRL_E = 5
CTRL_T = 20

def check_navigation(navigator,last_key_pressed):
    if last_key_pressed == curses.KEY_UP:
        navigator.up()
    elif last_key_pressed == curses.KEY_DOWN:
        navigator.down()
    elif last_key_pressed == curses.KEY_RIGHT:
        navigator.right()
    elif last_key_pressed == curses.KEY_LEFT:
        navigator.left()
    elif last_key_pressed == curses.KEY_ENTER:
        navigator.run()
    elif last_key_pressed == CTRL_B:
        navigator.set_current_state(Explorer)
    elif last_key_pressed == CTRL_E:
        navigator.set_current_state(Editor)
    elif last_key_pressed == CTRL_T:
        navigator.set_current_state(Menu)