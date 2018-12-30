import objgen


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.translated_code = ""
        self.all_vals = ""

    def parse(self):
        com = objgen.Comp()

        while self.token_index < len(self.tokens):
            token_type = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]
            self.all_vals += token_value + ' '
            print('------------------------------ ', token_type, token_value, ' ------------------------------')
            print(com.translate(token_type=token_type, value=token_value))
            self.token_index += 1
