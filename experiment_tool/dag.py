class DAG:
    def __init__(self, vertices, edges):
        self._graph = {}
        self._add_vertices(vertices)
        self._add_edges(edges)
        self._validate()

    def _add_vertices(self, vertices):
        """
        Add list of vertices to dag.
        """
        for v in vertices:
            self._graph.setdefault(v, [])

    def _add_edges(self, edges):
        """
        Add list of edges to dag.
        Throws exception if there is an end of an edge that is not in dag.
        """
        for (x, y) in edges:
            if (x not in self._graph) or (y not in self._graph):
                raise KeyError("No such vertex in a _graph")
            self._graph[x].append(y)

    def topological_sort(self) -> list:
        """
        Return a topological sort of dag.
        """
        res = []
        visited = set()

        def dfs(x):
            visited.add(x)
            for y in self._graph[x]:
                if y not in visited:
                    dfs(y)
            res.append(x)

        for v in self._graph:
            if v not in visited:
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
            for y in self._graph[x]:
                if visited[y] == 1:
                    return True
                if not visited[y]:
                    if dfs(y):
                        return True
            visited[x] = 2
            return False

        for v in self._graph:
            visited.setdefault(v, 0)
        for v in self._graph:
            if not visited[v]:
                if dfs(v):
                    raise Exception("Graph contains cycle")
