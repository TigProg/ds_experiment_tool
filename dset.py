import logging

from experiment_tool.utils import init_logger, create_parser
from experiment_tool.runner import Runner


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    if args.debug:
        init_logger(logging.DEBUG)
    else:
        init_logger(logging.INFO)

    log = logging.getLogger(__name__)

    log.info('Started')

    runner = Runner(
        args.path[0].name,
        dict(args.variables),
        args.metric,
        args.multiprocessing
    )
    runner.run()

    log.info('Finished')
