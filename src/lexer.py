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

