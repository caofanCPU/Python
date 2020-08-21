#!/usr/bin/env python
# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import os.path
import sys
from typing import Iterable
from urllib.request import urlopen
from rich import print
from rich.console import Console
import logging
from rich.logging import RichHandler

from rich.progress import (
    BarColumn,
    DownloadColumn,
    TextColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    Progress,
    TaskID,
)

progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
)


def copy_url(task_id: TaskID, url: str, path: str) -> None:
    """Copy data from a url to a local file."""
    response = urlopen(url)
    # This will break if the response doesn't contain content length
    progress.update(task_id, total=int(response.info()["Content-length"]))
    with open(path, "wb") as dest_file:
        progress.start_task(task_id)
        for data in iter(partial(response.read, 32768), b""):
            dest_file.write(data)
            progress.update(task_id, advance=len(data))


def download(url: str, loop: int, workers: int, dest_dir: str):
    """Download multuple files to the given directory."""
    if workers > 4:
        workers = 4
    if workers < 0:
        workers = 2
    with progress:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            for i in range(loop):
                filename = "D8{}.zip".format(i+1)
                dest_path = os.path.join(dest_dir, filename)
                task_id = progress.add_task("download", filename=filename, start=False)
                pool.submit(copy_url, task_id, url, dest_path)


def execute_download():
    url = "https://plugins.jetbrains.com/plugin/download?rel=true&updateId=94618"
    loop = 10
    workers = 2
    console = Console()
    console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")
    logging.basicConfig(level="DEBUG", format="%(message)s", datefmt="[%Y-%m-%d %X]", handlers=[RichHandler()])
    log = logging.getLogger("rich")
    try:
        if sys.argv[1]:
            loop = int(sys.argv[1])
        if sys.argv[2]:
            workers = int(sys.argv[2])
    except Exception as e:
        # just log
        log.warning("you didn't set any parameters!")
    console.print("parameter [bold magenta]loop[/bold magenta] = [bold green]10[/bold green], parameter [bold magenta]workers[/bold magenta] = [bold green]2[/bold green]")
    download(url, loop, workers, "./")


def main():
    execute_download()


if __name__ == '__main__':
    main()
