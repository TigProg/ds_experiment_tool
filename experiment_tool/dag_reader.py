from .dag import DAG


def example_reader():
    """
    Get experiment, hardcoded function
    :return: dag, functions, arguments
    """
    # create data
    import experiments.first_example as f
    _func = {
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

    # functions / vertices
    functions = {
        key.__name__: [key, *value]
        for key, value in _func.items()
    }
    vertices = [
        key.__name__ for key in _func
    ]

    # arguments / edges
    arguments = set()
    for in_args, out_args in _func.values():
        arguments.update(in_args)
        arguments.update(out_args)
    edges = []
    for start_edge, start_args in _func.items():
        for end_edge, end_args in _func.items():
            if set(start_args[1]).intersection(end_args[0]):
                edges.append((start_edge.__name__, end_edge.__name__))

    # dag
    dag = DAG(vertices, edges)

    return dag, functions, arguments
