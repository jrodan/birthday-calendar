import json
from dateutil import parser
import time


class Birthday():

    name = ""
    birthdayDate = ""
    source = ""

    def __init__(self, name, birthdayDate, source):

        self.name = name
        self.birthdayDate = self.normalizeDate(birthdayDate)
        self.source = source

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def normalizeDate(self, birthdayDate):

        if(len(birthdayDate) < 7):
            birthdayDateModified = time.strptime(birthdayDate, "%d.%m.")
        else:
            birthdayDateModified = time.strptime(birthdayDate, "%d.%m.%Y")

        return birthdayDateModified

    def getBirthdayDay(self):
        return self.birthdayDate.tm_yday

    def __repr__(self):
        return str(self.birthdayDate.tm_yday)+" "+self.name
