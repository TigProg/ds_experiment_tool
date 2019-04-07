from abc import abstractmethod
from typing import Any, Dict, List


class ExperimentStorage:
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_experiment_ids(self, exp_name: str, structure: str) -> List[int]:
        pass

    @abstractmethod
    def add_experiment(self, exp_name: str, structure: str) -> int:
        pass

    @abstractmethod
    def get_experiment_functions(self, exp_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def add_experiment_functions(self,
                                 exp_id: int,
                                 funcs: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_experiment_arguments(self, exp_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    def add_experiment_arguments(self,
                                 exp_id: int,
                                 args: Dict[str, Any]) -> None:
        pass

    # TODO: maybe for DSET-3
    # @abstractmethod
    # def get_all_experiments(self, exp_name: str) -> List[int]:
    #     pass
