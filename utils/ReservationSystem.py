from utils.CourtReservation import *
from utils.Database import Database
from utils.Export import Export


class ReservationSchedule:
    def __init__(self, database: Database):
        self.database = database
        self.reservations = []

    def collect_dbdata(self):
        self.reservations = []
        self.database.read_alldata()
        for row in self.database.cursor.fetchall():
            startdate = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            duration = timedelta(seconds=int(row[2]))
            self.reservations.append(CourtReservation(row[0], startdate, duration))

    def hours_of_reservations(self, reservationdate):
        reservationsofday = []
        reservedhours = []
        for i in range(len(self.reservations)):
            if self.reservations[i].startdate.day == reservationdate.day:
                reservationsofday.append(self.reservations[i])
        for reservation in reservationsofday:
            startdate = reservation.startdate
            for duration in range(int(reservation.duration / timedelta(minutes=30))):
                reservedhours.append(startdate)
                startdate += timedelta(minutes=30)
        return reservedhours

    def check_user_reservations(self, bookername, reservationdate):
        countofreservations = 0
        firstdayofweek = reservationdate - timedelta(days=reservationdate.weekday())
        lastdayofweek = reservationdate + timedelta(days=6 - reservationdate.weekday())
        for i in range(len(self.reservations)):
            if self.reservations[i].name == bookername:
                if firstdayofweek.date() <= self.reservations[i].startdate.date() <= lastdayofweek.date():
                    countofreservations += 1
        if countofreservations >= 2:
            print("You have already 2 reservations this week, choose another date.")
            return False
        return True

    def make_reservation(self):
        self.collect_dbdata()
        newcourtreservation = CourtReservation()

        newcourtreservation.input_name()
        if newcourtreservation.name is None:
            return None

        while True:
            newcourtreservation.input_date("book", "book a court")
            print(type(newcourtreservation.startdate))
            if newcourtreservation.startdate is None:
                return None

            if not self.check_user_reservations(newcourtreservation.name, newcourtreservation.startdate):
                return None

            busyhours = self.hours_of_reservations(newcourtreservation.startdate)
            if newcourtreservation.startdate in busyhours:
                while newcourtreservation.startdate in busyhours:
                    newcourtreservation.startdate = newcourtreservation.startdate + timedelta(minutes=30)
                if newcourtreservation.startdate.hour == 22:
                    print("Sorry but we have full occupancy to the end of the day, you can try earlier")
                    continue
                answerfornewdate = input(f"The time you chose is unavailable, would you like to make a reservation for "
                                         f"{newcourtreservation.startdate.strftime('%H:%M')} instead? (yes/no)\n")
                if answerfornewdate == "no":
                    continue
            break
        for i in range(len(busyhours)):
            busyhours[i] += timedelta(minutes=30)

        while True:
            newcourtreservation.input_duration()
            if newcourtreservation.duration is None:
                return None
            elif newcourtreservation.startdate + newcourtreservation.duration in busyhours:
                print("You need to choose shorter duration, because of next reservation")
                continue
            break

        self.database.insert_data(newcourtreservation)

    def cancel_reservation(self):
        self.collect_dbdata()
        cancelcourtreservation = CourtReservation()
        cancelcourtreservation.input_name()
        if cancelcourtreservation.name is None:
            return None
        cancelcourtreservation.input_date("cancel", "cancel a reservation")
        if cancelcourtreservation.startdate is None:
            return None
        for i in range(len(self.reservations)):
            if self.reservations[i].name == cancelcourtreservation.name and \
                    self.reservations[i].startdate == cancelcourtreservation.startdate:
                self.database.delete_data(cancelcourtreservation.name, cancelcourtreservation.startdate)
                return None
        print("Sorry but there is no reservation for you on specified date")

    def show_schedule(self):
        self.collect_dbdata()
        printdata = Export()
        printdata.input_time_period()
        for row in self.reservations:
            print(row)

    def save_schedule(self):
        self.collect_dbdata()
        exportdata = Export()
        exportdata.input_time_period()
        if exportdata.startdate and exportdata.enddate is None:
            return None
        exportdata.input_format()
        if exportdata.format is None:
            return None
        exportdata.input_filename()
        if exportdata.format == ".json":
            exportdata.export_json()
        elif exportdata.format == ".csv":
            exportdata.export_csv()
