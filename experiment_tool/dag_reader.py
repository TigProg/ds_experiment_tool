import importlib
import logging
import os
import sys
from typing import Callable, Dict, List, Set, Tuple

from experiment_tool.dag import DAG

log = logging.getLogger(__name__)


def get_experiment(experiment_name: str, package: str = 'experiments') \
        -> Dict[Callable, List]:
    """
    Get hardcoded experiment
    :param experiment_name:
    :param: package:
    :return: functions with arguments
    """
    path = sys.path
    path_to_exp = '{path}/{package}'.format(
        path=os.getcwd(), package=package
    )
    sys.path.insert(0, path_to_exp)
    try:
        module = importlib.import_module(experiment_name)
        log.debug('module with experiment successfully loaded')
        experiment = module.__dict__['experiment']
        log.debug('experiment successfully loaded')
        return experiment
    except ModuleNotFoundError:
        log.error('module  with experiment failed to load')
        raise
    except KeyError:
        log.error('experiment failed to load')
        raise
    finally:
        sys.path = path


def example_reader(experiment_name: str) \
        -> Tuple[DAG, Dict[str, List], Set[str]]:
    """
    Get experiment by name
    :return: dag, functions, arguments
    """
    # get data
    _func = get_experiment(experiment_name)

    # functions
    functions = {
        key.__name__: [key, value[0], value[1]]
        for key, value in _func.items()
    }

    # arguments
    arguments = set()
    for in_args, out_args in _func.values():
        arguments.update(in_args)
        arguments.update(out_args)

    # dag
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
