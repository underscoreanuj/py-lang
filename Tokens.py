##################################################
#                   TOKENS                       #
##################################################


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if(self.value):
            return '{} : {}'.format(self.type, self.value)
        return '{}'.format(self.type)