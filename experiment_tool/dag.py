import logging

log = logging.getLogger(__name__)


class DAG:
    def __init__(self, vertices, edges):
        self._graph_out = {}
        self._graph_in = {}
        self._add_vertices(vertices)
        self._add_edges(edges)
        self._validate()

    def _add_vertices(self, vertices):
        """
        Add list of vertices to dag.
        """
        for v in vertices:
            self._graph_in.setdefault(v, set())
            self._graph_out.setdefault(v, set())

    def _add_edges(self, edges):
        """
        Add list of edges to dag.
        Throws exception if there is an end of an edge that is not in dag.
        """
        for (x, y) in edges:
            if (x not in self._graph_out) or (y not in self._graph_out):
                raise KeyError("No such vertex in a _graph")
            self._graph_out[x].add(y)
            self._graph_in[y].add(x)

    def get_vertices(self):
        return self._graph_out.keys()

    def get_edges(self):
        edges = []
        for v in self._graph_out:
            for u in self._graph_out[v]:
                edges.append((v, u))
        return edges

    def topological_sort(self) -> list:
        """
        Return a topological sort of dag.
        """
        log.debug('start topological sort')
        res = []
        visited = set()

        def dfs(x):
            visited.add(x)
            for y in self._graph_out[x]:
                if y not in visited:
                    dfs(y)
            res.append(x)
        for v in self._graph_out:
            if v not in visited:
                dfs(v)
        res.reverse()
        log.debug('finish topological sort')
        return res

    def ready_vertices_generator(self):
        set_ready = set()
        set_new = set()
        for v in self._graph_in:
            if not self._graph_in[v]:
                set_new.add(v)
        log.info(f"initial set: {set_new}")
        while True:
            yield set_new
            set_new = set()
            vert_ready = yield
            log.info(f"vertex received: {vert_ready}")
            set_ready.add(vert_ready)
            log.info(f"set_ready: {set_ready}")
            for v in self._graph_out[vert_ready]:
                for u in self._graph_in[v]:
                    if u not in set_ready:
                        break
                else:
                    set_new.add(v)
            log.info(f"set_new: {set_new}")

    def get_subgraph(self, metrics, modified=None):
        """
        Return subgraph that contains all vertices, functions in which should be recalculated
        in order to obtain desired metrics.
        None value for modified means all vertices.
        """
        vertices = set()
        edges = []
        visited = set()

        if modified is None:
            modified = self._graph_out.keys()

        def dfs(x):
            visited.add(x)
            recalculate = False
            if x in metrics:
                recalculate = True
            for y in self._graph_out[x]:
                if y not in visited:
                    if dfs(y):
                        recalculate = True
                elif y in vertices:
                    recalculate = True
            if recalculate:
                vertices.add(x)
                return True
            return False

        for v in modified:
            if v not in visited:
                dfs(v)

        for (u, v) in self.get_edges():
            if (u in vertices) and (v in vertices):
                edges.append((u, v))

        res = DAG(vertices, edges)
        return res

    def _validate(self):
        """
        Check if dag is valid.
        Throws exception otherwise.
        """
        visited = {}  # values : 0 - not visited, 1 - in, 2 - out

        def dfs(x):
            visited[x] = 1
            for y in self._graph_out[x]:
                if visited[y] == 1:
                    return True
                if not visited[y]:
                    if dfs(y):
                        return True
            visited[x] = 2
            return False

        for v in self._graph_out:
            visited.setdefault(v, 0)
        for v in self._graph_out:
            if not visited[v]:
                if dfs(v):
                    raise Exception("Graph contains cycle")
