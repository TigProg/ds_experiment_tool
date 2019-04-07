import inspect
import json
from time import time
from sys import stderr
from typing import Any, Dict, Set, Tuple

from experiment_tool.dag_reader import example_reader
from experiment_tool.storage_sqlite import SQLiteExpStorage


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

        self._storage_path = 'test.db'
        self._storage_obj = None

    def _init_args(self, arg_names: Set[str]) -> None:
        self._args = {
            arg: self._null_value for arg in arg_names
        }
        for arg_name, arg_value in self.init_args.items():
            self._args[arg_name] = arg_value

    def run(self) -> None:
        start_time = time()  # TODO: add logging

        exp_id = self._check_graph_structure()
        # exp_id = self._init_graph_id()
        # exit()
        modified = set()
        if exp_id is not None:
            print('EXIT')
            exit()
            for _, func_name, func_text in self._get_functions_from_storage():
                if inspect.getsource(self._funcs[func_name]) != func_text:
                    modified.add(func_name)
            # for _, arg_name,
            # """надо проверить отдельные функции"""
            # """затем делать как обычно"""
            # # TODO

        self._dag = self._dag.get_subgraph(self.metrics, modified)
        for func_name in self._dag.topological_sort():
            self._execute_function(func_name)
        for metric in self.metrics:
            print('{name}: {value}'.format(
                name=metric, value=self._args[metric]
            ))

        # if exp_id is None:
        #     exp_id = self._add_graph_structure()
        #     exit()
        #     # TODO

        print(time() - start_time, 'seconds', file=stderr)

    def _check_graph_structure(self):
        print('start _check_graph_structure')
        self._storage_obj = self._storage_obj \
                            or SQLiteExpStorage(self._storage_path)
        exp_json = json.dumps({
            name: [value[1], value[2]]
            for name, value in self._funcs.items()
        }, sort_keys=True)
        print('end _check_graph_structure')
        return self._storage_obj.get_experiment_id(
            self.experiment_name, exp_json
        )

    def _add_graph_structure(self):
        print('start _add_graph_structure')
        self._storage_obj = self._storage_obj \
                            or SQLiteExpStorage(self._storage_path)
        exp_json = json.dumps({
            name: [value[1], value[2]]
            for name, value in self._funcs.items()
        }, sort_keys=True)
        print('end _add_graph_structure')
        return self._storage_obj.add_experiment(
            self.experiment_name, exp_json
        )

    def _get_functions_from_storage(self):
        print('start _get_functions_from_storage')
        self._storage_obj = self._storage_obj \
                            or SQLiteExpStorage(self._storage_path)
        print('end _get_functions_from_storage')
        return [
            i for i in self._storage_obj.get_functions()
        ]
        #     self._storage_obj.add_experiment(
        #     self.experiment_name, exp_json
        # )

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
