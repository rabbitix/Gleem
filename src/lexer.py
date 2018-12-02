import re
import constants


class Lexer(object):
    def __init__(self):
        pass  # constructor function

    def getMatcher(self, matcher, sourceCode, currentIndex):
        # Check if matcher is in the same source_code item
        if sourceCode[currentIndex].count('"') == 2:

            # this will partition the string and return a tuple like this
            # ('word', 'matcher(")', ';')
            # it will separate words in a tuple
            word = sourceCode[currentIndex].partition('"')[-1].partition('"'[0])

            # This will return the string and any extra characters such as end statement
            if word[2] != '':
                return ['"' + word[0] + '"', '', word[2]]

            # This will return just the string and empty fields that represent `undefined` or `null`
            else:
                return ['"' + word[0] + '"', '', '']

        else:

            # Cut off the parts of the source code behind the matcher
            sourceCode = sourceCode[currentIndex:len(sourceCode)]

            # This will keep track of the string as it is being built up
            word = ""

            # This will keep count of the iterations
            iter_count = 0

            # This will loop through the source code to find each part of the string and matcher
            for item in sourceCode:

                # Increment the iteration count
                iter_count += 1

                # Append the word that found to the string
                word += item + " "

                # If the word has the matcher in it and it is not the first matcher
                if matcher in item and iter_count != 1:
                    # return the whole string, iteration count and extra characters like a statement end
                    return [
                        '"' + word.partition('"')[-1].partition('"'[0])[0] + '"',  # The string
                        word.partition('"')[-1].partition('"'[0])[2],  # The extra character
                        iter_count - 1  # Number of iterations it took to get string
                    ]

                    # Break out the loop as the whole string was found
                    break

    def tokenize(self, sourceCode):
        # this will hold all tokens in it
        tokens = []
        # clean up code by remove all extra lines
        sourceCode = sourceCode.split()
        # current character position that we are in and parsing
        sourceIndex = 0
        # this loop will go through all words
        while sourceIndex < len(sourceCode):
            # This will be the word that is retrieved from source code
            word = sourceCode[sourceIndex]

            # ignore new lines if exist
            if word in "\n":
                pass

            # Identify all of the Data Types
            elif word in constants.DATA_TYPE:
                tokens.append(["DATATYPE", word])

            # Identify all the indentifiers which are all in 'KEYWWORDS' const
            elif word in constants.KEYWORDS:
                tokens.append(["IDENTIFIER", word])

            # Identify all custom identifers like variable names in source code
            elif re.match("[a-z]", word) or re.match("[A-Z]", word) and word is not "AND" and word is not "OR":
                if word[len(word) - 1] != ';':
                    tokens.append(["IDENTIFIER", word])
                else:
                    tokens.append(["IDENTIFIER", word[0:len(word) - 1]])

            elif word == "+=" or word == "-=" or word == "*=" or word == "/=" or word == "%=":
                tokens.append(['INCREMENTAL_OPERATOR', word])

            # Identify all arithmetic operations in source code
            elif word in "*-/+%=":
                tokens.append(["OPERATOR", word])

            # Identify all bianry operators
            elif word == "AND" or word == "OR":
                tokens.append(["BINARY_OPERATOR", word])

            # Identifies seperators mainly used in for loops
            elif word == "?":
                tokens.append(["SEPERATOR", word])

            # Identify all comparison symbols in source code
            elif word in "==" or word in "!=" or word in ">" or word in "<" or word in "<=" or word in ">=":
                tokens.append(["COMPARISON_OPERATOR", word])

            # Identify all scope definers '{ }' in source code
            elif word in "{}":
                tokens.append(["SCOPE_DEFINER", word])

            # Identifies a comment defenition e.g. "// this is a comment \\"
            elif word == "($" or word == "$)":
                tokens.append(["COMMENT_DEFINER", word])

            # Identify all integer (number) values
            elif re.match("[0-9]", word) or re.match("[-]?[0-9]", word):

                # This will check if there is an end statement at the end of an integer and remove it if there is
                if word[len(word) - 1] == ';':
                    tokens.append(["INTEGER", word[:-1]])
                else:
                    tokens.append(["INTEGER", word])

            # Identify any strings which are surrounded in '' or ""
            elif ('"') in word:

                # Call the getMatcher() method to get the full string
                matcherReturn = self.getMatcher(matcher='"', currentIndex=sourceIndex,
                                                sourceCode=sourceCode)

                # If the string was in one source code item then we can just append it e.g '"Hello"'
                if matcherReturn[1] == '':
                    tokens.append(["STRING", matcherReturn[0]])

                # If the string was spread out across multiple source code item e.g '"Hello', 'world"'
                else:

                    # Append the string token
                    tokens.append(["STRING", matcherReturn[0]])

                    # Check for a semicolon at the end of thee string and if there is one then add end statament
                    if ';' in matcherReturn[1]:
                        tokens.append(["STATEMENT_END", ";"])

                    # Skip all the already checked string items so there are no duplicates
                    sourceIndex += matcherReturn[2]

                    # Skip every other check and loop again
                    pass

            # Checks for the end of a statement ';'
            if ";" in word[len(word) - 1]:
                # Add statement end
                tokens.append(["STATEMENT_END", ";"])

            # Increment to the next word in tachyon source code
            sourceIndex += 1

        return tokens
