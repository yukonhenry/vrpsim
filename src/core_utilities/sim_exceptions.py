# Copyright YukonTR 2015'
__author__ = 'henry'

class CodeLogicError(Exception):
    ''' Generic Exception if there is a logic error in code '''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class ConfigurationError(Exception):
    ''' Generic Exception if there is a logic error in code '''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg
    def __str__(self):
        return repr(self.msg)