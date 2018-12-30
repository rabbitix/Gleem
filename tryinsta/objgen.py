import constant


class Comp():
    def __init__(self):
        self.exe_string = ""


    def translate(self, token_type=None, operation=None, value=None):
        if token_type is "KEYWORD":
            if value:
                self.exe_string+="user:{0}".format(value)



        return self.exe_string
