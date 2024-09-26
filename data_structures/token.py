class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position
        self.free = True

    def __repr__(self):
        return (f'Token(type={self.type}, ' + 
                f'value={self.value}, ' + 
                f'position={self.position}, ' +
                f'free={self.free})')
