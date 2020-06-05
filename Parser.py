from Constants import *
from Nodes import *

##################################################
#                   PARSER                       #
##################################################


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def binary_operation(self, func, ops):
        left = func()

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = func()

            left = BinOpNode(left, op_tok, right)
        
        return left

    def factor(self):
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)

    def term(self):
        return self.binary_operation(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.binary_operation(self.term, (TT_PLUS, TT_MINUS))

    def parse(self):
        res = self.expr()
        return res
