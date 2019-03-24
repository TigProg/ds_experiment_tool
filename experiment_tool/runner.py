from time import time
from experiment_tool.dag_reader import example_reader


class Runner:
    def __init__(self, experiment_name, dataset_name, metrics):
        self._experiment_name = experiment_name
        self._dataset_name = dataset_name
        self._metrics = metrics
        self._dag = None
        self._funcs = None
        self._args = None
        self._null_value = object()

    def run(self):
        START_TIME = time()  # FIXME
        self._dag, self._funcs, self._args = example_reader()
        self._init_args()
        self._dag = self._dag.get_subgraph(None, None)
        for func_name in self._dag.topological_sort():
            self._execute_function(func_name)
        print(time() - START_TIME)  # FIXME
        for metric in self._metrics:
            print(self._args[metric])

    def _init_args(self):
        args_with_values = {}
        for arg in self._args:
            args_with_values[arg] = self._null_value
        self._args = args_with_values
        for arg_name, arg_value in self._dataset_name.items():
            self._args[arg_name] = arg_value

    def _execute_function(self, func_name):
        func, func_args, func_res = self._funcs[func_name]
        in_value = [
            self._args[i] for i in func_args
        ]
        if self._null_value in in_value:
            raise ValueError('some variable is not defined')
        out_value = func(*in_value)
        if not isinstance(out_value, tuple):
            out_value = (out_value,)
        for arg_name, arg_value in zip(func_res, out_value):
            self._args[arg_name] = arg_value


if __name__ == '__main__':
    Runner('first_example', {'name': 'first_example'}, ('result', )).run()
