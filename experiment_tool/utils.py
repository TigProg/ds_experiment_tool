import logging
from typing import Any


log = logging.getLogger(__name__)


def init_logger(debug_level: int = logging.INFO) -> None:
    logging.basicConfig(
        format='%(asctime)-24s %(levelname)-9s %(name)-37s %(message)s',
        level=debug_level,
    )


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
