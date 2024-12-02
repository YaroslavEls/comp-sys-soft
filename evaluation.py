import pandas as pd
from data_structures.expression import Expression
from utilities.lexical_analysis import lexical_analysis
from utilities.optimization import optimize_expression
from utilities.tree_building import build_tree
from utilities.equivalents_generation import get_associative_equivalents
from utilities.matrix_system_modeling import (model_matrix_system,
                                              evaluate_matrix_system)

def evaluate():
    # original = 'T*H-T*O-F*F*5-F*F*Q-G*F*5-G*Q-F/(D-Q-R)-G/(D-Q-R)'
    original = 'A*B+A*C+(D*E+D*F+(G*K+G*H))'

    oo = optimize_expression(original)
    tokens = lexical_analysis(oo)
    exp = Expression(tokens)
    ot = build_tree(exp)[0]
    os = model_matrix_system(ot)

    equivalents = get_associative_equivalents(original, 100)
    data = []
    for expression in equivalents:
        optimized = optimize_expression(expression)
        tokens = lexical_analysis(optimized)
        exp = Expression(tokens)

        tree = build_tree(exp)[0]
        system = model_matrix_system(tree)
        data.append((expression, tree, system))

    data = sorted(data, key=lambda x: len(x[2].history))
    data.insert(0, (original, ot, os))

    table = []
    for item in data:
        tmp = []
        t, S, E = evaluate_matrix_system(item[1], item[2])

        tmp.append(item[0])
        tmp.append(item[1].value.level + 1)
        tmp.append(t)
        tmp.append(round(S, 2))
        tmp.append(round(E, 2))

        table.append(tmp)

    df = pd.DataFrame(table, columns=['Expression', 'Tree Depth', 't', 'S', 'E'])
    print(df)
    # print(df.to_latex(index=False, float_format="{:.2f}".format))
    

evaluate()
