#!/usr/local/bin/python3
# -*- coding: utf-8 -*- c

import os
import sys
import lexer
import parser
import objgen


def main():
    content = ""  # This variable will hold the contents of the source code file
    path = os.getcwd()  # Holds path this script was executed from

    # Holds the name of the file the user wants to compile
    try:
        fileName = sys.argv[1]
    except Exception:
        print("[ERROR] Expected 1 Argument Containing File Name to be Run e.g 'gleem file.gl'")
        return

    # Check if the file extension is correct
    if fileName[len(fileName) - 3:len(fileName)] != ".gl":
        print("[ERROR] File extension not recognised please make sure extension is '.gl'")
        return  # quit programme

    # Check to make sure that only one argument is passed
    try:
        print('[ERROR] Expected 1 argument found 2 (' + sys.argv[1] + ", " + sys.argv[2] + ')')
        return  # quit programme
    except Exception:
        pass

    # Open source code file and get it's content and save it to the 'contents' var
    try:
        with open(path + "/" + fileName, "r") as file:
            content = file.read()
    except Exception:
        print('Cannot find "' + fileName + '"')

    # --------------------------------------
    #  LEXER
    # --------------------------------------

    print('|||||||||||||||||||||  LEXER LOG  ||||||||||||||||||||| \n')
    # Create an instance of the lexer class
    lex = lexer.Lexer()

    # Call lexer method to perform lexical analysis on code
    tokens = lex.tokenize(source_code=content)
    print(tokens)
    print('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||| \n')

    # --------------------------------------
    #  PARSER
    # --------------------------------------

    print('|||||||||||||||||||||  PARSER LOG  |||||||||||||||||||| \n')
    # Create an instance of the parser class
    Parser = parser.Parser(token_stream=tokens)

    # Call the parser method and pass in the tokens as arguments
    source_ast = Parser.parse(token_stream=tokens)
    print(source_ast)
    print('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||| \n')

    # --------------------------------------
    # Object Generation
    # --------------------------------------

    print('||||||||||||||||  OBJECT GENERATION LOG  ||||||||||||||| \n')
    # Create an instance of the Object Generator (objgen) class
    object_generator = objgen.ObjectGenerator(source_ast=source_ast)

    # Call the object definer to get python exec() string
    exec_string = object_generator.object_definer(isGettingBody=False)
    print('\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||| \n')

    # Execute the gleem code that has been transpiled to python code to get output
    print('|||||||||||||||||||  TRANSLATED CODE  |||||||||||||||||| \n')
    print(exec_string)
    print('\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||| \n')

    print('|||||||||||||||||||||||  OUTPUT  ||||||||||||||||||||||| \n')
    exec(exec_string)
    print('\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||| \n')


main()
