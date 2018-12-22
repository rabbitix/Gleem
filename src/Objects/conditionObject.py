from Objects.varObject import VariableObject
from Objects.builtinObject import BuiltInFunctionObject
from Objects.loopObject import LoopObject
from Objects.commentObject import CommentObject


class ConditionObject():

    def __init__(self, ast, nesting_count):
        # The ast will hold the dictionary version of the ast which is a copy somehow
        self.ast = ast['ConditionalStatement']
        # This will hold the exec string for variable decleration
        self.exec_string = ""
        # This is to handle the nesting indentation ===>تودرتو!
        self.nesting_count = nesting_count

    def translate(self):
        # This method will use the AST in order to create a python version of the gleem
        # Loop through each ast value list items
        for value in self.ast:

            # Get the first comparison value
            try:
                self.exec_string += "if " + str(value['value1']) + " "
            except Exception:
                pass

            # Get the comparison type
            try:
                self.exec_string += value['comparison_type'] + " "
            except Exception:
                pass

            # Get the second comparison valie
            try:
                self.exec_string += str(value['value2']) + ": \n"
            except Exception:
                pass

            # Get the body of the conditional statement
            try:
                self.exec_string += self.translate_body(value['body'], self.nesting_count)
            except Exception:
                pass

        return self.exec_string

    def translate_body(self, body_ast, nesting_count):

        # This method will use the body AST to create a python version of gleem
        # it'll create code for the body statement while managing indentations in nesting statments
        # Holds the body executable string of the first statement
        body_exec_string = ""

        # Loop through each ast item in the body dictionary
        for ast in body_ast:

            # This will parse variable declerations within the body
            if self.check_ast('VariableDecleration', ast):
                var_obj = VariableObject(ast)
                transpile = var_obj.translate()
                if self.should_dedent_trailing(ast, self.ast):
                    body_exec_string += ("   " * (nesting_count - 1)) + transpile + "\n"
                else:
                    body_exec_string += ("   " * nesting_count) + transpile + "\n"

            # This will parse built-in within the body
            if self.check_ast('PrebuiltFunction', ast):
                gen_builtin = BuiltInFunctionObject(ast)
                transpile = gen_builtin.translate()
                if self.should_dedent_trailing(ast, self.ast):
                    body_exec_string += ("   " * (nesting_count - 1)) + transpile + "\n"
                else:
                    body_exec_string += ("   " * nesting_count) + transpile + "\n"

            # This will parse comments within the body
            if self.check_ast('Comment', ast):
                gen_comment = CommentObject(ast)
                transpile = gen_comment.translate()
                if self.should_dedent_trailing(ast, self.ast):
                    body_exec_string += ("   " * (nesting_count - 1)) + transpile + "\n"
                else:
                    body_exec_string += ("   " * nesting_count) + transpile + "\n"

            # This will parse nested conditional statement within the body
            if self.check_ast('ConditionalStatement', ast):
                # Increase nesting count because this is a condition statement inside a conditional statement
                # Only increase nest count if needed
                if self.should_increment_nest_count(ast, self.ast):
                    nesting_count += 1
                # Create conditional statement exec string
                condition_obj = ConditionObject(ast, nesting_count)
                # The second nested statament only needs 1 indent not 2
                if nesting_count is 2:
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += "   " + condition_obj.translate()
                else:
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += ("   " * (nesting_count - 1)) + condition_obj.translate()

            # This will parse nested conditional statement within the body
            if self.check_ast('ForLoop', ast):
                # Increase nesting count because this is a condition statement inside a conditional statement
                # Only increase nest count if needed
                if self.should_increment_nest_count(ast, self.ast):
                    nesting_count += 1
                # Create conditional statement exec string
                loop_obj = LoopObject(ast, nesting_count)
                body_exec_string += ("   " * (nesting_count - 1)) + loop_obj.translate()

        return body_exec_string

    def check_ast(self, astName, ast):

        # This method will check if the AST dictionary item being looped through has the
        # same key name as the `astName` argument

        try:
            if ast[astName] is []:
                return True
            if ast[astName]:
                return True
        except Exception:
            return False

    def should_dedent_trailing(self, ast, full_ast):

        # This method will check if the ast item being checked is outside a conditional statement for example
        #
        # if a == 11 {
        #     if name == "Alex" {
        #         print "Not it";
        #     }
        #     print "Hi"; <--- This is the code that should be dedented by 1
        #     so when found will return true if dedent flag is true
        # }
        #
        #
        # it will return
        #     True  : If the code should not be indented because it is in current scope below current nested condition
        #     False : The item should not be dedented

        # This creates an array of only body elements
        new_ast = full_ast[3]['body']
        # This will know whether it should dedent
        dedent_flag = False

        # Loop through body ast's and when a conditonal statement is founds set
        # the dedent flag to 'true'
        for x in new_ast:

            # When a conditional stateemenet AST is found set the dedent trailing to true
            if self.check_ast('ConditionalStatement', x):
                dedent_flag = True

            if ast is x and dedent_flag is True:
                return True

        return False

    def should_increment_nest_count(self, ast, full_ast):

        # This method will check if the ast item being checked is outside a conditional statement for example

        # if a == 11 {
        #     if name == "alex" {
        #         print "Not it";
        #     }
        #     if 1 != 2 { <--- This is the statement that should not be nested more
        #         print "Yo"
        #     }
        # }
        #     will return :
        #     True  : If the nesting should increase by 1
        #     False : If the nesting should not be increased

        # Counts of the number of statements in that one scope
        statement_counts = 0

        # Loops through the body to count the number of conditional statements
        for x in full_ast[3]['body']:

            # If a statement is found then increment statement count variable value by 1
            if self.check_ast('ConditionalStatement', x):
                statement_counts += 1
            # If the statement being checked is the one found then break
            if ast is x:
                break

        # Return false if there were less then 1 statements
        if statement_counts > 1:
            return False
        # Return true if there were more than 1 statements
        else:
            return True
