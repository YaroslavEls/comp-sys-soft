import re

sequential_division_pattern = \
    r'([a-zA-Z0-9]+)((?:/\s*(?:[a-zA-Z0-9]+|\([^\)]+\))){4,})'
sequential_substraction_pattern = \
    r'([a-zA-Z0-9]+)((?:-\s*(?:[a-zA-Z0-9]+|\([^\)]+\))){4,})'

def unary_minus(expression):
    if expression[0] == '-':
        expression = '0' + expression
    return re.sub(r'\(-', '(0-', expression)

def remove_useless_parenthases(expression):
    pattern = r'\(\s*([a-zA-Z0-9]+(?:\.[0-9]+)?)\s*\)'
    while re.search(pattern, expression):
        expression = re.sub(pattern, r'\1', expression)
    return expression

def optimize_sequential_division(match):
    numerator = match.group(1)
    denominators = match.group(2)[1:]
    transformed_denominators = re.sub(r'/\s*', '*', denominators)
    return f'{numerator}/({transformed_denominators})'

def optimize_sequential_substraction(match):
    minuend = match.group(1)
    subtrahends = match.group(2)[1:]
    transformed_subtrahends = re.sub(r'-\s*', '+', subtrahends)
    return f'{minuend}-({transformed_subtrahends})'

def optimize_expression(expression):
    expression = ''.join(expression.split())
    expression = unary_minus(expression)
    expression = remove_useless_parenthases(expression)
    expression = re.sub(sequential_division_pattern, 
                        optimize_sequential_division, 
                        expression)
    expression = re.sub(sequential_substraction_pattern, 
                        optimize_sequential_substraction, 
                        expression)
    return expression
