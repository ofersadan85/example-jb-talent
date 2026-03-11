from time import sleep
from datetime import datetime, timedelta

def break_timer(m):
    break_over = datetime.now() + timedelta(minutes=m)
    while (break_over - datetime.now()).total_seconds() > 0:
        print("BREAK OVER:", break_over - datetime.now())
        sleep(1)


# break_timer(13)

# next_year = datetime(2027, 1, 1, 12)
# formatted = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# as_date = datetime.strptime(formatted, "%d/%m/%Y %H:%M:%S")
