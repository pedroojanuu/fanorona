from abc import ABC, abstractmethod
from copy import deepcopy

class Move(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def __eq__(self, __value: object) -> bool:
        pass

    @abstractmethod
    def allows_multiple_moves(self) -> bool:
        pass

    @abstractmethod
    def execute(self, state):
        pass

    @staticmethod
    def execute_decorator(func):
        """
        Execute functions that change the state should be decorated with this function.

        To prevent copying twice, it should only be used in the final classes (not the abstract classes).
        """
        def wrapper(self, const_state):
            state_copy = deepcopy(const_state)
            return func(self, state_copy)
        return wrapper

