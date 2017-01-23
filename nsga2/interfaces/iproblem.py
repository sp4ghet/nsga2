from abc import ABCMeta, abstractmethod
import numpy as np
from typing import Tuple


class IProblem(metaclass=ABCMeta):

    @property
    def bounds(self) -> np.ndarray:
        pass

    @property
    def dimensions(self) -> int:
        pass

    @staticmethod
    @abstractmethod
    def fitness(X: np.ndarray) -> Tuple[np.ndarray, ...]:
        pass

    @staticmethod
    @abstractmethod
    def perfect_pareto_front() -> np.ndarray:
        raise NotImplementedError

