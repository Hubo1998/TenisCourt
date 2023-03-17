import csv
import json
from datetime import datetime, timedelta


class Export:
    def __init__(self, filename=None, startdate=None, enddate=None):
        self.filename = filename
        self.file = None
        self.startdate = startdate
        self.enddate = enddate
        self.format = None

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def input_time_period(self):
        while True:
            startinputdate = input("Input a start date. (DD.MM.YYY)\n")
            try:
                self.startdate = datetime.strptime(startinputdate, '%d.%m.%Y')
                break
            except ValueError:
                if startinputdate == "exit":
                    break
                print("Wrong date format, try input again")
        while True:
            endinputdate = input("Input an end date. (DD.MM.YYYY)\n")
            try:
                enddate = datetime.strptime(endinputdate, '%d.%m.%Y')
                if enddate >= self.startdate:
                    self.enddate = enddate
                else:
                    print("End date must be after start date.")
                    continue
                break
            except ValueError:
                if endinputdate == "exit":
                    break
                print("Wrong date format, try input again")

    def input_format(self):
        while True:
            fileformatinput = input("What file format you choose?\n1. JSON\n2. CSV\n").lower()
            if fileformatinput.startswith("jso") or fileformatinput == "1":
                self.format = ".json"
                break
            elif fileformatinput.startswith("cs") or fileformatinput == "2":
                self.format = ".csv"
                break
            elif fileformatinput == "exit":
                break
            print("Wrong file format, input again.")

    def input_filename(self):
        while True:
            filenameinput = input("Input name of file that you want to export data to:\n")

            if len(filenameinput) > 0 and filenameinput.isascii():
                self.filename = filenameinput
                self.file = open(self.filename, 'w')
                break
            print("Try again")

    def export_csv(self, csv_rowslist):
        with self.file:
            writer = csv.writer(self.file)
            writer.writerows(csv_rowslist)

    def export_json(self, json_rowslist):
        with self.file:
            json.dump(json_rowslist, self.file)
