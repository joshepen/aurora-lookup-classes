from bs4 import BeautifulSoup
from auroranav.AuroraNav import AuroraNav
import os
from objects.Course import Course
from out.OutputExcel import OutputExcel
from out.OutputString import OutputString

INPUT_DIR = "input/"
OUTPUT_DIR = "output/"


def main():
    i = 1
    files = os.listdir(INPUT_DIR)
    filename = "courses%d.txt" % i
    while filename in files:
        LookupClasses(INPUT_DIR + filename)
        i += 1
        filename = "courses%d.txt" % i


def LookupClasses(filename):
    semester = GetSemester(filename)
    names = GetClassNames(filename)
    userID = GetUserID(filename)
    password = GetPassword(filename)

    nav = AuroraNav()
    nav.OpenAurora()
    nav.Login(userID, password)
    data = []
    for name in names:
        currCourse = GetClassInfo(nav, semester, name)
        if len(currCourse) > 0:
            data.append(currCourse)

    nav.CloseWindow()

    OutputString.output(data, f"{OUTPUT_DIR+semester}.txt")


def GetUserID(filepath):
    userIDIndex = 0
    with open(filepath, "r") as file:
        return file.readlines()[userIDIndex].strip()


def GetPassword(filepath):
    passwordIndex = 1
    with open(filepath, "r") as file:
        return file.readlines()[passwordIndex].strip()


def GetCatalogInfo(nav: AuroraNav, semester, courseName):
    nav.HomePage()
    nav.GoToPage("Enrolment & Academic Records")
    nav.GoToPage("Registration and Exams")
    nav.GoToPage("Course Catalog")

    nav.SelectTerm(semester)
    nav.SelectDepartment(courseName.split(" ")[0])
    if nav.GoToPage(courseName, elementType="a"):
        return ProcessCatalogPage(
            BeautifulSoup(nav.GetPageContents(), features="html.parser")
        )
    return None


def GetLUCInfo(nav: AuroraNav, semester, name):
    nav.HomePage()
    nav.GoToPage("Enrolment & Academic Records")
    nav.GoToPage("Registration and Exams")
    nav.GoToPage("Look Up Classes")

    nav.SelectTerm(semester)
    nav.SelectDepartment(name.split(" ")[0])
    if nav.GoToLookupClass(name.split(" ")[1]):
        content = BeautifulSoup(nav.GetPageContents(), features="html.parser")
        content = ProcessLUCPage(content)
        return content
    return {"sections": [], "headers": []}


def GetSemester(filename):
    semesterIndex = 2
    with open(filename, "r") as file:
        return file.readlines()[semesterIndex].strip()


def GetClassNames(filename):
    classesIndex = 3
    names = []
    with open(filename, "r") as file:
        for line in file.readlines()[classesIndex:]:
            names.append(line.strip())
    return names


def ProcessLUCPage(pageContents: BeautifulSoup):
    table = pageContents.find("table", class_="datadisplaytable").tbody

    data = []
    wantedColumns = GetWantedColumnIndices(table.contents[2])

    currSection = {}
    for name in wantedColumns:
        currSection[name] = []

    for trIndex in range(3, len(table.contents)):
        if (
            table.contents[trIndex] != "\n"
            and table.contents[trIndex].find("b") == None
            and table.contents[trIndex].find("hr") == None
        ):
            for columnName in wantedColumns:
                columnIndex = wantedColumns[columnName]
                value = table.contents[trIndex].contents[columnIndex].get_text()
                if value != None:
                    value = value.replace("\xa0", "")
                currSection[columnName].append(value)

        elif table.contents[trIndex].find("hr") not in [None, -1]:
            # transpose data for easier processing
            currSection = [
                [row[i] for row in list(currSection.values())]
                for i in range(len(list(currSection.values())[0]))
            ]
            data.append(currSection)
            currSection = {}
            for name in wantedColumns:
                currSection[name] = []

    return {"sections": data, "headers": list(wantedColumns.keys())}


def ProcessCatalogPage(page: BeautifulSoup):
    return {
        "name": page.find("td", class_="nttitle").get_text(),
        "description": page.find("td", class_="ntdefault").get_text(),
    }


def GetWantedColumnIndices(headerRow: BeautifulSoup):
    wantedColumns = [
        "CRN",
        "Sec",
        "Cmp",
        "Title",
        "Days",
        "Time",
        "Instructor",
        "Date",
        "Rem",
        "WL Act",
    ]
    wantedIndices = {}
    for i in range(len(headerRow.contents)):
        for name in wantedColumns:
            if name in headerRow.contents[i].get_text():
                wantedIndices[headerRow.contents[i].get_text()] = i

    return wantedIndices


def GetClassInfo(nav: AuroraNav, semester, name):
    course = Course(name.strip())
    lookupData = GetLUCInfo(nav, semester, name)
    course.AddSections(lookupData["sections"])
    course.SetHeaders(lookupData["headers"])
    if len(course) > 0:
        catalogInfo = GetCatalogInfo(nav, semester, name)
        description = catalogInfo["description"]
        course.SetFullName(catalogInfo["name"].strip())

        # decrease the amount of whitespace
        description = description.replace("\n\n", "\n")
        description = description.replace("\n\n", "\n")
        if "Restrictions" in description:
            description = description[: description.find("Restrictions")]
        description = description.strip()
        course.SetDescription(description)
    return course


if __name__ == "__main__":
    main()
