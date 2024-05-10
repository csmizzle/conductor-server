"""
Celery tasks for the collect app.
"""
from celery import shared_task
from conductor.functions.apify_ import sync_summarize_urls


@shared_task
def task_collect_summarize_urls(urls) -> dict:
    """
    Task for summarizing URLs.
    """
    data = sync_summarize_urls(urls)
    return [dict(_) for _ in data]
