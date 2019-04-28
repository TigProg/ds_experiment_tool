import logging
from abc import ABC, abstractmethod
from typing import Any, Iterable, Iterator


log = logging.getLogger(__name__)


class AbstractScope(ABC):
    @abstractmethod
    def __init__(self, var_names: Iterable[str]) -> None:
        """Create scope with undefined variables"""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Get number of defined variables"""
        pass

    @abstractmethod
    def __getitem__(self, item: str) -> Any:
        """Get the value of defined variable by name"""
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: Any) -> None:
        """Set the value of undefined variable"""
        pass

    @abstractmethod
    def __iter__(self) -> Iterator:
        """Get iterator on defined variables"""
        pass

    @abstractmethod
    def __contains__(self, item: str) -> bool:
        """Check if variable is defined"""
        pass


class MemoryScope(AbstractScope):
    def __init__(self, var_names: Iterable[str]) -> None:
        self._defined = dict()
        self._undefined = set(var_names)

    def __len__(self) -> int:
        return len(self._defined)

    def __getitem__(self, item: str) -> Any:
        if not isinstance(item, str):
            log.error('variable identifier must be a string')
            raise TypeError('variable identifier must be a string')
        if item not in self._defined:
            log.error("variable '%s' not defined", item)
            raise KeyError("variable '{}' not defined".format(item))
        return self._defined[item]

    def __setitem__(self, key: str, value: Any) -> None:
        if not isinstance(key, str):
            log.error('variable identifier must be a string')
            raise TypeError('variable identifier must be a string')
        if key not in self._undefined:
            log.error("variable '%s' not defined", key)
            raise KeyError("variable '{}' not found".format(key))
        self._undefined.remove(key)
        self._defined[key] = value

    def __iter__(self) -> Iterator:
        return iter(self._defined)

    def __contains__(self, item: str) -> bool:
        return item in self._defined
