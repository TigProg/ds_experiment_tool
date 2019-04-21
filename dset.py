import logging

from experiment_tool.utils import init_logger
from experiment_tool.runner import Runner


if __name__ == '__main__':
    init_logger(logging.INFO)
    log = logging.getLogger(__name__)
    log.info('Started')
    Runner('first_example', {'name': '1 2 3 2 31'}, ('result', )).run()
    log.info('Finished')
