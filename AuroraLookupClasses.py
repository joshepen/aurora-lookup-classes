from bs4 import BeautifulSoup
from auroranav.AuroraNav import AuroraNav
import os
import threading


class CourseInfo:
    def __init__(self):
        pass


def main():
    semester = GetSemester("courses.txt")

    names = GetClassNames("courses.txt")

    nav = AuroraNav()
    nav.OpenAurora()
    nav.Login(os.getenv("AURORA_USER"), os.getenv("AURORA_PASS"))
    for name in names:

        # x = threading.Thread(target=GetClassInfo, args=(semester, name))
        # x.start()
        GetClassInfo(nav, semester, name)
    nav.CloseWindow()


def GetCatalogInfo(nav: AuroraNav, semester, courseName):
    nav.HomePage()
    nav.GoToPage("Enrolment & Academic Records")
    nav.GoToPage("Registration and Exams")
    nav.GoToPage("Course Catalog")

    nav.SelectTerm(semester)
    nav.SelectDepartment(courseName.split(" ")[0])
    nav.GoToPage(courseName)
    return nav.GetPageContents()


def GetLUInfo(nav: AuroraNav, semester, name):
    nav.HomePage()
    nav.GoToPage("Enrolment & Academic Records")
    nav.GoToPage("Registration and Exams")
    nav.GoToPage("Look Up Classes")

    nav.SelectTerm(semester)
    nav.SelectDepartment(name.split(" ")[0])
    nav.GoToLookupClass(name.split(" ")[1])

    content = BeautifulSoup(nav.GetPageContents(), features="html.parser")
    content = ProcessCourseInfoPage(content)
    return content


def GetSemester(filename):
    with open(filename, "r") as file:
        return file.readline().strip()


def GetClassNames(filename):
    names = []
    with open(filename, "r") as file:
        for line in file.readlines()[1:]:
            names.append(line.strip())
    return names


def ProcessCourseInfoPage(pageContents: BeautifulSoup):
    table = pageContents.find("table", class_="datadisplaytable")
    GetLUTableData(table)


def GetLUTableData(table: BeautifulSoup):
    tbl = table.tbody
    data = []
    wantedColumns = GetWantedColumnIndices(tbl.contents[2])


def GetWantedColumnIndices(headerRow: BeautifulSoup):
    wantedColumns = [
        "CRN,",
        "Sec",
        "Cmp",
        "Title",
        "Days",
        "Time",
        "Instructor",
        "Date (MM/DD)",
    ]
    wantedIndices = {}
    for i in range(len(headerRow.contents)):
        print(headerRow.contents[i].string)
        if headerRow.contents[i].string in wantedColumns:
            wantedIndices[headerRow.contents[i].string] = i

    return wantedIndices


def GetClassInfo(nav: AuroraNav, semester, name):

    description = GetCatalogInfo(nav, semester, name)
    table = GetLUInfo(nav, semester, name)


main()
