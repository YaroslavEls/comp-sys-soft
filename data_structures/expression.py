class Expression():
    def __init__(self, tokens):
        self.tokens = tokens
        self.children = self._get_children()
    
    def _get_children(self):
        counter = 0
        active = False
        ignore = 0
        res = []

        for token in self.tokens:
            if token.type == 'LPAREN':
                if active:
                    ignore += 1
                else:
                    res.append([])
                    active = True

            if active:
                res[counter].append(token)

            if token.type == 'RPAREN':
                if ignore > 0:
                    ignore -= 1
                else:
                    counter += 1
                    active = False

        for i in range(len(res)):
            res[i] = Expression(res[i][1:-1])

        return res
