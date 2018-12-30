import constant


class Comp():
    def __init__(self):
        # self.exe_string = ""
        self.values = ""

    def translate(self, token_type=None, operation=None, value=None):
        self.values += value + ' '
        return self.values
