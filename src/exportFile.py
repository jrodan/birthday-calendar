from src import helper, birthday
from os import listdir
from os.path import isfile, join
import os


def fillDailyBirthdayListFromExportFiles(cfg):
    bList = handleExportFiles(cfg)
    writeTodaysBirthdayListHtml(cfg, bList)
    print(bList)


def handleExportFiles(cfg):
    files = [f for f in listdir(cfg.baseDir+cfg.exportFolder)
             if isfile(join(cfg.baseDir+cfg.exportFolder, f))]
    birthdayLists = []
    birthdays = []

    print("checking for new birthdays today and the last 2 days")
    for fileName in files:
        exportFileO = ExportFile(fileName, cfg)
        birthdayLists.append(exportFileO)
        birthdays = birthdays + exportFileO.birthdays

    # return birthdays
    return sorted(birthdays,
                  key=lambda x: x.getBirthdayDay())


def writeTodaysBirthdayList(cfg, foundBirthdays):

    f = open(cfg.baseDir+"todaysBirthdayList.txt", "w")
    strRes = ""

    for birthdayL in foundBirthdays:
        strRes += str(birthdayL.birthdayDate.tm_yday) + "." + \
            str(birthdayL.birthdayDate.tm_mon) + \
            ". - "+str(birthdayL.name) + " - " + str(birthdayL.source.replace("-extract.txt", "")) + \
            "\r\n"

    os.system(
        cfg.texteditorPath+" "+cfg.baseDir+"todaysBirthdayList.txt")

    f.write(strRes)
    f.close()


def writeTodaysBirthdayListHtml(cfg, foundBirthdays):

    # read template file
    f = open(cfg.baseDir+"setup/birthdayListTemplate.html", "r")
    template = f.read()
    f.close()

    # read template row
    f = open(cfg.baseDir+"setup/birthdayListTemplateRow.html", "r")
    templateRow = f.read()
    f.close()

    strRes = ""

    for birthdayL in foundBirthdays:
        row = templateRow.replace("<!-- PLACEHOLDER_DAY -->", str(birthdayL.birthdayDate.tm_yday) + "." +
                                  str(birthdayL.birthdayDate.tm_mon) +
                                  ".")
        row = row.replace("<!-- PLACEHOLDER_NAME -->", str(birthdayL.name))
        row = row.replace("<!-- PLACEHOLDER_SOURCE -->",
                          str(birthdayL.source.replace("-extract.txt", "")))

        strRes += row

    resultFile = template.replace("<!-- PLACEHOLDER_BIRTHDAYS -->", strRes)

    f = open(cfg.baseDir+"todaysBirthdayList.html", "w")
    f.write(resultFile)
    f.close()

    os.system(
        cfg.browserPath+" "+cfg.baseDir+"todaysBirthdayList.html")


class ExportFile():

    def __init__(self, fileName, cfg):
        self.fileName = fileName
        self.cfg = cfg
        self.birthdays = list()
        self.parseBirthdays()

    def parseBirthdays(self):
        f = open(self.cfg.baseDir+self.cfg.exportFolder+"/"+self.fileName, "r")
        for row in f:
            birthdayO = birthday.Birthday(row, self.fileName)
            if(birthdayO != None and birthdayO.birthdayDate != None):
                self.birthdays.append(birthdayO)
        f.close()
