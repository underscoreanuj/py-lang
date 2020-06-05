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