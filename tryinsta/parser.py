import objgen


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0

    def parse(self):
        com = objgen.Comp()

        while self.token_index < len(self.tokens):
            token_type = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]
            print('------------------------------ ', token_type, token_value, ' ------------------------------')

            com.translate(value=token_value)
            self.token_index += 1
