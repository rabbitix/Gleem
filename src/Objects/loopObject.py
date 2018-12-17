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
                body_exec_string += ("   " * (nesting_count - 1)) + condition_obj.transpile()

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
