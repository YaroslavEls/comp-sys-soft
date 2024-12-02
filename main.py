import sys
from data_structures.expression import Expression
from utilities.lexical_analysis import lexical_analysis
from utilities.syntax_analysis import syntax_analysis
from utilities.optimization import optimize_expression
from utilities.tree_building import build_tree
from utilities.output_printing import (print_equivalent_forms,
                                       print_tree_schema,
                                       print_gantt_chart,
                                       print_system_performance_report)
from utilities.equivalents_generation import (get_associative_equivalents,
                                              get_commutative_equivalents)
from utilities.matrix_system_modeling import (model_matrix_system,
                                              evaluate_matrix_system)

def main():
    if len(sys.argv) < 2:
        print('Missing required argument: expression')
        exit(1)

    try:
        original = sys.argv[1]
        print(f'Input Expression: {original}')

        tokens = lexical_analysis(original, syntax_positions=True)
        report = syntax_analysis(tokens)
        print(report)

        a_eq = get_associative_equivalents(original, 100)
        c_eq = get_commutative_equivalents(original, 100)
        print_equivalent_forms(a_eq, 0, 5)
        print_equivalent_forms(c_eq, 1, 5)

        optimized = optimize_expression(original)
        print(f'Optimized Expression: {optimized}')

        tokens = lexical_analysis(optimized)
        expression = Expression(tokens)
        tree = build_tree(expression)[0]
        print_tree_schema(tree)

        system = model_matrix_system(tree)
        print_gantt_chart(system.history)
        print_system_performance_report(*evaluate_matrix_system(tree, system))
    except ExceptionGroup as eg:
        print(eg)
        for e in eg.exceptions:
            print(f'\t{e}')

if __name__ == "__main__":
    main()
