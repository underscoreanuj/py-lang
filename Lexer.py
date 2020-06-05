from Tokens import Token
from Errors import IllegalCharError, IllegalNumberError
from Constants import *

##################################################
#                   POSITION                     #
##################################################


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            selc.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


##################################################
#                   LEXER                        #
##################################################


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_number(self):
        num_str = ''
        decimal_count = 0

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if decimal_count == 1:
                    return Token(TT_INT, float(num_str)), 'error'
                decimal_count += 1
            num_str += self.current_char
            self.advance()

        if decimal_count == 0:
            return Token(TT_INT, int(num_str)), None
        else:
            return Token(TT_FLOAT, float(num_str)), None


    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            # numbers
            elif self.current_char in DIGITS:
                pos_start = self.pos.copy()
                num, error = self.make_number()
                if error is not None:
                    return [], IllegalNumberError(pos_start, self.pos, "'" + str(num) + "'")
                tokens.append(num)
            # operators
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            # parens
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None