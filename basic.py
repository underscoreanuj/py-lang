##################################################
#                   CONSTANTS                    #
##################################################

DIGITS = '0123456789'


##################################################
#                   ERRORS                       #
##################################################

class Error:
    def __init__(self, pos_start, pos_end, error_name, error_details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.error_details = error_details

    def __str__(self):
        return '{}: {}, File: {}, at line {}'.format(self.error_name, self.error_details, self.pos_start.fn, self.pos_start.ln+1)


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, error_details):
        super().__init__(pos_start, pos_end, 'Illegal Character', error_details)

class IllegalNumberError(Error):
    def __init__(self, pos_start, pos_end, error_details):
        super().__init__(pos_start, pos_end, 'Illegal Number', error_details)


##################################################
#                   TOKENS                       #
##################################################

# data types
TT_INT          = "INT"
TT_FLOAT        = "FLOAT"
# operators
TT_PLUS         = "PLUS"
TT_MINUS        = "MINUS"
TT_MUL          = "MUL"
TT_DIV          = "DIV"
#parens
TT_LPAREN       = "LPAREN"
TT_RPAREN       = "RPAREN"


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if(self.value):
            return '{} : {}'.format(self.type, self.value)
        return '{}'.format(self.type)



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


##################################################
#                   RUN                          #
##################################################

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()

    return tokens, error