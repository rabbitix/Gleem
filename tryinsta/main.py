import lexer
import parser
import objgen
import os
import sys


def main():
    # content = ""  # the source code
    #
    # path = os.getcwd()
    #
    # # Holds the name of the file the user wants to compile
    # try:
    #     fileName = sys.argv[1]
    # except:
    #     print("[ERROR] Expected 1 Argument Containing File Name to be Run e.g 'gleem file.gl'")
    #     return
    #
    # # Check if the file extension is correct
    # if fileName[len(fileName) - 3:len(fileName)] != ".gl":
    #     print("[ERROR] File extension not recognised please make sure extension is '.gl'")
    #     return  # quit programme
    #
    # # Check to make sure that only one argument is passed
    # try:
    #     print('[ERROR] Expected 1 argument found 2 (' + sys.argv[1] + ", " + sys.argv[2] + ')')
    #     return  # quit programme
    # except:
    #     pass
    #
    # # Open source code file and get it's content and save it to the 'contents' var
    # try:
    #     with open(path + "/" + fileName, "r") as file:
    #         content = file.read()
    # except:
    #     print('Cannot find "' + fileName + '"')

    content = ""
    with open('syntax.gl', 'r') as source_code:
        content = source_code.read()

    lex = lexer.Lexer()
    tokens = lex.tokenize(source_code=content)

    print("\n\033[34m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m")
    print(  "\033[34m~~~~~~~~~~~~~~~~~~~/ LEXER LOG /~~~~~~~~~~~~~~~~~~~\033[0m")
    print(  "\033[34m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m\n")
    for token in tokens:  # to print tokens in new lines
        print('\033[36m', token)

    print("\n\033[34m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m")
    print("  \033[34m~~~~~~~~~~~~~~~~~~~/ PARSER LOG /~~~~~~~~~~~~~~~~~~\033[0m")
    print("  \033[34m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m\n")

    pars = parser.Parser(tokens=tokens)
    parsed = pars.parse()

    print("\n\033[34m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m")
    print("  \033[34m~~~~~~~~~~~~~~~~~~~~/ OBJ PART /~~~~~~~~~~~~~~~~~~~\033[0m")
    print("  \033[34m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m\n")

    objectgen = objgen.Comp()
    objectgen.compile(parsed)


if __name__ == '__main__':
    main()
