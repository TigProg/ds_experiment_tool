from typing import Callable, Dict, List, Set, Tuple

from experiment_tool.dag import DAG


def get_first_experiment(experiment_name: str) -> Dict[Callable, List]:
    """
    Get hardcoded experiment
    :param experiment_name:
    :return: functions with arguments
    """
    if experiment_name == 'first_example':
        import experiments.first_example as f
        return {
            f.get_5_numbers: [('name',), ('a', 'b', 'c', 's', 'n')],
            f.slow_1: [('a', 's'), ('id1',)],
            f.slow_2: [('b', 's'), ('id2',)],
            f.slow_3: [('c', 's'), ('id3',)],
            f.fib_1: [('n',), ('x',)],
            f.fib_2: [('n',), ('y',)],
            f.fib_3: [('n',), ('z',)],
            f.get_sum: [('id1', 'id2', 'id3'), ('u',)],
            f.check: [('x', 'y', 'z'), ('v',)],
            f.get_result: [('u', 'v'), ('result',)],
        }
    raise ValueError('uncorrect experiment name {}'.format(experiment_name))


def example_reader(experiment_name: str) \
        -> Tuple[DAG, Dict[str, List], Set[str]]:
    """
    Get experiment by name
    :return: dag, functions, arguments
    """
    # get data
    _func = get_first_experiment(experiment_name)

    # functions
    functions = {
        key.__name__: [key, value[0], value[1]]
        for key, value in _func.items()
    }

    # arguments
    arguments = set()
    for in_args, out_args in _func.values():
        arguments.update(in_args)
        arguments.update(out_args)

    # dag
    vertices = [
        key.__name__ for key in _func
    ]
    edges = []
    for start_edge, start_args in _func.items():
        for end_edge, end_args in _func.items():
            if set(start_args[1]).intersection(end_args[0]):
                edges.append((start_edge.__name__, end_edge.__name__))

    dag = DAG(vertices, edges)

    return dag, functions, arguments
