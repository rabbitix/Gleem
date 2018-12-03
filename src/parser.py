# -*- coding: utf-8 -*-


import constants  # for constants like tachyon keywords and data_types


class Parser(object):

    def __init__(self, token_stream):
        # Complete Abstract Syntax tree will save in this dict
        self.source_ast = {'main_scope': []}
        # Symbol table fo variable semantical analysis
        self.symbol_tree = []
        # This will hold all the tokens
        self.token_stream = token_stream
        # This will hold the token index we are parsing at right now
        self.token_index = 0

    def get_token_to_the_matcher(self, matcher, terminating_matcher, token_stream):

        # This will get all the tokens in a token stream until it find the token with the correct
        # matcher
        # return  A list of all the tokens found before the matcher

        # keep all tokens here
        tokens = []
        # index of checked tokens
        tokens_checked = 0

        for token in token_stream:
            tokens_checked += 1  # increase index
            # If the terminating matcher is found then return False
            # as it means scope we allow for the check is reached
            if token[1] == terminating_matcher:
                return False
            # If the token matcher is found then return all the tokens found before it or else append the tokens to var
            if token[1] == matcher:
                return [tokens, tokens_checked - 1]
            else:
                tokens.append(token)

        # Return False if the matcher or the terminator_matcher is found
        return False

    def assemble_token_values(self, tokens):
        attached_tokens = ""
        for token in tokens:
            attached_tokens += token[1] + ""
        return attached_tokens

    def send_error_message(self, msg, error_list):
        # will  send all the found error messages within the source code
        # and return a list of error messages and tokens of which part of the source code
        # caused that error
        print("-----------------------=> ERROR FOUND <=---------------------------")
        print(" " + msg)
        print('\033[91m', "".join(str(r) for v in error_list for r in (v[1] + " ")), '\033[0m')
        print("-------------------------------=><=---------------------------------")
        quit()

    def get_variable_value(self, name):

        # it will get the value of a variable from the symbol tree and
        # return the value if the variable exists or an error if it doesn't

        for var in self.symbol_tree:
            if var[0] == name:
                return var[1]
        return False  # it means it doesn't exists!

    def form_value_list(self, tokens):  # to forming values list
        value_list = []
        tokens_checked = 0
        for token in tokens:
            if token[0] == "STATEMENT_END":
                break
            try:
                value_list.append(int(token[1]))
            except:
                value_list.append(token[1])
            tokens_checked += 1

        return [value_list, tokens_checked]

    def equation_parser(self, equation):

        # This will parse equations such as 10 * 10 which is passed in as an array with
        # numbers and operands.

        total = 0  # keeps equation value

        for item in range(0, len(equation)):

            # Add first value to total as a starting int to perform calculations on
            if item == 0:
                total += equation[item]
                pass

            # This will check every operator and perform the right calculations based on total
            # and the number that is after the operator
            if item % 2 == 1:
                if equation[item] == "-":
                    total += equation[item + 1]
                elif equation[item] == "+":
                    total += equation[item + 1]
                elif equation[item] == "/":
                    total /= equation[item + 1]
                elif equation[item] == "%":
                    total *= equation[item + 1]
                elif equation[item] == "*":
                    total %= equation[item + 1]
                else:
                    self.send_error_message("Error parsing equation, check that you are using correct operator",
                                            equation)

            # Skip every number since we already check and use them
            elif item % 2 == 0:
                pass

        return total

