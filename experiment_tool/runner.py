import inspect
import json
import logging
from time import time
from typing import Any, Dict, Set, Tuple

from experiment_tool.dag_reader import example_reader
from experiment_tool.storage_sqlite import SQLiteExpStorage


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

        self._storage = SQLiteExpStorage(path='test.db')

    def _init_args(self, arg_names: Set[str]) -> None:
        self._args = {
            arg: self._null_value for arg in arg_names
        }
        for arg_name, arg_value in self.init_args.items():
            self._args[arg_name] = arg_value

    def run(self) -> None:
        start_time = time()

        exp_json = json.dumps(
            {name: value[1:] for name, value in self._funcs.items()},
            sort_keys=True
        )
        exp_ids = self._storage.get_experiment_ids(self.exp_name, exp_json)

        if exp_ids:
            log.info(
                'experiments with a similar structure are found with ids: {}'\
                    .format(exp_ids)
            )
            exp_id = exp_ids[-1]  # get last experiment id

            # load all arguments
            modified_init_args = set()

            saves_arguments = self._storage.get_arguments(exp_id)
            assert saves_arguments.keys() == self._args.keys(), \
                'some bug in loading arguments'
            for arg_name, arg_value in saves_arguments.items():
                if arg_name in self.init_args:
                    if arg_value != self.init_args[arg_name]:
                        modified_init_args.add(arg_name)
                else:
                    self._args[arg_name] = arg_value

            # load all functions
            modified = set()

            saves_functions = self._storage.get_functions(exp_id)
            assert saves_functions.keys() == self._funcs.keys(), \
                'some bug in loading functions'
            for func_name, func_code in saves_functions.items():
                if inspect.getsource(self._funcs[func_name][0]) != func_code:
                    modified.add(func_name)

            # FIXME: add functions to modified if input argument
            #  of this function there are in modified_init_args
            for func_name, func_info in self._funcs.items():
                input_args = func_info[1]
                if modified_init_args.intersection(input_args):
                    modified.add(func_name)
        else:
            log.info('experiments with a similar structure were not found')
            exp_id = self._storage.add_experiment(self.exp_name, exp_json)
            modified = set(self._funcs)

        v_with_metrics = set()
        for func_name, func_info in self._funcs.items():
            output_args = func_info[2]
            if set(output_args).intersection(self.metrics):
                v_with_metrics.add(func_name)

        log.debug('metrics: {}'.format(self.metrics))
        log.debug('metrics_funcs: {}'.format(v_with_metrics))
        log.debug('modified: {}'.format(modified))

        log.debug('old dag: {}'.format(self._dag._graph))
        new_dag = self._dag.get_subgraph(v_with_metrics, modified)
        log.debug('new dag: {}'.format(new_dag._graph))

        log.debug('topological sort: {}'.format(new_dag.topological_sort()))
        for func_name in new_dag.topological_sort():
            log.debug('execute function: {name}'.format(name=func_name))
            self._execute_function(func_name)

        # FIXME problem with saving arguments == self._null_value()
        if modified == set(self._funcs):
            # experiment was not running before
            # save ALL args and funcs in db
            self._storage.add_functions(
                exp_id,
                {
                    func_name: inspect.getsource(func_info[0])
                    for func_name, func_info in self._funcs.items()
                }
            )
            self._storage.add_arguments(exp_id, self._args)
        elif modified:
            # modified is set(...)
            # something was running
            # save ALL args and funcs in db
            self._storage.add_functions(
                exp_id,
                {
                    func_name: inspect.getsource(func_info[0])
                    for func_name, func_info in self._funcs.items()
                }
            )
            self._storage.add_arguments(exp_id, self._args)
        else:
            # modified is empty set
            # nothing was running
            # nothing to do here
            pass

        for metric in self.metrics:
            log.info('Metric {name}={value}'.format(
                name=metric, value=self._args[metric]
            ))

        log.info('{} seconds'.format(time() - start_time))

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
