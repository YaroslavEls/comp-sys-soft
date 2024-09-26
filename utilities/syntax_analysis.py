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

def check_beginning(tokens, errors):
    if tokens[0].type not in TRANSITIONS['BEGINNING']:
        errors.append(SyntaxError(
            f'The expression can not start with {tokens[0].type}'))
    return errors

def check_middle(tokens, errors):
    previous = None
    for token in tokens:
        if previous:
            if token.type not in TRANSITIONS[previous.type]:
                errors.append(SyntaxError(
                    f'{token.type} can not be placed after ' + 
                    f'{previous.type} (index {token.position})'))
        previous = token
    return errors

def check_ending(tokens, errors):
    if tokens[-1].type not in TRANSITIONS['ENDING']:
        errors.append(SyntaxError(
            f'The expression can not end with {tokens[-1].type}'))
    return errors

def check_parentheses(tokens, errors):
    left = sum(1 for token in tokens if token.type == 'LPAREN')
    right = sum(1 for token in tokens if token.type == 'RPAREN')
    if left > right:
        errors.append(SyntaxError('Not enough closing brackets'))
    if left < right:
        errors.append(SyntaxError('Not enough opening brackets'))
    return errors

def syntax_analysis(tokens):
    errors = []
    steps = [
        check_beginning,
        check_middle,
        check_ending,
        check_parentheses
    ]
    for step in steps:
        errors = step(tokens, errors)

    if errors:
        eg = ExceptionGroup('Syntax Analysis Errors:', errors)
        raise eg
    else:
        return 'No errors detected in the expression'
