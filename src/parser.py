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

