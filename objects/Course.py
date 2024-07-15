class Course:
    def __init__(self, name):
        self.name = name
        self.sections = []

    def __len__(self):
        return len(self.sections)

    def SetDescription(self, description):
        self.description = description

    def AddSection(self, section: dict):
        self.sections.append(section)

    def AddSections(self, sections: list):
        self.sections += sections

    def SetHeaders(self, headers: list):
        self.headers = headers

    def GetHeaders(self):
        return self.headers

    def GetName(self):
        return self.name

    def GetDescription(self):
        return self.description

    def GetSections(self):
        return self.sections
