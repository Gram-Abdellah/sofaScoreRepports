import schedule
import time
import os

def run_main_script():
    os.system('python generate_reports.py')

schedule.every().day.at("00:00").do(run_main_script)

while True:
    schedule.run_pending()
    time.sleep(1)
