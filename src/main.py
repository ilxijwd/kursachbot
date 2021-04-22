from threading import Thread

from src.bot import loop_over_requests
from src.scheduler import loop_over_tasks


if __name__ == '__main__':
    bot_thread = Thread(target=loop_over_requests)
    schedule_thread = Thread(target=loop_over_tasks)

    bot_thread.start()
    schedule_thread.start()
