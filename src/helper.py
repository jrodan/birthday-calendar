import datetime
import os


def getCompareDates():
    compareDates = []
    counter = 0
    today = getToday()
    while counter < 3:
        compareDates.append(str(today.day-counter)+"."+str(today.month)+".")
        compareDates.append("0"+str(today.day-counter)+"."+str(today.month))
        compareDates.append("0"+str(today.day-counter)+".0"+str(today.month))
        compareDates.append(str(today.day-counter)+".0"+str(today.month))
        counter += 1
    return compareDates


def getToday():
    return datetime.date.today()


def readConfigOrCreate(cfg, tmpFolder, configFilePath, finderText):
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
