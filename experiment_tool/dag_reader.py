import importlib
import logging
import os
import sys
from typing import Callable, Dict, List, Set, Tuple

from experiment_tool.dag import DAG

log = logging.getLogger(__name__)


def get_experiment(experiment_path: str) -> Dict[Callable, List]:
    """
    Get experiment from python file
    :param experiment_path:
    :return: functions with arguments
    """
    exp_path, exp_file = os.path.split(experiment_path)
    exp_module, _ = os.path.splitext(exp_file)

    saved_path = sys.path
    sys.path.insert(0, exp_path)
    try:
        module = importlib.import_module(exp_module)
        log.debug('module with experiment successfully loaded')
        experiment = module.experiment
        log.debug('experiment successfully loaded')
        return experiment
    except ModuleNotFoundError:
        log.error('module %s with experiment failed to load', exp_module)
        raise
    except KeyError:
        log.error('experiment from module %s failed to load', exp_module)
        raise
    finally:
        sys.path = saved_path


def example_reader(experiment_name: str) \
        -> Tuple[DAG, Dict[str, List], Set[str]]:
    """
    Get experiment by name
    :return: dag, functions, arguments
    """
    _func = get_experiment(experiment_name)

    functions = {
        key.__name__: [key, value[0], value[1]]
        for key, value in _func.items()
    }

    arguments = set()
    for in_args, out_args in _func.values():
        arguments.update(in_args)
        arguments.update(out_args)

    vertices = [
        key.__name__ for key in _func
    ]
    edges = []
    for start_edge, start_args in _func.items():
        for end_edge, end_args in _func.items():
            if set(start_args[1]).intersection(end_args[0]):
                edges.append((start_edge.__name__, end_edge.__name__))

    dag = DAG(vertices, edges)

    return dag, functions, arguments
