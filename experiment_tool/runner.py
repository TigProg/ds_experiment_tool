from experiment_tool.dag import read_first_example


class Runner:
    # def __init__(self, experiment_name, dataset_name, metrics):
    def __init__(self):
        pass
        # self._experiment_name = experiment_name
        # self._dataset_name = dataset_name
        # self._metrics = metrics

    def run(self):
        dag, function, args = read_first_example()
        simplified_dag = dag.get_subgraph(None, None)
        # print(simplified_dag.topological_sort())
        for v in simplified_dag.topological_sort():
            current_args = [
                ...
            ]
            temp = function[v]()


if __name__ == '__main__':
    Runner().run()
