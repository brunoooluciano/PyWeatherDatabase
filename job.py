import schedule
import time
from main import main


def job():
    main.mainRun()
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
db.close()





