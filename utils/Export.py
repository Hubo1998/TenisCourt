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
        self.jsondata = None
        self.csvdata = None

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
                    return None
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
                    return None
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
                self.file = open(self.filename + self.format, 'w')
                break
            print("Try again")

    def prepare_csv(self, listofreservations):
        csvdata = []
        for reservation in listofreservations:
            if self.startdate < reservation.startdate < self.enddate:
                starttime = datetime.strftime(reservation.startdate, '%d.%m.%Y %H:%M')
                endtime = datetime.strftime(reservation.startdate + reservation.duration, '%d.%m.%Y %H:%M')
                onereservation = [reservation.name, starttime, endtime]
                csvdata.append(onereservation)
        print(csvdata)
        self.csvdata = csvdata

    def export_csv(self, csv_rowslist):
        with self.file:
            writer = csv.writer(self.file)
            writer.writerow(["name", "start_time", "end_time"])
            writer.writerows(csv_rowslist)

    def prepare_json(self, listofreservations):
        jsondata = {}
        for i in range((self.enddate - self.startdate).days):
            dateofres = self.startdate + timedelta(days=i)
            reservationsofday = []
            for reservation in listofreservations:
                if self.startdate < reservation.startdate < self.enddate and \
                        reservation.startdate.date() == dateofres.date():
                    starttime = datetime.strftime(reservation.startdate, '%H:%M')
                    endtime = datetime.strftime(reservation.startdate + reservation.duration, '%H:%M')
                    oneres = {"name": f"{reservation.name}", "start_time": f"{starttime}", "end_time": f"{endtime}"}
                    reservationsofday.append(oneres)
            jsondata[datetime.strftime(dateofres, '%d.%m')] = reservationsofday
        self.jsondata = jsondata

    def export_json(self, json_rowslist):
        with self.file:
            json.dump(json_rowslist, self.file, indent=0)
