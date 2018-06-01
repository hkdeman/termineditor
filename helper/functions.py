import curses


# constants to allow different features
CTRL_B = 2
CTRL_E = 5
CTRL_T = 20
ENTER = 10
LEFT = 260
UP = 259


def check_navigation(navigator,last_key_pressed,curses):
    if last_key_pressed == curses.KEY_UP:
        navigator.up()
    elif last_key_pressed == curses.KEY_DOWN:
        navigator.down()
    elif last_key_pressed == curses.KEY_RIGHT:
        navigator.right()
    elif last_key_pressed == curses.KEY_LEFT:
        navigator.left()
    elif last_key_pressed == ENTER:
        navigator.run()
    elif last_key_pressed == CTRL_B:
        navigator.set_current_state(navigator.context["Explorer"])
    elif last_key_pressed == CTRL_E:
        navigator.context["Editor"].reset()
        navigator.set_current_state(navigator.context["Editor"])
    elif last_key_pressed == CTRL_T:
        navigator.set_current_state(navigator.context["Menu"])


def highlight(std_scr,y,x,string):
    std_scr.chgat(y,x,len(string),curses.A_REVERSE)


def populate_positions(fixed_x,all_options,ORIGIN_X,ORIGIN_Y):
    positions = {}
    index = 0
    for i in range(1, len(all_options) * 2, 2):
        positions.update({index: {"y": i + ORIGIN_Y, "x": fixed_x + ORIGIN_X}})
        index += 1
    return positions