from chains.utils import run_map_reduce_summarize
from celery import shared_task


@shared_task
def run_summary_task(task_id: str, content: list[str]) -> None:
    run_map_reduce_summarize(content=content, task_id=task_id)
