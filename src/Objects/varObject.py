class VariableObject(object):

    def __init__(self, ast):
        # The ast will hold the dictionary version of the ast which is like a blueprint
        self.ast = ast['VariableDecleration']
        # This will hold the exec string for variable decleration
        self.exec_string = ""

    def translate(self):

        # This method will use the AST in order to create a python version of the gleem
        # generated dictionary AST.

        # Loop through all dictionary values
        for value in self.ast:

            # Get the name of the variable
            try:
                self.exec_string += value['name'] + " = "
            except:
                pass

            # Get the value of the variable
            try:
                self.exec_string += str(value['value'])
            except:
                pass

        return self.exec_string
