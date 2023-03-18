# TenisCourt
Tenis Court reservation REPL application which allows to make and cancel reservations, print and save to a file schedule.

## MENU

![Image showing menu of an application](https://user-images.githubusercontent.com/64363554/226107067-ee51abf4-d6ef-47c5-a3ed-4bc63bbd5bf6.png)

You can input words in every menu or just numbers.
Capitalization doesn't matter, because it is always formatted properly after input.
You can also write "exit" in every step of the application what takes you to the menu.
In menu you can input "setup_table" to clear the table of database.

### Make a reservation

![Making a reservation process](https://user-images.githubusercontent.com/64363554/226108498-aac3d11c-f526-4026-a911-e15238f1f716.png)

To make a reservation you need to enter your name, date of reservation and duration.  
There is also validation of data which allows you to book a court only between 8:00 - 21:30, at least one hour in advance from present and only on full hour (HH:00) or half of hour (HH:30).
If there is a reservation on given date, program will suggest the next possible hour if it's possible
There are 3 intervals of duration, if the reservation will be to long because of the next booking, app will tell us to choose shorter duration

### Cancel a reservation

![Canceling a reservation](https://user-images.githubusercontent.com/64363554/226108757-b1db54be-0e5e-42e3-b8ea-cc247067bea8.png)

To cancel a reservation you need to enter your name and exact start date of your reservation, if there is no reservation for the name on specified date, process will fail and app will take us to menu.  

### Print Schedule

![printing a schedule](https://user-images.githubusercontent.com/64363554/226108975-06f19a39-2239-40f9-a3af-356affac40b2.png)

To print a schedule you need to enter start and end dates of period that you want to print.  
Instead of dates of the closest days we will see weekday names and etc.

### Save schedule to a file

![Saving a schedule](https://user-images.githubusercontent.com/64363554/226109302-88feb97e-3004-4ed5-a0f9-f578659fd562.png)

To save a schedule you need to enter start and end dates of period that you want to save.  
You can choose format of file and the filename.
.json and .csv files are in repo

