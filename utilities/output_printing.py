def print_tree_schema(token, level=0):
    if level == 0:
        print('Parallel Tree Schema:')
    if token.type == 'SUBTREE':
        subtree = token.value
        if subtree.rleaf:
            print_tree_schema(subtree.rleaf, level + 1)
        print(' ' * 4 * level + '->', subtree.operation.value)
        if subtree.lleaf:
            print_tree_schema(subtree.lleaf, level + 1)
    elif token.type == 'VARIABLE' or token.type == 'CONSTANT':
        print(' ' * 4 * level + '->', token.value)

def print_tree_details(token, indent=0):
    indent_str = '    ' * indent
    if token.type == 'NODE':
        node = token.value
        print(f"{indent_str}Node (Level: {node.level})")
        if node.lleaf:
            print(f"{indent_str}Left:")
            print_tree_details(node.lleaf, indent + 1)
        print(f"{indent_str}Operation: {node.operation.value}")
        if node.rleaf:
            print(f"{indent_str}Right:")
            print_tree_details(node.rleaf, indent + 1)
    elif token.type == 'VARIABLE':
        print(f"{indent_str}Variable: {token.value}")
    elif token.type == 'OPERATOR':
        print(f"{indent_str}Operator: {token.value}")
