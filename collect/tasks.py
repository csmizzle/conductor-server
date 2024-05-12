"""
Celery tasks for the collect app.
"""
from celery import shared_task
from conductor.functions.apify_ import sync_summarize_urls
from collect import models
import logging


logger = logging.getLogger(__name__)


@shared_task
def task_collect_summarize_urls(task_id: str, urls: list[str]) -> None:
    """
    Task for summarizing URLs.
    """
    # get task and update status to running
    task = models.Task.objects.get(pk=task_id)
    logging.info(f"Task {task_id} started ...")
    task.status = models.TaskStatus.RUNNING
    task.save()
    try:
        summaries = sync_summarize_urls(urls=urls, task_id=task_id)
        # serialize the data into URLSummary objects
        for summary in summaries:
            logging.info(f"Saving summary for {summary["job_id"]} ...")
            summary_object = models.URLSummary(
                job_id=summary["job_id"],
                task_id=task,
                url=summary["url"],
                content=summary["content"],
                summary=summary["summary"],
            )
            summary_object.save()
        # update task status to completed
        task.status = models.TaskStatus.COMPLETED
        task.save()
    except Exception as e:
        logging.error(f"Error in task {task_id}: {str(e)}")
        task.status = models.TaskStatus.FAILED
        task.save()
        raise e
