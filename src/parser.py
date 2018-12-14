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

    def concatenation_parser(self, concatenation_list):
        # This will parse concatenation of strings and variables with string values or integer
        # values to concatenate arithmetics to strings together

        full_string = ""

        for item in range(0, len(concatenation_list)):

            current_value = concatenation_list[item]

            # Add the first item to the string
            if item == 0:
                # This checks if the value being checked is a string or a variable
                # If it is a string then just add it without the surrounding quotes
                if current_value[0] == '"':
                    full_string += current_value[1:len(current_value) - 1]
                # If it isn't a string then get the variable value and append it
                else:
                    var_value = self.get_variable_value(current_value)
                    if var_value is not False:
                        full_string += var_value[1:len(var_value) - 1]
                    else:
                        self.send_error_message(
                            'Cannot find variable "%s" because it was never created' % concatenation_list[item + 1],
                            concatenation_list)
                pass

            # This will check for the concatenation operator
            if item % 2 == 1:

                if current_value == "+":
                    # This checks if the value being checked is a string or a variable
                    if concatenation_list[item + 1][0] != '"':

                        # This will get the variable value and check if it exists if
                        # so then it adds it to the full string
                        var_value = self.get_variable_value(concatenation_list[item + 1])
                        if var_value is not False:
                            full_string += var_value[1:len(var_value) - 1]
                        else:
                            self.send_error_message(
                                'Cannot find variable "%s" because it was never created' % concatenation_list[item + 1],
                                concatenation_list)

                    else:
                        full_string += concatenation_list[item + 1][1:len(concatenation_list[item + 1]) - 1]

                elif current_value == ",":
                    full_string += " " + concatenation_list[item + 1]

                else:
                    self.send_error_message("Error parsing equation, check that you are using correct operand",
                                            concatenation_list)

            # This will skip value as it is already being added and dealt with when getting the operand
            if item % 2 == 0:
                pass

        return '"' + full_string + '"'

    def parsing_variables_decleration(self, token_stream, is_in_body):
        # this method will parse variable declerations and add them to the source AST or
        # return them if variable decleration is being parsed for body of a statement

        ast = {'VarDecleration': []}  # The abstract syntax tree for var decl
        tokens_checked = 0  # Number of token checked that made up the var decl
        var_exists = True

        for x in range(0, len(token_stream)):

            # Create variables for identify token type and value
            token_type = token_stream[x][0]
            token_value = token_stream[x][1]

            # Skip '=' operator in var decl
            if x is 2 and token_type is "OPERATOR" and token_value is "=":
                pass
            # This will handle error detection for making sure  '=' sign is found
            if x is 2 and token_type is not "OPERATOR" and token_value is not "=":
                self.send_error_message("Variable Decleration Missing '='.",
                                        self.token_stream[self.token_index:self.token_index + tokens_checked + 2])

            # If a `statement end` is found then break the parsing
            if token_stream[x][0] is "STATEMENT_END":
                break

            # it will parse the first token which will be the var type
            if x is 0:
                ast['VarDecleration'].append({"type": token_value})

            # it will parse the second token which will be the name of the var
            if x is 1 and token_type is "IDENTIFIER":

                # Check if a variable has already been named the same and is so send an error
                if self.get_variable_value(token_value) is not False:
                    self.send_error_message(
                        "Variable '%s' is already exists and cannot be defined again!" % token_value,
                        self.token_stream[self.token_index:self.token_index + tokens_checked + 1])
                else:
                    # Set var exists to False so that it can be added
                    var_exists = False

                    # This will check if the variable is being delared but not initialised
                    if token_stream[x + 1][0] is "STATEMENT_END":
                        # Adds the default value of 'undefined' and breaks out of loop
                        ast['VarDecleration'].append({"name": token_value})
                        ast['VarDecleration'].append({"value": '"undefined"'})
                        tokens_checked += 1
                        break
                    else:
                        ast['VarDecleration'].append({"name": token_value})

            # Error handling for variable name to make sure the naming convention is true and acceptable
            if x is 1 and token_type is not "IDENTIFIER":
                self.send_error_message("Invalid Variable Name '%s'" % token_value,
                                        self.token_stream[self.token_index:self.token_index + tokens_checked + 1])

            # This will parse the 3rd token which is the value of the variable
            if x is 3 and token_stream[x + 1][0] is "STATEMENT_END":

                # Check if the value matches the variable defined type
                if type(eval(token_value)) is eval(token_stream[0][1]):
                    # Add value as a number not a string if it is an int or else add it as a string
                    try:
                        ast['VarDecleration'].append({"value": int(token_value)})
                    except ValueError:
                        ast['VarDecleration'].append({"value": token_value})
                else:
                    self.send_error_message("Variable value does not match defined type!",
                                            self.token_stream[self.token_index:self.token_index + tokens_checked + 1])

            # This will parse any variable declerations which have concatenation or arithmetics
            elif x >= 3:

                # This will call the form_value_list method and
                # it will return the concatenation value and tokens checked
                value_list_func_call = self.form_value_list(token_stream[tokens_checked:len(token_stream)])
                value_list = value_list_func_call[0]
                tokens_checked += value_list_func_call[1]

                # Call the equation parser and append value returned
                # or try concat parser if an error occurs
                try:
                    ast['VarDecleration'].append({"value": self.equation_parser(value_list)})
                except:
                    try:
                        ast['VarDecleration'].append({"value": self.concatenation_parser(value_list)})
                    except:
                        self.send_error_message("Invalid variable decleration!",
                                                self.token_stream[self.token_index:self.token_index + tokens_checked])
                break  # Break out of the current var parsing loop since we just parsed everything

            tokens_checked += 1  # Indent within overall for loop

        #  error validation checking if all needed var decl elements are in the ast such as:
        # var type, name and value
        try:
            ast['VarDecleration'][0]
        except:
            self.send_error_message("Invalid variable decleration could not set variable type!",
                                    self.token_stream[self.token_index:self.token_index + tokens_checked])
        try:
            ast['VarDecleration'][1]
        except:
            self.send_error_message("Invalid variable decleration could not set variable name!",
                                    self.token_stream[self.token_index:self.token_index + tokens_checked])
        try:
            ast['VarDecleration'][2]
        except:
            self.send_error_message("Invalid variable decleration could not set variable value!",
                                    self.token_stream[self.token_index:self.token_index + tokens_checked])

        # if this is being run to parse inside a body then there is no need to add it to the source ast
        # as it will be added to the body of statement being parsed
        if not is_in_body:
            self.source_ast['main_scope'].append(ast)

        if not var_exists:
            self.symbol_tree.append([ast['VarDecleration'][1]['name'], ast['VarDecleration'][2]['value']])

        self.token_index += tokens_checked

        return [ast, tokens_checked]  # return is only used within body parsing to create body ast

    def get_statement_body(self, token_stream):
        # This will get the tokens that make up the body of a statement (in a condition or a loop)
        # and return the tokens
        # it will returns tokens that make up the body for statements

        count_of_nesting = 1
        tokens_checked = 0
        body_tokens = []

        for token in token_stream:

            tokens_checked += 1

            # separate tokens types and values to make it more readable
            token_value = token[1]
            token_type = token[0]

            # keeps track of the opening and closing scope definers '}' and '{' (for statements)
            if token_type is "SCOPE_DEFINER" and token_value is "{":
                count_of_nesting += 1
            elif token_type is "SCOPE_DEFINER" and token_value is "}":
                count_of_nesting -= 1

            # checks whether the closing scope definer is found to finish creating body tokens
            if count_of_nesting is 0:  # have some doubt
                body_tokens.append(token)
                break
            else:
                body_tokens.append(token)

        # print('{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}', body_tokens)

        return [body_tokens, tokens_checked]

    def parsing_conditional_statements(self, token_stream, is_nested):
        # this will parse conditional statements like 'if else' and create an
        # abstract syntax tree for it and will return that as a AST tree dict
        # is_nested parameter means that there is a condition inside another condition

        tokens_checked = 0
        ast = {'ConditionalStatement': []}

        # this loop will parse the condition and walk through it!
        for x in range(0, len(token_stream)):

            allowed_conditional_token_types = ['INTEGER', 'STRING', 'IDENTIFIER']
            tokens_checked += 1
            token_type = token_stream[x][0]
            token_value = token_stream[x][1]
            # break out of the loop at the end of the condition statement
            if token_type is 'SCOPE_DEFINER' and token_value is '{':
                break
            # Pass if token is the 'if' identifier as it has already been checked
            # cuz we dont want to parse `if` itself
            if token_type is 'IDENTIFIER' and token_value is 'if':
                pass
            # This will check for the first value and add it to the AST
            if x is 1 and token_type in allowed_conditional_token_types:
                # This will check for an identifier (var[variable])
                # and then check if it exists so it can add the value to it
                if self.get_variable_value(token_value) is not False:
                    ast['ConditionalStatement'].append({'value1': self.get_variable_value(token_value)})
                else:
                    ast['ConditionalStatement'].append({'value1': token_value})

            # This will check for the comparison operator and add it to the AST
            if x is 2 and token_type is 'COMPARISON_OPERATOR':
                ast['ConditionalStatement'].append({'comparison_type': token_value})

            # This will check for the second value and add it to the AST
            if x is 3 and token_type in allowed_conditional_token_types:
                # This will check for an identifier (var) and then check if it exists so it can add the value to it
                if self.get_variable_value(token_value) is not False:
                    ast['ConditionalStatement'].append({'value2': self.get_variable_value(token_value)})
                else:
                    ast['ConditionalStatement'].append({'value2': token_value})

        # Increment token index for tokens checked in condition that we parse
        self.token_index += tokens_checked - 1

        # This will get the body tokens and the tokens checked
        # that make up the body to skip them
        get_body_return = self.get_statement_body(token_stream[tokens_checked:len(token_stream)])
        print()
        print()
        print('---=>', get_body_return)  # this part is tmp for see results
        print()
        print()
        # If it nested then call parse_body with nested parameter of true else false
        if is_nested is True:
            self.parse_body(get_body_return[0], ast, 'ConditionalStatement', True)
        else:
            self.parse_body(get_body_return[0], ast, 'ConditionalStatement', False)
        # Add the amount tokens we checked in body
        tokens_checked += get_body_return[1]
        return [ast, tokens_checked]  # Return is only used within body parsing to create body AST

    def parse_body(self, token_stream, statement_ast, astName, isNested):
        # This will parse the body of conditional, iteration, functions and etc
        # to return a body ast like this --> {'body': []}

        tokens_checked = 0
        nesting_count = 0
        ast = {'body': []}
        while tokens_checked < len(token_stream):  # iter trough all token string

            # This will parse variable declerations within the body
            if token_stream[tokens_checked][0] is "DATATYPE":
                var_decleration_parse = self.parsing_variables_decleration(
                    token_stream[tokens_checked:len(token_stream)],
                    True)
                ast['body'].append(var_decleration_parse[0])
                tokens_checked += var_decleration_parse[1]

            # This will parse nested conditional statements within the body
            elif token_stream[tokens_checked][0] is 'IDENTIFIER' and token_stream[tokens_checked][1] is 'if':
                condition_parsing = self.parsing_conditional_statements(token_stream[tokens_checked:len(token_stream)],
                                                                        True)
                ast['body'].append(condition_parsing[0])
                tokens_checked += condition_parsing[1] - 1  # minus one to dont skip extra token

            elif token_stream[tokens_checked][0] is "IDENTIFIER" and token_stream[tokens_checked][1] is "for":
                loop_parse = self.parse_for_loop(token_stream[tokens_checked:len(token_stream)], True)
                ast['body'].append(loop_parse[0])
                tokens_checked += loop_parse[1]

            # This will parse builtin functions in the body
            elif token_stream[tokens_checked][0] == 'IDENTIFIER' and token_stream[tokens_checked][
                1] in constants.BUILT_IN_FUNCTIONS:
                built_in_func_parse = self.parse_built_in_function(token_stream[tokens_checked:len(token_stream)], True)
                ast['body'].append(built_in_func_parse[0])
                tokens_checked += built_in_func_parse[1]

            # This will parse comments in the body
            elif token_stream[tokens_checked][0] == "COMMENT_DEFINER" and token_stream[tokens_checked][1] == "($":
                comment_parsing = self.parse_comment(token_stream[tokens_checked:len(token_stream)], True)
                ast['body'].append(comment_parsing[0])
                tokens_checked += comment_parsing[1]

            # This is needed to increase token index  when a closing scope definer is found because it is skipped
            # so when it is found then add 1 or else this will lead to a logical bug in nesting
            if token_stream[tokens_checked][1] == '}':
                nesting_count += 1

            tokens_checked += 1

        # Increase token index by amount of closing scope definers found which is usually skipped and add 1 for the last
        #  one which is not passed in to this method
        self.token_index += nesting_count + 1
        # Form the full AST with the statement and body combined and then add it to the source AST
        statement_ast[astName].append(ast)
        # If the statments is not nested then add it or else dont
        # because parent will be added containing the child
        if not isNested: self.source_ast['main_scope'].append(statement_ast)
