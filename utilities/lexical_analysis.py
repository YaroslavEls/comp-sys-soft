import re
from data_structures.token import Token

TOKEN_REGEX = {
    'CONSTANT': r'\d+(\.\d+)?',
    'VARIABLE': r'[a-zA-Z_]\w*',
    'OPERATOR': r'[+\*/]',
    'MINUS': r'\-',
    'LPAREN': r'\(',
    'RPAREN': r'\)'
}

def lexical_analysis(expression, syntax_positions=False):
    tokens = []
    position = 0

    while position < len(expression):
        match = None
        for type, pattern in TOKEN_REGEX.items():
            regex = re.compile(pattern)
            match = regex.match(expression, position)
            if match:
                token = Token(type, match.group(0), position)
                tokens.append(token)
                position = match.end(0)
                break
        if not match:
            if expression[position].isspace():
                position += 1
            else:
                error = SyntaxError(
                    f'Unknown symbol: {expression[position]} ' +
                    f'(index {position})')
                raise ExceptionGroup('Lexical Analysis Errors:', [error])
            
    if not syntax_positions:
        i = 0
        for token in tokens:
            token.position = i
            i += 1

    return tokens
