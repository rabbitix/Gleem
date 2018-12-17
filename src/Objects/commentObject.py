class CommentObject():

    def __init__(self, ast):
        # This will hold the dictionary version of the AST
        self.ast = ast['Comment']
        # This will hold the python exec string being formed
        self.exec_string = ""

    def translate(self):
        # Generate python comment from comment AST
        self.exec_string += "# " + self.ast
        # Return the generated python exec string
        return self.exec_string
