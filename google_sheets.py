import gspread

gc = gspread.service_account(filename="poisonsell.json")
sh = gc.open("PoisonSell_base")
USERS = sh.worksheet("Пользователи")
ORDERS = sh.worksheet("Заказы")
MAIN_DATA = sh.worksheet("Основные данные")

