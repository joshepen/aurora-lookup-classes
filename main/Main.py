from logic.AuroraLookupClasses import AuroraLookupClasses
from ui.TkGUI import TkGUI
from out.OutputString import OutputString
from out.OutputExcel import OutputExcel
import threading

OUTPUT_DIR = "output/"
# Edit the below line to change the output method
OUTPUT_FUNCTION = OutputString.output
# Set this to false if the program is having issues to determine where it's getting caught up.
IS_HEADLESS = True


def main():
    global alu
    alu = AuroraLookupClasses()
    ui = TkGUI(startFunction)
    alu.SetUI(ui)

    ui.Start()


def startFunction(username, password, semester, courses, outFile):
    global alu
    thread = threading.Thread(
        target=lambda: alu.LookupClasses(
            username,
            password,
            semester,
            courses,
            OUTPUT_FUNCTION,
            OUTPUT_DIR + outFile,
            headless=IS_HEADLESS,
        )
    )
    thread.start()


if __name__ == "__main__":
    main()
