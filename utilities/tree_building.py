from data_structures.token import Token
from data_structures.tree import Tree

def get_subtrees(tokens, operators, level):
    subtrees = []
    for token in tokens:
        if token.value in operators:
            left = next((x for x in tokens if x.position == (token.position - 1)))
            right = next((x for x in tokens if x.position == (token.position + 1)))

            if left.free and right.free:
                token.free = left.free = right.free = False
                subtree = Tree(left, right, token, level)
                subtrees.append(subtree)
            else:
                if operators == ['*', '/']:
                    left.free = False
                    next_operator = next((x for x in tokens if x.position == (right.position + 1)), False)
                    if next_operator:
                        if next_operator.value in ['+', '-']:
                            right.free = False

    return subtrees

def simple_expressions_to_subtrees(tokens, subtrees):
    for subtree in subtrees:
        position = subtree.operation.position
        for token in [subtree.lleaf, subtree.rleaf, subtree.operation]:
            tokens.remove(token)
        tokens.append(Token('SUBTREE', subtree, position))

    tokens = sorted(tokens, key=lambda token: token.position)
    for i in range(len(tokens)):
        tokens[i].position = i
        if tokens[i].type == 'PARENTHASES':
            continue
        tokens[i].free = True

    return tokens

def child_expressions_to_subtrees(tokens, replacements):
    tokens = tokens.copy()

    for exp, tree in replacements:
        length = len(exp)
        for i in range(len(tokens) - length + 1):
            if tokens[i:i + length] == exp:
                if tokens[i-1].type == 'LPAREN' and tokens[i+length].type == 'RPAREN':
                    tokens[i-1:i+length+1] = tree
                    break

    for i in range(len(tokens)):
        tokens[i].position = i

    return tokens

def expression_to_tree(tokens, level):
    tokens = tokens.copy()

    if not any(token.type in ['OPERATOR', 'MINUS'] for token in tokens):
        return tokens

    for token in [token for token in tokens if token.type == 'PARENTHASES']:
        if level > token.value.level:
            token.type = 'SUBTREE'
            token.free = True 

    tmp1 = get_subtrees(tokens, ['*', '/'], level)
    tmp2 = get_subtrees(tokens, ['+', '-'], level)
    subtrees = [*tmp1, *tmp2]

    tokens = simple_expressions_to_subtrees(tokens, subtrees)
    return expression_to_tree(tokens, level+1)

def build_tree(expression):
    tokens = None

    if expression.children:
        replacements = []
        for child in expression.children:
            child_tree = build_tree(child)
            child_tree[0].type = 'PARENTHASES'
            child_tree[0].free = False
            replacements.append((child.tokens, child_tree))
        tokens = child_expressions_to_subtrees(expression.tokens, replacements)

    return expression_to_tree(tokens if tokens else expression.tokens, 0)
