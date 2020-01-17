import os
from os import listdir
from os.path import isfile, join
import config_local as cfg
import datetime
import fileinput
import re
import birthday
import json
import copy
import sys

exportFolder = "exports"
tmpFolder = "tmp/"
configFileName = "config.py"
configFilePath = cfg.baseDir+tmpFolder+configFileName
today = datetime.date.today()


def readConfigOrCreate(finderText):
    lastDayString = ""
    try:
        os.makedirs(cfg.baseDir+tmpFolder)
    except OSError as e:
        test = ""
    if(os.path.isfile(configFilePath)):
        lastDayString = open(configFilePath, "r").read()
        lastDayString = lastDayString.replace(
            finderText, "").replace("\"", "").replace("\n", "")
        if(lastDayString == ""):
            lastDayString = finderText+"\"\""
    else:
        open(configFilePath, "w").write(finderText+"\"\"")
    return lastDayString


def getDate():

    # read last run date or create config file
    lastDayString = readConfigOrCreate("lastDay = ")

    try:
        return datetime.datetime.strptime(lastDayString, '%Y-%m-%d').date()
    except ValueError:
        print("wrong date - check the config file")
        return (today - datetime.timedelta(days=1))


def getCompareDates():
    compareDates = []
    counter = 0
    while counter < 3:
        compareDates.append(str(today.day-counter)+"."+str(today.month)+".")
        compareDates.append("0"+str(today.day-counter)+"."+str(today.month))
        compareDates.append("0"+str(today.day-counter)+".0"+str(today.month))
        compareDates.append(str(today.day-counter)+".0"+str(today.month))
        counter += 1
    return compareDates


def handleExportFiles():
    files = [f for f in listdir(cfg.baseDir+exportFolder)
             if isfile(join(cfg.baseDir+exportFolder, f))]
    foundBirthdays = []
    compareDates = getCompareDates()

    print("checking for new birthdays today and the last 2 days")
    for fileName in files:
        f = open(cfg.baseDir+exportFolder+"/"+fileName, "r")
        for row in f:
            found = False
            for compareDate in compareDates:
                if(row.find(compareDate) != -1):
                    rowSplitted = row.replace("\n", "").split(";")
                    name = rowSplitted[0]
                    birthdayS = rowSplitted[1]
                    birthdayO = birthday.Birthday(name, birthdayS, fileName)
                    foundBirthdays.append(
                        birthdayO)
                    found = True
                    break
        f.close()

    return sorted(foundBirthdays,
                  key=lambda x: x.getBirthdayDay())


def notify(title, text):
    print(text)
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def writeTodaysBirthdayList(foundBirthdays):

    f = open(cfg.baseDir+"todaysBirthdayList.txt", "w")
    strRes = ""

    for birthdayL in foundBirthdays:
        strRes += str(birthdayL.birthdayDate.tm_yday) + "." + \
            str(birthdayL.birthdayDate.tm_mon) + \
            ". - "+str(birthdayL.name)+"\r\n"

    os.system(
        cfg.texteditorPath+" "+cfg.baseDir+"todaysBirthdayList.txt")

    f.write(strRes)
    f.close()


def writeToConfig():
    content = open(configFilePath, "r").read()

    with open(configFilePath, "w") as f:
        f.write(re.sub(r"lastDay = \"(.*)\"",
                       "lastDay = \""+str(today)+"\"", content))


date = getDate()

if(date < today):
    foundBirthdays = handleExportFiles()
    print(foundBirthdays)
    writeTodaysBirthdayList(foundBirthdays)
    writeToConfig()

sys.exit(0)
