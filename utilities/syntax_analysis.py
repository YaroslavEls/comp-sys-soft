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
    stack = []
    for token in tokens:
        if token.type == 'LPAREN':
            stack.append(token)
        elif token.type == 'RPAREN':
            if not stack:
                errors.append(SyntaxError(
                    f'RPAREN without corresponding LPAREN ' +
                    f'(index {token.position})'))
            else:
                stack.pop()
    if stack:
        for token in stack:
            errors.append(SyntaxError(
                f'LPAREN without corresponding RPAREN ' +
                f'(index {token.position})'))
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
