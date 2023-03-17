from utils.Database import Database
from utils.Menu import Menu
from datetime import datetime, timedelta

db = Database('TenisCourt.db')
menu = Menu(db)

while menu.show_menu():
    pass
