from utils.Database import Database
from utils.Menu import Menu

db = Database('TenisCourt.db')
menu = Menu(db)

while menu.show_menu():
    pass
