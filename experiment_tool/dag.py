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
    def __init__(self, vertices, edges):
        self.graph = {}
        self._add_vertices(vertices)
        self._add_edges(edges)
        self._validate()

    def _add_vertices(self, vertices):
        """
        Add list of vertices to dag.
        """
        for v in vertices:
            self.graph.setdefault(v, [])

    def _add_edges(self, edges):
        """
        Add list of edges to dag.
        Throws exception if there is an end of an edge that is not in dag.
        """
        for (x, y) in edges:
            if (x not in self.graph.keys()) or (y not in self.graph.keys()):
                raise KeyError("No such vertex in a graph")
            self.graph[x].append(y)

    def topological_sort(self) -> list:
        """
        Return a topological sort of dag.
        """
        res = []
        visited = {}

        def dfs(x):
            visited[x] = True
            for y in self.graph[x]:
                if not visited[y]:
                    dfs(y)
            res.append(x)

        for v in self.graph.keys():
            visited.setdefault(v, False)
        for v in self.graph.keys():
            if not visited[v]:
                dfs(v)
        res.reverse()
        return res

    def get_subgraph(self, metrics, modified):
        """
        Return subgraph that contains all vertices, functions in which should be recalculated
        in order to obtain desired metrics.
        """
        return self

    def _validate(self):
        """
        Check if dag is valid.
        Throws exception otherwise.
        """
        visited = {}  # values : 0 - not visited, 1 - in, 2 - out

        def dfs(x):
            visited[x] = 1
            for y in self.graph[x]:
                if visited[y] == 1:
                    return True
                if not visited[y]:
                    if dfs(y):
                        return True
            visited[x] = 2
            return False

        for v in self.graph.keys():
            visited.setdefault(v, 0)
        for v in self.graph.keys():
            if not visited[v]:
                if dfs(v):
                    raise Exception("Graph contains cycle")
