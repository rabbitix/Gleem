import lexer
import constant
import parser
txt =""
with open('syntax.gl', 'r') as source_code:
    txt=source_code.read()

lex = lexer.Lexer()
pars = parser.Parser(lex.tokenize(source_code=txt)).parse()
