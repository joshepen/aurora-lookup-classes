from abc import ABC, abstractmethod
from objects.Course import Course


class IOutput(ABC):

    @staticmethod
    @abstractmethod
    def output(course: Course, filepath: str = None):
        pass

    @abstractmethod
    def test(self):
        pass
