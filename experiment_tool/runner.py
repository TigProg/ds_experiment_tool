import logging
from time import time
from typing import Any, Dict, Set, Tuple

from experiment_tool.dag_reader import example_reader
from experiment_tool.function_run_storage import FunctionRunStorage


log = logging.getLogger(__name__)


class Runner:
    def __init__(self,
                 experiment_name: str,
                 dataset_name: Dict[str, Any],
                 metrics: Tuple[str, ...]
                 ) -> None:
        self.exp_name = experiment_name
        self.init_args = dataset_name
        self.metrics = metrics

        self._null_value = object()
        self._dag, self._funcs, arg_names = example_reader(self.exp_name)
        self._init_args(arg_names)

        self._storage = FunctionRunStorage(path='test.db')

    def _init_args(self, arg_names: Set[str]) -> None:
        self._args = {
            arg: self._null_value for arg in arg_names
        }
        for arg_name, arg_value in self.init_args.items():
            self._args[arg_name] = arg_value

    def run(self) -> None:
        start_time = time()
        log.info('start experiment')

        # TODO
        # add DAG().get_subgraph() for metrics

        for func_name in self._dag.topological_sort():
            log.info('execute function: %s', func_name)
            self._execute_function(func_name)

        for metric in self.metrics:
            log.info('METRIC %s = %s', metric, self._args[metric])

        log.info('finish experiment')
        log.info('experiment run time: %s seconds', time() - start_time)

    def _execute_function(self, func_name: str) -> None:
        func_obj, args_names, result_names = self._funcs[func_name]
        args_mapping = {i: self._args[i] for i in args_names}
        if self._null_value in args_mapping.values():
            not_defined_vars = (
                i for i in args_mapping.values() if i is self._null_value
            )
            error_msg = \
                'variable(s) {} is/are not defined while running {}'.format(
                    not_defined_vars, func_name
                )
            log.error(error_msg)
            raise ValueError(error_msg)

        func_result = self._storage.get_function_result(func_obj, args_mapping)

        if func_result is None:
            log.info('calculate the function %s', func_name)
            args_order = [args_mapping[arg_name] for arg_name in args_names]
            func_result = func_obj(*args_order)
            func_result = (func_result, )  # TODO think about this
            self._storage.add_function(func_obj, args_mapping, func_result)
        else:
            log.info('function %s already calculate', func_name)

        if len(result_names) == 1:
            self._args[result_names[0]] = func_result[0]
        else:
            for arg_name, arg_value in zip(result_names, *func_result):
                self._args[arg_name] = arg_value
