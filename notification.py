import os
import sys
import config_local as cfg
import datetime
import fileinput
import re
import json
import copy
from src import helper, exportFile, birthday

tmpFolder = "tmp/"
configFileName = "config.py"
configFilePath = cfg.baseDir+tmpFolder+configFileName


def getDate():

    # read last run date or create config file
    lastDayString = helper.readConfigOrCreate(cfg,
                                              tmpFolder, configFilePath, "lastDay = ")

    try:
        return datetime.datetime.strptime(lastDayString, '%Y-%m-%d').date()
    except ValueError:
        print("wrong date - check the config file")
        return (helper.getToday() - datetime.timedelta(days=1))


def writeToConfig():
    content = open(configFilePath, "r").read()

    with open(configFilePath, "w") as f:
        f.write(re.sub(r"lastDay = \"(.*)\"",
                       "lastDay = \""+str(helper.getToday())+"\"", content))


def updateBirthdayLists():

    for module in cfg.modulesToUpateBeforeNotification:
        # get the linkedin birthdays of today
        if(len(module) > 0):
            try:
                os.system("cd "+cfg.baseDir+" | /usr/bin/python3 -m " +
                          cfg.scrappingModulesPath + "." + module)
            except:
                print("An exception occurred during execution of " +
                      module+" crawler ")


date = getDate()

if(date < helper.getToday()):

    updateBirthdayLists()
    exportFile.fillDailyBirthdayListFromExportFiles(cfg)
    writeToConfig()

sys.exit(0)
