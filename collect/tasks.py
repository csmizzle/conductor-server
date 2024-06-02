"""
Celery tasks for the collect app.
"""
from celery import shared_task

from collect.utils import run_url_summary_task


@shared_task
def task_collect_summarize_urls(task_id: str, urls: list[str]) -> None:
    """
    Task for summarizing URLs.
    """
    # get task and update status to running
    run_url_summary_task(urls=urls, task_id=task_id)
