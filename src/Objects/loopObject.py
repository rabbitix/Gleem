import Objects.conditionObject
from Objects.varObject import VariableObject
from Objects.builtinObject import BuiltInFunctionObject
from Objects.commentObject import CommentObject


class LoopObject(object):

    def __init__(self, ast, nesting_count):
        # This will hold the dictionary version of the AST
        self.ast = ast['ForLoop']
        # This will hold the python exec string being formed
        self.exec_string = ""
        # This will keep track of the nested of `for` loops
        self.nesting_count = nesting_count

    def translate(self):

        # Variables that will store the AST value
        init_val_name = ""
        init_val = ""
        comparison = ""
        incrementer = ""
        end_val = ""
        body = []

        # Loop through the ast items and store them in the variables
        for value in self.ast:

            # Get the initialValueName
            try:
                init_val_name = value['initialValueName']
            except Exception:
                pass

            # Get the initialValue
            try:
                init_val = value['initialValue']
            except Exception:
                pass

            # Get the comparsion
            try:
                comparison = value['comparison']
            except Exception:
                pass

            # Get the endValue
            try:
                end_val = value['endValue']
            except Exception:
                pass

            # Get the incrementer
            try:
                incrementer = value['incrementer']
            except Exception:
                pass

            # Get the body
            try:
                body = value['body']
            except Exception:
                pass

        # This will check if incrementer has + at the first index
        # and remove it if it does as it will cause python syntax error
        if incrementer[0] is "+":
            incrementer = incrementer[1:len(incrementer)]

        # Append the python for loop statement to the exect string separate from the body
        self.exec_string += "for " + init_val_name + " in range(" + str(init_val) + ", " + str(
            end_val) + ", " + incrementer + "):\n"

        # Translate body and add return translated code to exec string with correct indentation
        self.exec_string += self.translate_body(body, self.nesting_count)

        return self.exec_string

    def translate_body(self, body_ast, nesting_count):

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
                condition_obj = Objects.conditionObject.ConditionObject(ast, nesting_count)
                body_exec_string += ("   " * (nesting_count - 1)) + condition_obj.translate()

            # This will parse nested conditional statement within the body
            if self.check_ast('ForLoop', ast):
                # Increase nesting count because this is a condition statement inside a conditional statement
                # Only increase nest count if needed
                if self.should_increment_nest_count(ast, self.ast):
                    nesting_count += 1
                # Create conditional statement exec string
                loop_obj = LoopObject(ast, nesting_count)
                # The second nested statament only needs 1 indent not 2
                if nesting_count == 2:
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += "   " + loop_obj.translate()
                else:
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += ("   " * (nesting_count - 1)) + loop_obj.translate()

        return body_exec_string

    def check_ast(self, astName, ast):
        # check for that ast be not empty
        try:
            if ast[astName] is []:
                return True
            if ast[astName]:
                return True
        except Exception:
            return False

    def should_dedent_trailing(self, ast, full_ast):

        # This method will check if the ast item being checked is outside a conditional statement e.g.

        # if a == 11 {
        #     if name == "Alex" {
        #         print "Not it";
        #     }
        #     print "Hi"; <--- This is the code that should be indented by 1
        #     so when found will return true if dedent flag is true
        # }
        # will return  ==> True  : If the code should not be indented
        # because it is in current scope below current nested condition
        #             ==> False : The item should not be indented

        # This  will creates an array of only body elements
        new_just_body_ast = full_ast[len(full_ast) - 1]['body']
        # This will know whether it should dedent
        dedent_flag = False

        # Loop through body's ast and when a conditional statement is founds set
        # the dedent flag to 'true'
        for x in new_just_body_ast:

            # When a conditional stateemenet AST is found set the dedent trailing to true
            if self.check_ast('ForLoop', x):
                dedent_flag = True

            if ast == x and dedent_flag is True:
                return True

        return False

    def should_increment_nest_count(self, ast, full_ast):

        # This method will check if another statement is found and whether or not it should increase
        # nesting count for example
        # if a == 11 {
        #     if name == "Alex" {
        #         print "Not it";
        #     }
        #     if 1 != 2 { <--- This is the statement that should not be nested more
        #         print "Yo man! "
        #     }
        # }
        # will return:
        #     True  : If the nesting should increase by 1
        #     False : If the nesting should not be increased

        # Counts of the number of statements in that one scope
        statement_counts = 0

        # Loops through the body to count the number of conditional statements
        for x in full_ast[len(full_ast) - 1]['body']:

            # If a statement is found then increment statement count variable value by 1
            if self.check_ast('ForLoop', x):
                statement_counts += 1

            # If the statement being checked is the one found then break
            if ast == x:
                break

        # Return false if there were less then 1 statements
        if statement_counts > 1:
            return False
        # Return true if there were more than 1 statements
        else:
            return True
