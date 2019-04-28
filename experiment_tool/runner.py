import logging
import multiprocessing
from time import time
from typing import Any, Dict, Tuple

from experiment_tool.scope import MemoryScope
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

        self._dag, self._funcs, arg_names = example_reader(self.exp_name)
        self._args = MemoryScope(arg_names)
        for arg_name, arg_value in self.init_args.items():
            self._args[arg_name] = arg_value

        self._storage = FunctionRunStorage(path='test.db')

    def run(self, *, multiproc: bool = False) -> None:
        start_time = time()
        log.info('start experiment')

        # new_dag = self._dag.get_subgraph(self.metrics)
        new_dag = self._dag

        if multiproc:
            gen = new_dag.ready_vertices_generator()
            functions = list(gen.send(None))
            next(gen)
            while functions:
                log.info('functions to run: %s', functions)
                new_functions = []
                for f in functions:
                    self._execute_function(f)
                    temp = gen.send(f)
                    next(gen)
                    new_functions.extend(temp)
                functions = new_functions[:]
        else:
            for func_name in new_dag.topological_sort():
                log.info('execute function: %s', func_name)
                self._execute_function(func_name)

        for metric in self.metrics:
            log.info('METRIC %s = %s', metric, self._args[metric])

        log.info('finish experiment')
        log.info('experiment run time: %s seconds', time() - start_time)

    def _execute_function(self, func_name: str) -> None:
        func_obj, args_names, result_names = self._funcs[func_name]
        args_mapping = {
                key: self._args[key] for key in iter(self._args)
        }

        func_result = self._storage.get_function_result(func_obj, args_mapping)

        if func_result is None:
            log.info('calculate the function %s', func_name)
            args_order = [args_mapping[arg_name] for arg_name in args_names]
            func_result = isolated_function_running(func_obj, args_order)
            func_result = (func_result, )  # TODO think about this
            self._storage.add_function(func_obj, args_mapping, func_result)
        else:
            log.info('function %s already calculate', func_name)

        if len(result_names) == 1:
            self._args[result_names[0]] = func_result[0]
        else:
            for arg_name, arg_value in zip(result_names, *func_result):
                self._args[arg_name] = arg_value


def isolated_function_running(func, args):
    return func(*args)
