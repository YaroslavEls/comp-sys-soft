from itertools import combinations
import random
import regex as re

def get_parenthases(expression):
    pattern = r'\((?:[^()]+|(?R))*\)'
    return re.findall(pattern, expression)

def get_terms(expression):
    terms = []
    signs = []
    placeholders = {}
    stack = []

    parenthases = get_parenthases(expression)
    placeholders = {}
    for i in range(len(parenthases)):
        if parenthases[i] in placeholders.keys():
            continue
        value = '%'*(i+1)
        placeholders[parenthases[i]] = value
        expression = expression.replace(parenthases[i], value)

    if expression[0] == '-':
        signs.append('-')
        expression = expression[1:]
    else:
        signs.append('+')

    for sym in expression:
        if sym != '+' and sym != '-':
            stack.append(sym)
            continue

        terms.append(''.join(stack))
        signs.append(sym)
        stack = []
    terms.append(''.join(stack))
    return terms, signs, placeholders

def get_factors(terms):
    variables = []
    for term in terms:
        if '*' not in term:
            continue

        tmp = term.split('*')
        if len(tmp) > 2:
            combs = [combinations(tmp, r) for r in range(2, len(tmp)+1)]
            for comb in combs:
                for i in set(comb):
                    variables.append('*'.join(i))
        variables += tmp

    return sorted(list(set(variables)))

def get_dividers(terms):
    variables = set(term.split('/')[1] for term in terms if '/' in term)
    return sorted(list(variables))

def get_full_terms(expression, res):
    terms, _, placeholders = get_terms(expression)
    for key in placeholders.keys():
        get_full_terms(key[1:-1], res)
    res.append(sorted(terms))
    return res

def is_var_in_term(var, term):
    pattern = rf'(?<=^|[\*/]){re.escape(var)}(?=$|[\*/])'
    if re.search(pattern, term):
        return True
    return False

def transform_multiplication(terms, signs, factors):
    terms_g = terms.copy()
    res = ''
    for factor in factors:
        matches = []
        for term in terms:
            if is_var_in_term(factor, term):
                matches.append(term)

        if len(matches) == 0:
            continue
        elif len(matches) == 1:
            sign = signs[terms_g.index(matches[0])]
            res += f'{sign}{matches[0]}'
        else:
            tmp = []
            for term in matches:
                index = term.index(factor)
                if index == 0:
                    tmp.append(term.replace(factor, '', 1)[1:])
                else:
                    tmp.append(term[:index-1] + term[index+len(factor):])
            parent = [signs[terms_g.index(term)] + tmp[matches.index(term)]
                      for term in matches]
            parent = ''.join(parent)
            parent = parent[1:] if parent[0] == '+' else parent
            res += f'+{factor}*({parent})'

        for match in matches:
            terms.remove(match)

    return res

def transform_division(terms, signs, dividers):
    terms_g = terms.copy()
    res = ''
    for divider in dividers:
        matches = []
        for term in terms:
            if (is_var_in_term(divider, term) and 
                (divider == term.split('/')[1])):
                matches.append(term)

        if len(matches) == 0:
            continue
        elif len(matches) == 1:
            sign = signs[terms_g.index(matches[0])]
            res += f'{sign}{matches[0]}'
        else:
            offset = len(divider) + 1
            parent = [signs[terms_g.index(term)] + term[0:len(term)-offset]
                      for term in matches]
            parent = ''.join(parent)
            parent = parent[1:] if parent[0] == '+' else parent
            res += f'+({parent})/{divider}'

        for match in matches:
            terms.remove(match)

    return res

def transform_simple_terms(terms, signs):
    res = ''
    for term in terms:
        res += f'{signs[terms.index(term)]}{term}'
    return res

def transform(terms, signs, factors, dividers):
    mul_terms = [term for term in terms.copy() if '/' not in term]
    div_terms = [term for term in terms.copy() if '/' in term]
    simp_terms = [term for term in terms.copy() 
                  if ('*' not in term) and ('/' not in term)]
    
    mul_signs = [signs[terms.index(term)] for term in mul_terms]
    div_signs = [signs[terms.index(term)] for term in div_terms]
    simp_signs = [signs[terms.index(term)] for term in simp_terms]

    mul = transform_multiplication(mul_terms, mul_signs, factors)
    div = transform_division(div_terms, div_signs, dividers)
    simp = transform_simple_terms(simp_terms, simp_signs)

    res = mul + div + simp
    return res[1:] if res[0] == '+' else res

def apply_associative_law(expression):
    children = get_parenthases(expression)
    parenthases = {}
    for child in children:
        transformed = apply_associative_law(child[1:-1])
        transformed = f'({transformed})'
        parenthases[child] = transformed
        expression = expression.replace(child, transformed, 1)

    terms, signs, placeholders = get_terms(expression)
    factors = get_factors(terms)
    random.shuffle(factors)
    dividers = get_dividers(terms)
    random.shuffle(dividers)
    final = transform(terms, signs, factors, dividers)

    ph = sorted(placeholders.items(), key=lambda item: item[1], reverse=True)
    for key, value in ph:
        final = final.replace(value, key)

    return final

def apply_commutative_law(expression):
    children = get_parenthases(expression)
    parenthases = {}
    for child in children:
        transformed = apply_commutative_law(child[1:-1])
        transformed = f'({transformed})'
        parenthases[child] = transformed
        expression = expression.replace(child, transformed, 1)

    terms, signs, placeholders = get_terms(expression)
    terms = [signs[i] + terms[i] for i in range(len(terms))]
    random.shuffle(terms)
    final = ''.join(terms)
    final = final[1:] if final[0] == '+' else final

    ph = sorted(placeholders.items(), key=lambda item: item[1], reverse=True)
    for key, value in ph:
        final = final.replace(value, key)

    return final

def get_associative_equivalents(expression, n):
    result_expressions = []
    result_terms = []
    for _ in range(n):
        result = apply_associative_law(expression)
        if result in result_expressions:
            continue
        full_terms = get_full_terms(result, [])
        if full_terms in result_terms:
            continue
        result_expressions.append(result)
        result_terms.append(full_terms)

        for _ in range(1):
            result = apply_associative_law(result)
            if result in result_expressions:
                continue
            full_terms = get_full_terms(result, [])
            if full_terms in result_terms:
                continue
            result_expressions.append(result)
            result_terms.append(full_terms)

    return result_expressions

def get_commutative_equivalents(expression, n):
    result_expressions = []
    for _ in range(n):
        result = apply_commutative_law(expression)
        if result not in result_expressions:
            result_expressions.append(result)
    return result_expressions
