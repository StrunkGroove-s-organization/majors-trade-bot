from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .check_links import check_links

scheduler = AsyncIOScheduler()

scheduler.add_job(check_links, "interval", seconds=1)
