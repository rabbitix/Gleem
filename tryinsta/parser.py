import objgen
from constant import *
from objgen import Comp as c

cc = c()


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.log_file = ""
        self.all_tokens = ""

    def parse(self):
        com = objgen.Comp()
        if self.tokens[0][1] in KEYWORDS["StartIdentifier"]:
            com.main_log = self.tokens[1][1]
        else:
            cc.show_error("Syntax Error")
            quit()
        while self.token_index < len(self.tokens):
            # todo dont pass two identifier after each other
            token_type = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]
            # Handel syntax error
            # TODO add specific errors
            if self.token_index % 2 is 0:
                if self.tokens[self.token_index][0] is "IDENTIFIER":
                    cc.show_error("Syntax Error")

                    quit()
            if self.token_index % 2 is 0:
                if token_value not in data_type and token_value not in key_words:
                    cc.show_error("syntax error")
                    quit()

            print('\033[35m----------------------------[ ' + token_type, token_value + ' ]----------------------------')

            self.all_tokens = com.translate(value=token_value)
            self.token_index += 1

        return self.all_tokens
