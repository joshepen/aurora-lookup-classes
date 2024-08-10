import tkinter as tk
import tkinter.font
import os
from out.IOutput import IOutput
from out.OutputString import OutputString
from logic.AuroraLookupClasses import AuroraLookupClasses
from types import FunctionType

INPUT_DIR = "input/"
OUTPUT_DIR = "output/"


class TkGUI:
    def __init__(self, startFunction: FunctionType):
        self.startFunction = startFunction
        self.root = tk.Tk()
        self.root.title("AuroraLookupClasses")
        self.consolasFont = tk.font.Font(family="Consolas")
        self.__CreateWidgets()
        self.__PlaceWidgets()

    def Start(self):
        self.root.mainloop()

    def __CreateWidgets(self):
        self.inputBox = tk.Text(self.root, font=self.consolasFont, width=30, height=10)
        self.usernameLabel = tk.Label(
            self.root, text="User ID:", font=self.consolasFont
        )
        self.usernameEntry = tk.Entry(self.root, font=self.consolasFont)
        self.passwordLabel = tk.Label(
            self.root, text="Password:", font=self.consolasFont
        )
        self.passwordEntry = tk.Entry(self.root, show="*", font=self.consolasFont)

        self.semesterLabel = tk.Label(
            self.root, text="Semester:", font=self.consolasFont
        )
        self.semesterEntry = tk.Entry(self.root, font=self.consolasFont)

        self.outFilenameLabel = tk.Label(
            self.root, font=self.consolasFont, text="Out Filename (No extension)"
        )
        self.outFilenameEntry = tk.Entry(self.root, font=self.consolasFont)

        self.messageBar = tk.Entry(
            self.root,
            font=self.consolasFont,
        )
        self.messageBar.insert(0, "Enter course names in text box or txt filename.")
        self.messageBar.config(state=tk.DISABLED)

        self.startButton = tk.Button(
            self.root, text="Start", width=10, command=self.Lookup
        )

    def __PlaceWidgets(self):
        self.usernameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.usernameEntry.grid(row=0, column=1, padx=10, pady=10)

        self.passwordLabel.grid(row=1, column=0, padx=10, pady=10)
        self.passwordEntry.grid(row=1, column=1, padx=10, pady=10)

        self.semesterLabel.grid(row=2, column=0, padx=10, pady=10)
        self.semesterEntry.grid(row=2, column=1, padx=10, pady=10)

        self.outFilenameLabel.grid(row=3, column=0, padx=10, pady=10)
        self.outFilenameEntry.grid(row=3, column=1, padx=10, pady=10)

        self.inputBox.grid(row=0, column=2, rowspan=4, columnspan=1, padx=10, pady=10)

        self.messageBar.grid(
            row=4, column=0, columnspan=3, padx=10, pady=10, sticky="EW"
        )

        self.startButton.grid(row=0, column=3, rowspan=5, padx=10, pady=10, sticky="NS")

    def DisplayMessage(self, message: str):
        self.messageBar.config(state=tk.NORMAL)
        self.messageBar.delete(0, tk.END)
        self.messageBar.insert(0, message)
        self.messageBar.config(state=tk.DISABLED)

    def GetCourseNames(self):
        names = [
            name.strip()
            for name in self.inputBox.get("1.0", tk.END).split("\n")
            if name.strip() != ""
        ]
        if len(names) > 0:
            if names[0] in os.listdir(INPUT_DIR):
                with open(INPUT_DIR + names[0]) as file:
                    names = [name.strip() for name in file.readlines()]

        return names

    def Lookup(self):
        self.startFunction(
            self.usernameEntry.get(),
            self.passwordEntry.get(),
            self.semesterEntry.get(),
            self.GetCourseNames(),
            self.outFilenameEntry.get(),
        )
