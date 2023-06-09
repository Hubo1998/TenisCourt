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
            if newcourtreservation.startdate is None:
                return None

            if not self.check_user_reservations(newcourtreservation.name, newcourtreservation.startdate):
                return None

            busyhours = self.hours_of_reservations(newcourtreservation.startdate)
            if newcourtreservation.startdate in busyhours:
                originalstartdate: datetime = newcourtreservation.startdate
                newstartdateafter = originalstartdate
                newstartdatebefore = originalstartdate
                i = 1
                while newstartdateafter in busyhours and newstartdatebefore in busyhours:
                    if newstartdateafter.hour < 22:
                        newstartdateafter = originalstartdate + timedelta(minutes=30 * i)
                    if newstartdatebefore.hour > 7:
                        newstartdatebefore = originalstartdate - timedelta(minutes=30 * i)
                    i += 1
                if newstartdateafter not in busyhours:
                    newcourtreservation.startdate = newstartdateafter
                elif newstartdatebefore not in busyhours:
                    newcourtreservation.startdate = newstartdatebefore
                elif newstartdatebefore.hour > 7 and newstartdateafter.hour < 22:
                    print("Sorry but we have full occupancy to the end of the day, you can try another day")
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
        print(f"You have booked a court on {newcourtreservation.startdate.strftime('%d.%m.%Y %H:%M')}")

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
                print(f"You have canceled a reservation on "
                      f"{cancelcourtreservation.startdate.strftime('%d.%m.%Y %H:%M')}")
                return None
        print("Sorry but there is no reservation for you on specified date")

    def print_days_reservations(self, day: str, dateofreservation):
        print(f"{day}:")
        count = 0
        for reservation in self.reservations:
            if dateofreservation == reservation.startdate.date():
                print(reservation)
                count += 1
        if count == 0:
            print("No Reservations")
        print()

    def show_schedule(self):
        self.collect_dbdata()
        printdata = Export()
        printdata.input_time_period()
        if printdata.startdate is None or printdata.enddate is None:
            return None
        for i in range((printdata.enddate - printdata.startdate).days):
            dayofreservations = printdata.startdate.date() + timedelta(days=i)
            datenow = datetime.now().date()
            if dayofreservations == datenow:
                self.print_days_reservations("Today", dayofreservations)
            elif datenow + timedelta(days=1) >= dayofreservations > datenow:
                self.print_days_reservations("Tomorrow", dayofreservations)
            elif datenow > dayofreservations >= datenow - timedelta(days=1):
                self.print_days_reservations("Yesterday", dayofreservations)
            elif datenow + timedelta(days=7) > dayofreservations > datenow:
                self.print_days_reservations(dayofreservations.strftime('%A'), dayofreservations)
            else:
                self.print_days_reservations(dayofreservations.strftime('%Y-%m-%d'), dayofreservations)

    def save_schedule(self):
        self.collect_dbdata()
        exportdata = Export()
        exportdata.input_time_period()
        if exportdata.startdate is None or exportdata.enddate is None:
            return None
        exportdata.input_format()
        if exportdata.format is None:
            return None
        exportdata.input_filename()
        if exportdata.format == ".json":
            exportdata.prepare_json(self.reservations)
            exportdata.export_json(exportdata.jsondata)
        elif exportdata.format == ".csv":
            exportdata.prepare_csv(self.reservations)
            exportdata.export_csv(exportdata.csvdata)
        print(f"You saved a schedule to a {exportdata.filename + exportdata.format} file")
