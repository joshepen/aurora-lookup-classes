from logic.AuroraLookupClasses import AuroraLookupClasses
from ui.TkGUI import TkGUI
from out.OutputString import OutputString


def main():
    alu = AuroraLookupClasses()
    ui = TkGUI(alu)
    alu.SetUI(ui)

    ui.Start()


if __name__ == "__main__":
    main()
