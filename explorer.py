class Explorer:
    def __init__(self,std_scr):
        self.std_scr = std_scr
        self.is_global_state = False

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

    def display(self):
        pass

    def update_global_status(self,status):
        self.is_global_state = status