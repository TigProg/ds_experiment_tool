def read_first_example():
    # TODO
    import experiments.first_example as f
    first_dag = DAG()
    # add funcs / vertices
    _funcs = [
        f.slow_1, f.slow_2, f.slow_3,
        f.fib_1, f.fib_2, f.fib_3,
        f.get_sum, f.check, f.get_result,
    ]
    result_funcs = {
        i.__name__: i
        for i in _funcs
    }
    first_dag._add_vertices([
        i.__name__ for i in _funcs
    ])
    # add args / edges
    first_dag._add_edges(...)  # FIXME how?
    result_args = ...
    return first_dag, result_funcs, result_args


class DAG:
    def __init__(self):
        raise NotImplementedError

    def _add_vertices(self, vertices):
        """
        Add list of vertices to dag.
        """
        raise NotImplementedError

    def _add_edges(self, edges):
        """
        Add list of edges to dag.
        Throws custom exception if there is an end of an edge that is not in DAG.
        """
        raise NotImplementedError

    def topological_sort(self) -> list:
        """
        Return a topological sort of dag.
        """
        raise NotImplementedError

    def get_subgraph(self, metrics, modified) -> DAG:
        """
        Return subgraph that contains all vertices, functions
        in which should be recalculated in order to obtain desired metrics.
        """
        raise NotImplementedError

    # TODO maybe this is private method?
    def validate(self):
        """
        Check if dag is valid.
        Throws custom exception otherwise.
        """
        raise NotImplementedError
