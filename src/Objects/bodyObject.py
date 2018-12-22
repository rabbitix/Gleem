from Objects.varObject import VariableObject
from Objects.builtinObject import BuiltInFunctionObject
import Objects.loopObject
import Objects.conditionObject


class BodyObject(object):

    def __init__(self, ast, astName, nesting_count=None):
        # The Name of the ast name using these methods
        self.astName = astName
        self.ast = ast
        self.nesting_count = nesting_count

    def translate_body(self, body_ast, nesting_count):

        # This method will use the body AST to create a python version of the gleem
        # code for the body statement while managing indentations

        # Holds the body executable string of the first statement
        body_exec_string = ""

        # Loop through each ast item in the body dictionary
        for ast in body_ast:

            # This will parse variable declerations within the body
            if self.check_ast('VariableDecleration', ast):
                var_obj = VariableObject(ast)
                translate = var_obj.translate()
                if self.should_dedent_trailing(ast, self.ast):
                    body_exec_string += ("   " * (nesting_count - 1)) + translate + "\n"
                else:
                    body_exec_string += ("   " * nesting_count) + translate + "\n"

            # This will parse built-in within the body
            if self.check_ast('PrebuiltFunction', ast):
                gen_builtin = BuiltInFunctionObject(ast)
                translate = gen_builtin.translate()
                if self.should_dedent_trailing(ast, self.ast):
                    body_exec_string += ("   " * (nesting_count - 1)) + translate + "\n"
                else:
                    body_exec_string += ("   " * nesting_count) + translate + "\n"

            # This will parse nested conditional statement within the body
            if self.check_ast('ConditionalStatement', ast):
                # Increase nesting count because this is a condition statement inside a conditional statement
                # Only increase nest count if needed
                if self.should_increment_nest_count(ast, self.ast):
                    nesting_count += 1
                # Create conditional statement exec string
                condition_obj = Objects.conditionObject.ConditionObject(ast, nesting_count)
                # The second nested statament only needs 1 indent not 2
                if nesting_count == 2:
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
                loop_obj = Objects.loopObject.LoopObject(ast, nesting_count)
                # The second nested statament only needs 1 indent not 2
                if nesting_count == 2:
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += "   " + loop_obj.translate()
                else:
                    # Add the content of conditional statement with correct indentation
                    body_exec_string += ("   " * (nesting_count - 1)) + loop_obj.translate()

        return body_exec_string

    def check_ast(self, astName, ast):

        try:

            if ast[astName] is []:
                return True
            if ast[astName]:
                return True
        except Exception:
            return False

    def should_dedent_trailing(self, ast, full_ast):

        print('///// - ', ast)
        # This creates an array of only body elements
        new_ast = full_ast[len(full_ast) - 1]['body']
        # This will know whether it should dedent
        dedent_flag = False

        # Loop through body ast's and when a conditonal statement is founds set
        # the dedent flag to 'true'
        for x in new_ast:
            print('-/-/- ', ast, ' ===== ', x)
            if self.check_ast(self.astName, x):
                dedent_flag = True

            if ast == x and dedent_flag is True:
                return True

        return False

    def should_increment_nest_count(self, ast, full_ast):

        # Counts of the number of statements in that one scope
        statement_counts = 0

        # Loops through the body to count the number of conditional statements
        for x in full_ast[len(full_ast) - 1]['body']:

            # If a statement is found then increment statement count variable value by 1
            if self.check_ast(self.astName, x): statement_counts += 1
            # If the statement being checked is the one found then break
            if ast == x: break

        # Return false if there were less then 1 statements
        if statement_counts > 1:
            return False
        # Return true if there were more than 1 statements
        else:
            return True
