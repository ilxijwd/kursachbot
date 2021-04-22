import time

import schedule

import src.scheduler.tasks


def loop_over_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)
