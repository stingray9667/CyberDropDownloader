import asyncio
import contextlib
import logging

import aiorun
from rich.logging import RichHandler

from cyberdrop_dl.managers.manager import Manager
from cyberdrop_dl.scraper.scraper import ScrapeMapper
from cyberdrop_dl.ui.ui import program_ui


def startup():
    """
    Starts the program and returns the manager
    This will also run the UI for the program
    After this function returns, the manager will be ready to use and scraping / downloading can begin
    """

    try:
        manager = Manager()
        manager.startup()

        if not manager.args_manager.immediate_download:
            program_ui(manager)

        logging.basicConfig(
            filename=manager.file_manager.main_log,
            level=logging.DEBUG,
            format="%(asctime)s:%(levelname)s:%(module)s:%(filename)s:%(lineno)d:%(message)s",
            filemode="w",
            # handlers=[RichHandler(rich_tracebacks=True)]
        )

        return manager

    except KeyboardInterrupt:
        print("\nExiting...")
        exit(0)


async def director(manager: Manager):
    await manager.async_startup()

    scrape_mapper = ScrapeMapper(manager)
    asyncio.create_task(scrape_mapper.map_urls())


def main():
    manager = startup()

    with contextlib.suppress(RuntimeError, asyncio.CancelledError):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        aiorun.run(director(manager))
        exit(0)


if __name__ == '__main__':
    main()
