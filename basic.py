from Lexer import Lexer
from Parser import Parser

##################################################
#                   RUN                          #
##################################################

def run(fn, text):
    # generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    if error:
        return tokens, error

    # generate abstract syntax tree (AST)
    parser = Parser(tokens)
    ast = parser.parse()

    return ast, None