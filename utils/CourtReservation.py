from datetime import datetime, timedelta


class CourtReservation:
    def __init__(self, id, name, startdate, enddate):
        self.id = id
        self.name = name
        self.startdate = startdate
        self.enddate = enddate

    def __str__(self):
        return f'* {self.name} {self.startdate} - {self.enddate}'


def input_name():
    while True:
        bookerinputname = input("What's your Name?\n")
        if bookerinputname == "exit":
            return None
        elif 40 > len(bookerinputname) >= 3:
            bookername = bookerinputname.title()
            break
        else:
            print("Try input your name again")
    return bookername


def input_date(inputprompt, validationprompt):
    while True:
        reservationinputdate = input(f"When would you like to {inputprompt} a reservation? (DD.MM.YYYY HH:MM)\n")
        try:
            reservationdate = datetime.strptime(reservationinputdate, '%d.%m.%Y %H:%M')
            if reservationdate - datetime.now() < timedelta(hours=1):
                print(f"There must be at least an hour to {validationprompt}")
                if inputprompt == "make":
                    raise ValueError
                elif inputprompt == "cancel":
                    return None
            elif reservationdate.minute != 0 and reservationdate.minute != 30:
                print(f"You can {validationprompt} only on HH:00 or HH:30")
                raise ValueError
            elif reservationdate.hour < 8 or reservationdate.hour > 21:
                print(f"You can {validationprompt} only from 8:00 to 21:30")
                raise ValueError
            else:
                break
        except ValueError:
            if reservationinputdate == "exit":
                return None
            print("Wrong date format, try input again")
    return reservationdate


def input_duration():
    while True:
        reservationinputduration = input(
            "How long would you like to book court?\n1. 30 Minutes\n2. 60 Minutes\n3. 90 Minutes\n")
        if reservationinputduration.startswith("30") or reservationinputduration == "1":
            reservationtduration = timedelta(minutes=30)
            break
        elif reservationinputduration.startswith("60") or reservationinputduration == "2":
            reservationtduration = timedelta(minutes=60)
            break
        elif reservationinputduration.startswith("90") or reservationinputduration == "3":
            reservationtduration = timedelta(minutes=90)
            break
        elif reservationinputduration.startswith("exit"):
            return None
        else:
            print("Wrong duration of reservation, try again")
    return reservationtduration
