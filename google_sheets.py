import gspread

gc = gspread.service_account(filename="./data/poisonsell.json")
sh = gc.open("PoisonSell_base")
USERS = sh.worksheet("Пользователи")
ORDERS = sh.worksheet("Заказы")
MAIN_DATA = sh.worksheet("Основные данные")
PROMOCODES = sh.worksheet("Промокоды")
