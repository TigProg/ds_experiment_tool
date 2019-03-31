from time import time
from sys import stderr
from typing import Any, Dict, Tuple

from experiment_tool.dag_reader import example_reader


class Runner:
    def __init__(self,
                 experiment_name: str,
                 dataset_name: Dict[str, Any],
                 metrics: Tuple[str, ...]
                 ) -> None:
        self.experiment_name = experiment_name
        self.init_args = dataset_name
        self.metrics = metrics

        self._null_value = object()
        self._dag, self._funcs, arg_names = example_reader(experiment_name)
        self._init_args(arg_names)

    def _init_args(self, arg_names: set) -> None:
        self._args = {
            arg: self._null_value for arg in arg_names
        }
        for arg_name, arg_value in self.init_args.items():
            self._args[arg_name] = arg_value

    def run(self) -> None:
        start_time = time()  # TODO: add logging

        self._dag = self._dag.get_subgraph(None, None)
        for func_name in self._dag.topological_sort():
            self._execute_function(func_name)
        for metric in self.metrics:
            print('{name}: {value}'.format(
                name=metric, value=self._args[metric]
            ))

        print(time() - start_time, 'seconds', file=stderr)

    def _execute_function(self, func_name: str) -> None:
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
    Runner('first_example', {'name': '1 2 3 0 20'}, ('result',)).run()
