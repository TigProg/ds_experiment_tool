import pytest
import random

from experiment_tool.dag import DAG


def dag_1():
    vertices = ['get_5_numbers', 'slow_1', 'slow_2', 'slow_3', 'fib_1', 'fib_2', 'fib_3',
                'get_sum', 'check', 'get_result']
    random.shuffle(vertices)
    edges = [('get_5_numbers', 'slow_1'), ('get_5_numbers', 'slow_2'), ('get_5_numbers', 'slow_3'),
             ('get_5_numbers', 'fib_1'), ('get_5_numbers', 'fib_2'), ('get_5_numbers', 'fib_3'),
             ('slow_1', 'get_sum'), ('slow_2', 'get_sum'), ('slow_3', 'get_sum'),
             ('fib_1', 'check'), ('fib_2', 'check'), ('fib_3', 'check'),
             ('get_sum', 'get_result'), ('check', 'get_result')]
    return DAG(vertices, edges)


def dag_2():
    vertices = list(range(8))
    random.shuffle(vertices)
    edges = [(0, 1), (1, 2), (1, 4), (2, 3), (4, 5), (4, 6)]
    """
                        0
                        |
                        1
                       / \
                      2   4      7
                     /   / \
                    3   5   6
    """
    return DAG(vertices, edges)


@pytest.fixture(scope="function",
                params=[dag_1(), dag_2()],
                ids=["first_example", "custom_graph_2"])
def param_topological_sort(request):
    return request.param


def test_topological_sort(param_topological_sort):
    dag = param_topological_sort

    def check_topological_sort(dag, sorted_list):
        edges = dag.get_edges()
        order = {}
        for i in range(len(sorted_list)):
            order[sorted_list[i]] = i
        for e in edges:
            u, v = e
            if order[u] > order[v]:
                return False, u, v
        return True, None, None

    res, u, v = check_topological_sort(dag, dag.topological_sort())
    assert res, f"{v} before {u} in topological sort, while edge ({u}, {v}) present"


@pytest.fixture(scope="function",
                params=[(dag_1(),
                        [None, 'get_5_numbers', 'fib_2', 'slow_1', 'slow_3', 'fib_3',
                         'slow_2', 'get_sum', 'fib_1', 'check', 'get_result'],
                        [{'get_5_numbers'}, {'fib_2', 'slow_1', 'slow_3', 'fib_3', 'slow_2', 'fib_1'},
                         set(), set(), set(), set(), {'get_sum'}, set(), {'check'}, {'get_result'}, set()])],
                ids=["first_example"])
def param_ready_vertices_generator(request):
    return request.param


def test_ready_vertices_generator(param_ready_vertices_generator):
    dag, order, expected_output = param_ready_vertices_generator
    g = dag.ready_vertices_generator()
    output = []
    for f in order:
        output.append(g.send(f))
    assert output == expected_output


@pytest.fixture(scope="function",
                params=[(dag_1(), ['fib_2'], ['get_result'],
                        ({'fib_2', 'get_result', 'check'}, {('check', 'get_result'), ('fib_2', 'check')})),
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
