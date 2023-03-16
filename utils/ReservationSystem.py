from utils.CourtReservation import *
from utils.Database import Database


class ReservationSchedule:
    def __init__(self, database: Database):
        self.database = database
        self.reservations = []

    def collect_dbdata(self):
        self.reservations = []
        self.database.read_alldata()
        for row in self.database.cursor.fetchall():
            startdate = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            enddate = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
            self.reservations.append(CourtReservation(row[0], row[1], startdate, enddate))

    def hours_of_reservations(self, reservationdate):
        reservationsofday = []
        reserverdhours = []
        for i in range(len(self.reservations)):
            if self.reservations[i].startdate.day == reservationdate.day:
                reservationsofday.append(self.reservations[i])
        for reservation in reservationsofday:
            startdate = reservation.startdate
            while startdate < reservation.enddate:
                reserverdhours.append(startdate)
                startdate = startdate + timedelta(minutes=30)
        return reserverdhours

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

        bookername = input_name()
        if bookername is None:
            return None

        while True:
            reservationdate = input_date("book", "book a court")
            if reservationdate is None:
                return None

            if not self.check_user_reservations(bookername, reservationdate):
                return None

            busyhours = self.hours_of_reservations(reservationdate)
            if reservationdate in busyhours:
                while reservationdate in busyhours:
                    reservationdate = reservationdate + timedelta(minutes=30)
                if reservationdate.hour == 22:
                    print("Sorry but we have full occupancy to the end of the day, you can try earlier")
                    continue
                answerfornewdate = input(f"The time you chose is unavailable, would you like to make a reservation for "
                                         f"{reservationdate.strftime('%H:%M')} instead? (yes/no)")
                if answerfornewdate == "no":
                    continue
            break
        for i in range(len(busyhours)):
            busyhours[i] += timedelta(minutes=30)
        while True:
            reservationduration = input_duration()
            if reservationduration is None:
                return None
            elif reservationdate + reservationduration in busyhours:
                print("You need to choose shorter duration, because of next reservation")
                continue
            break

        self.database.insert_data(CourtReservation(None,
                                                   bookername, reservationdate, reservationdate + reservationduration))

    def cancel_reservation(self):
        self.collect_dbdata()
        bookername = input_name()
        if bookername is None:
            return None
        reservationdate = input_date("cancel", "cancel a reservation")
        if reservationdate is None:
            return None
        for i in range(len(self.reservations)):
            if self.reservations[i].name == bookername and self.reservations[i].startdate == reservationdate:
                self.database.delete_data(bookername, reservationdate)
                return None
        print("Sorry but there is no reservation for you on specified date")

    def show_schedule(self):
        self.collect_dbdata()
        for row in self.reservations:
            print(row)
