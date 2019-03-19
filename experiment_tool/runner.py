from .dag import read_first_example


class Runner:
    def __init__(self, experiment_name, dataset_name, metrics):
        pass
        # self._experiment_name = experiment_name
        # self._dataset_name = dataset_name
        # self._metrics = metrics

    def run(self):
        dag, function, args = read_first_example()
        simplified_dag = dag.get_subgraph()
        for v in simplified_dag.topological_sort():
            exec(function[v].__code__, args)
