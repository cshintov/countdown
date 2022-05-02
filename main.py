"""
Show countdown to an event.
"""

import time
from datetime import date
from datetime import datetime

from operator import itemgetter
from rich.progress import Progress
from rich import print

from db import init, get_event

SECONDS_IN_A_DAY = 10 #86400

def destructure(dict_, *keys):
    return itemgetter(*keys)(dict_)

def show_progress(start, end, interval):
    """ Given start, end and interval show progress """

    with Progress() as progress:

        task1 = progress.add_task("", total=end, completed=start)

        while not progress.finished:
            progress.update(task1, advance=1)
            time.sleep(interval)

def get_today():
    return datetime.now().date()

def test():
    start = date(year=2022, month=3, day=23)
    today = get_today()
    end = date(year=2022, month=5, day=24)
    days_remaining = (end - today).days
    days_gone = (today - start).days
    days_total = (end - start).days
    print(f'{days_total=} {days_gone=} {days_remaining=}')
    show_progress(days_gone, days_total, interval=SECONDS_IN_A_DAY)

def split_time(start, end):
    now = datetime.now()
    days_remaining = (end - now).days
    days_gone = (now - start).days
    days_total = (end - start).days

    return days_remaining, days_gone, days_total

def show_progress_of_an_event(id_):
    conn = init('./countdown.db')
    event = get_event(conn, id_)

    start, end, interval = event[2], event[3], event[4]
    days_remaining, days_gone, days_total = split_time(start, end)

    print(f'{days_total=} {days_gone=} {days_remaining=}')
    show_progress(days_gone, days_total, interval)

if __name__ == '__main__':
    show_progress_of_an_event('b141fe02-c017-43ee-9bd4-382aab9a13cd')
