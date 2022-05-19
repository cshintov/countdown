"""
Show countdown to an event.
"""

import time
from datetime import date
from datetime import datetime
from operator import itemgetter

from rich import print
from rich.progress import Progress
from rich.console import Console
from rich.table import Table

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

    show_progress_table(
            str(days_remaining), str(days_gone), str(days_total))

    try:
        show_progress(days_gone, days_total, interval)
    except KeyboardInterrupt:
        print('Stopped!')


def show_progress_table(remaining, gone, total):
    table = Table(title="Progress")

    table.add_column("Remaining", style="cyan", no_wrap=True)
    table.add_column("Gone", style="magenta")
    table.add_column("Total", justify="right", style="green")

    table.add_row(remaining, gone, total)

    console = Console()
    console.print(table)

if __name__ == '__main__':
    show_progress_of_an_event('f988597e-8683-4f38-b279-aae146d3e0d9')
