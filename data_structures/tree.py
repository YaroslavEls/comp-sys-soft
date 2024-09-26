class Tree:
    def __init__(self, lleaf, rleaf, operation, level):
        self.lleaf = lleaf
        self.rleaf = rleaf
        self.operation = operation
        self.level = level

    def __repr__(self):
        return (f'Tree(lleaf={self.lleaf}, ' + 
                f'rleaf={self.rleaf}, ' + 
                f'operation={self.operation}, ' +
                f'level={self.level})')
