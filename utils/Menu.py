from utils.ReservationSystem import ReservationSchedule
from utils.Database import Database


class Menu:
    def __init__(self, database: Database):
        self.database = database
        self.reservationschedule = ReservationSchedule(self.database)

    def show_menu(self):
        print("1. Make a reservation")
        print("2. Cancel a reservation")
        print("3. Print Schedule")
        print("4. Save schedule to a file")
        print("5. Exit")
        user_input = input("What you want to do?\n")
        user_input = user_input.capitalize()

        if user_input.startswith("Make") or user_input == "1":
            self.reservationschedule.make_reservation()
            return True
        elif user_input.startswith("Cancel") or user_input == "2":
            self.reservationschedule.cancel_reservation()
            return True
        elif user_input.startswith("Print") or user_input == "3":
            self.reservationschedule.show_schedule()
            return True
        elif user_input.startswith("Save") or user_input == "4":
            self.reservationschedule.save_schedule()
            return True
        elif user_input.startswith("Exit") or user_input == "5":
            print("Have a good day!")
            return False
        elif user_input == "Setup_table":
            self.database.setup_table()
            return True
        else:
            print("Wrong input, try again:")
            return True
