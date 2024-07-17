import tkinter as tk
import tkinter.font


class TkGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AuroraLookupClasses")
        self.consolasFont = tk.font.Font(family="Consolas")
        self.CreateWidgets()
        self.PlaceWidgets()

    def Start(self):
        self.root.mainloop()

    def CreateWidgets(self):
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

        self.startButton = tk.Button(self.root, text="Start", width=10)

    def PlaceWidgets(self):
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
        self.messageBar.config(state=tk.ACTIVE)
        self.messageBar.delete(0, tk.END)
        self.messageBar.insert(0, message)
        self.messageBar.config(state=tk.DISABLED)
