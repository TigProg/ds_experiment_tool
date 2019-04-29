import logging
import multiprocessing
from time import time
from typing import Any, Dict, Tuple

from experiment_tool.dag_reader import example_reader
from experiment_tool.function_run_storage import FunctionRunStorage
from experiment_tool.scope import MemoryScope


log = logging.getLogger(__name__)


class MiniRunner:
    def __init__(self, func, scope):
        self._storage = FunctionRunStorage(path='test.db')
        self._func = func[0]
        self._in_args = func[1]
        self._out_args = func[2]
        self._args = scope

    def run(self):
        args_order = [self._args[arg_name] for arg_name in self._in_args]
        func_result = isolated_function_running(self._func, args_order)
        if len(self._out_args) == 1:
            self._args[self._out_args[0]] = func_result
        else:
            for arg_name, arg_value in zip(self._out_args, func_result):
                self._args[arg_name] = arg_value


def dirty_run(func, scope):
    mini_runner = MiniRunner(func, scope)
    mini_runner.run()


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

            with multiprocessing.Manager() as manager:
                scope = manager.dict()
                for arg_name, arg_value in self.init_args.items():
                    scope[arg_name] = arg_value
                while functions:
                    procs = {}
                    new_functions = []

                    for f in functions:
                        func = self._funcs[f]
                        proc = multiprocessing.Process(
                            target=dirty_run,
                            args=(func, scope),
                        )
                        procs[f] = proc
                        proc.start()
                    for f, proc in procs.items():
                        proc.join()
                        new_functions.extend(gen.send(f))
                    functions = new_functions

                for metric in self.metrics:
                    log.info('METRIC %s = %s', metric, scope[metric])
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
                key: self._args[key] for key in args_names
        }
        packed_func_result = self._storage.get_function_result(
            func_obj, args_mapping
        )

        if packed_func_result.is_nothing():
            log.info('calculate the function %s', func_name)
            args_order = [args_mapping[arg_name] for arg_name in args_names]
            func_result = isolated_function_running(func_obj, args_order)
            self._storage.add_function(func_obj, args_mapping, func_result)
        else:
            func_result = packed_func_result.unpack()
            log.info('function %s already calculate', func_name)

        if len(result_names) == 1:
            self._args[result_names[0]] = func_result
        else:
            for arg_name, arg_value in zip(result_names, func_result):
                self._args[arg_name] = arg_value


def isolated_function_running(func, args):
    return func(*args)
