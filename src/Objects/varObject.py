class VariableObject(object):

    def __init__(self):
        self.exec_string = ""

    def transpile(self, name, operator, value):
        self.exec_string += name + " " + operator + " " + value+"\n"
        return self.exec_string
