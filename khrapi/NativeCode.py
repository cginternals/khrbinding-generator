
class NativeCode(object):
    def __init__(self, identifier, code):
        self.identifier = identifier
        self.code = code
        self.hideDeclaration = False
        self.declaration = code
