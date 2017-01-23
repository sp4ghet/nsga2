from nsga2.interfaces.iproblem import IProblem
from abc import ABCMeta, abstractmethod
from typing import Generator, Tuple
import numpy as np


class IOptimizer(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def call(iproblem: IProblem, epochs: int, agent_count: int) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        pass

