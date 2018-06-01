class Termineditor:
    def __init__(self,std_scr,context,current_state):
        self.std_scr = std_scr
        height, width = self.std_scr.getmaxyx()
        self.height = height
        self.width = width
        self.context = context
        self.current_state = current_state
        self.context["Manager"].set_navigator(self)
        self.last_came_from = None

    def set_current_state(self,current_state):
        self.last_came_from = self.current_state
        self.current_state = current_state

    def left(self):
        self.current_state.left()

    def right(self):
        self.current_state.right()

    def up(self):
        self.current_state.up()

    def down(self):
        self.current_state.down()

    def run(self):
        self.current_state.run()

    def display_all_states(self):
        for state in self.context.values():
            if state is self.current_state:
                state.update_global_status(True)
            else:
                state.update_global_status(False)
            state.display()
            self.std_scr.refresh()

    def get_current_state(self):
        return self.current_state

    def get_last_came_from(self):
        return self.last_came_from

    def set_last_came_from(self,last_came_from):
        self.last_came_from = last_came_from