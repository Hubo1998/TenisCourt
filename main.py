from utils.Database import Database
from utils.Menu import Menu
from datetime import datetime, timedelta

print(type(datetime(2022,1,1).date()))
print(timedelta(days=730).days)
db = Database('TenisCourt.db')
menu = Menu(db)

while menu.show_menu():
    pass
