from out.IOutput import IOutput
from objects.Course import Course
import os
from tabulate import tabulate
import itertools


class OutputString(IOutput):

    @staticmethod
    def output(data: list[Course], filepath: str = None) -> str:
        string = ""
        for course in data:
            string += f"{course.GetFullName()}\n{course.GetDescription()}\n"
            if len(course) > 0:
                string += tabulate(
                    itertools.chain.from_iterable(course.GetSections()),
                    headers=course.GetHeaders(),
                )
            string += "\n\n"

        if filepath != None:
            if not os.path.exists(filepath[: filepath.rfind("/")]):
                os.mkdir(filepath[: filepath.rfind("/")])
            with open(filepath + ".txt", "w") as file:
                file.write(string)

        return string
