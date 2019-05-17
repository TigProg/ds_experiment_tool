import argparse
import logging
from typing import Any, Callable


__version__ = '0.0.1'

log = logging.getLogger(__name__)


def init_logger(debug_level: int = logging.INFO) -> None:
    logging.basicConfig(
        format='%(asctime)-24s %(levelname)-9s %(name)-37s %(message)s',
        level=debug_level,
    )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='Data Scientist Experiment Tool',
    )
    parser.add_argument(
        '-p', '--path',
        required=True, nargs=1, type=argparse.FileType(),
        help='path to python file with experiment',
    )
    parser.add_argument(
        '-v', '--variables',
        required=True, action='append', type=lambda pair: pair.split("="),
        help='mapping external experiment variable name to string-value '
             '(separated by equality sign, '
             'for multiple variables use repeated command line argument)',
    )
    # parser.add_argument(
    #     '-v', '--variables',
    #     required=True, nargs=1, type=str,
    #     help='mapping external experiment variable names to values in json '
    #          '(with single quotes and without spaces)',
    # )
    parser.add_argument(
        '-m', '--metric',
        required=True, nargs='+', type=str,
        help='required metric(s)',
    )
    parser.add_argument(
        '--multiprocessing',
        action='store_true',
        help='use multiple processes',
    )
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='show debug messages',
    )
    parser.add_argument(
        '-V', '--version',
        action='version', version='%(prog)s {}'.format(__version__),
        help='show version and exit',
    )
    return parser


class Maybe:
    def __init__(self, obj: Any = None, nothing: bool = False):
        self._obj = obj
        self._nothing = nothing

    def is_nothing(self) -> bool:
        return self._nothing

    def is_just(self) -> bool:
        return not self.is_nothing()

    def unpack(self) -> Any:
        if self.is_just():
            return self._obj
        log.error('this Maybe is Nothing')
        raise TypeError('this Maybe is Nothing')


def encrypt_str(string: str, encryption_func: Callable):
    return encryption_func(string.encode()).hexdigest()
