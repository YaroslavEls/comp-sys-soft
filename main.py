import sys
import re

TOKEN_REGEX = {
    'CONSTANT': r'\d+(\.\d+)?',
    'VARIABLE': r'[a-zA-Z_]\w*',
    'OPERATOR': r'[+\*/]',
    'MINUS': r'\-',
    'LPAREN': r'\(',
    'RPAREN': r'\)'
}

TRANSITIONS = {
    'BEGINNING': ['CONSTANT', 'VARIABLE', 'MINUS', 'LPAREN'],
    'CONSTANT': ['OPERATOR', 'MINUS', 'RPAREN'],
    'VARIABLE': ['OPERATOR', 'MINUS', 'RPAREN'],
    'OPERATOR': ['CONSTANT', 'VARIABLE', 'LPAREN'],
    'MINUS': ['CONSTANT', 'VARIABLE', 'LPAREN'],
    'LPAREN': ['CONSTANT', 'VARIABLE', 'MINUS', 'LPAREN'],
    'RPAREN': ['OPERATOR', 'MINUS', 'RPAREN'],
    'ENDING': ['CONSTANT', 'VARIABLE', 'RPAREN']
}

class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return (f'Token(type={self.type}, ' + 
                f'value={self.value}, ' + 
                f'position={self.position})')

class LexicalAnalyzer:
    def __init__(self, expression):
        self.expression = expression
        self.tokens = []
        self.position = 0

    def analyze(self):
        while self.position < len(self.expression):
            match = None
            for type, pattern in TOKEN_REGEX.items():
                regex = re.compile(pattern)
                match = regex.match(self.expression, self.position)
                if match:
                    token = Token(type, match.group(0), self.position)
                    self.tokens.append(token)
                    self.position = match.end(0)
                    break
            if not match:
                if self.expression[self.position].isspace():
                    self.position += 1
                else:
                    raise SyntaxError(
                        f'Unknown symbol: {self.expression[self.position]}')
        return self.tokens

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errors = []

    def _check_beginning(self):
        if self.tokens[0].type not in TRANSITIONS['BEGINNING']:
            self.errors.append(
                f'The expression can not start with {self.tokens[0].type}')

    def _check_middle(self):
        previous = None
        for token in self.tokens:
            if previous:
               if token.type not in TRANSITIONS[previous.type]:
                    self.errors.append(
                        f'{token.type} can not be placed after ' + 
                        f'{previous.type} (index {token.position})')
            previous = token

    def _check_ending(self):
        if self.tokens[-1].type not in TRANSITIONS['ENDING']:
            self.errors.append(
                f'The expression can not end with {self.tokens[-1].type}')

    def _check_parentheses(self):
        left = sum(1 for token in self.tokens if token.type == 'LPAREN')
        right = sum(1 for token in self.tokens if token.type == 'RPAREN')
        if left > right:
            self.errors.append('Not enough closing brackets')
        if left < right:
            self.errors.append('Not enough opening brackets')

    def analyze(self):
        self._check_beginning()
        self._check_middle()
        self._check_ending()
        self._check_parentheses()

def report(expression, errors):
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    print(f'Input expression: {expression}')
    if not errors:
        print(f'{GREEN}No errors detected in the expression{RESET}')
    else:
        for error in errors:
            print(f'{RED}{error}{RESET}')

def main():
    if len(sys.argv) > 1:
        expression = sys.argv[1]
    else:
        print('Missing required argument: expression')
        exit(1)

    try:
        lexer = LexicalAnalyzer(expression)
        tokens = lexer.analyze()
        syntaxer = SyntaxAnalyzer(tokens)
        syntaxer.analyze()
        report(expression, syntaxer.errors)
    except SyntaxError as e:
        print(f'Lexical analysis error: {e}')
    
    
if __name__ == "__main__":
    main()
