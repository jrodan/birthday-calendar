import json
from dateutil import parser
import time
from src import helper
import datetime


class Birthday():

    def __init__(self, row, source):
        self.source = source
        self.row = row
        self.name = ""
        self.birthdayS = ""
        self.compareDates = helper.getCompareDates()
        self.birthdayDate = None
        self.parseRow()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def normalizeDate(self):

        if(len(self.birthdayS) < 7):
            self.birthdayDate = time.strptime(self.birthdayS, "%d.%m.")
        else:
            self.birthdayDate = time.strptime(self.birthdayS, "%d.%m.%Y")

    def getBirthdayDay(self):
        return self.birthdayDate.tm_yday

    def __repr__(self):
        return str(self.birthdayDate.tm_yday)+" "+self.name

    def parseRow(self):
        for compareDate in self.compareDates:
            if(self.row.find(compareDate) != -1):
                rowSplitted = self.row.replace("\n", "").split(";")
                self.name = rowSplitted[0]
                self.birthdayS = rowSplitted[1]
                self.normalizeDate()
                break
