from experiment_tool.dag import DAG
import random, pytest


def dag_1():
    vertices = list(range(10))
    random.shuffle(vertices)
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 7),
             (2, 7), (3, 7), (4, 8), (5, 8), (6, 8), (7, 9), (8, 9)]
    return DAG(vertices, edges)


def dag_2():
    vertices = list(range(8))
    random.shuffle(vertices)
    edges = [(0, 1), (1, 2), (1, 4), (2, 3), (4, 5), (4, 6)]
    return DAG(vertices, edges)


@pytest.fixture(scope="function",
                params=[dag_1(), dag_2()],
                ids=["first_example", "custom_graph_2"])
def param_topological_sort(request):
    return request.param


def test_topological_sort(param_topological_sort):
    dag = param_topological_sort
    assert check_topological_sort(dag, dag.topological_sort())


def check_topological_sort(dag, sorted_list):
    edges = dag.get_edges()
    order = {}
    for i in range(len(sorted_list)):
        order[sorted_list[i]] = i
    for e in edges:
        u, v = e
        if order[u] > order[v]:
            return False
    return True


@pytest.fixture(scope="function",
                params=[(dag_1(), [5], [9], ({5, 9, 8}, {(8, 9), (5, 8)})),
                        (dag_2(), [0], [5, 7], ({1, 4, 0, 5}, {(0, 1), (4, 5), (1, 4)}))],
                ids=["first_example", "custom_graph_2"])
def param_get_subgraph(request):
    return request.param


def test_get_subgraph(param_get_subgraph):
    dag, modified, metrics, expected_output = param_get_subgraph
    subgraph = dag.get_subgraph(metrics, modified)
    vertices = set(subgraph.get_vertices())
    edges = set(subgraph.get_edges())
    expected_vertices, expected_edges = expected_output
    assert (vertices == expected_vertices) and (edges == expected_edges)

