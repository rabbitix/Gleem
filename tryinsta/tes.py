import lexer
import constant

txt =""
with open('syntax.gl', 'r') as source_code:
    txt=source_code.read()

lex = lexer.Lexer()
print(lex.tokenize(source_code=txt))
