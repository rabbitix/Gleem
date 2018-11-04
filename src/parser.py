class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0

    def parse(self):
        while self.token_index < len(self.tokens):
            token_type = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]

            # print(token_type+"=>", token_value)
            if token_type == "VAR_DECELERATION" and token_value == "var":
                self.parse_variable_decelearition(self.tokens[self.token_index:len(self.tokens)])

            self.token_index += 1

    def parse_variable_decelearition(self, token_stream):
        # print(token_stream)
        # pass
        tokens_checkd = 0
        for token in range(0, len(token_stream)):
            token_type = token_stream[tokens_checkd][0]
            token_value = token_stream[tokens_checkd][1]

            if token == 0:
                print('variable type: ' + token_value)

            elif token == 1 and token_type == "IDENTIFIER":
                print('variable name: ' + token_value)
            elif token == 1 and token_type != 'IDENTIFIER':
                print("Erorr : Invalid variable name '" + token_value + "'")
                quit()

            elif token == 2 and token_type == "OPERATOR":
                print("Assigment Operator: " + token_value)
            elif token == 2 and token_type == "OPERATOR":
                print("Erorr: Assignment Operator is missing or invalid .it shuld be '='")
                quit()

            elif token == 3 and token_type in ['STRING', "INTEGER", "IDENTIFIER"]:
                print("Variable value :" + token_value)
            elif token == 3 and token_type not in ['STRING', "INTEGER", "IDENTIFIER"]:
                print("Invalid variable assignment value '" + token_value + "'")
                quit()
            tokens_checkd += 1
