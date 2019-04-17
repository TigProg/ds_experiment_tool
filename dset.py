import logging

log = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)-24s %(levelname)-9s %(name)-37s %(message)s',
    level=logging.INFO,
)

from experiment_tool.runner import Runner


if __name__ == '__main__':
    log.info('Started')
    Runner('first_example', {'name': '1 2 3 2 31'}, ('result', )).run()
    log.info('Finished')
