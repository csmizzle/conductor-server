from celery import shared_task
from chains.utils import run_map_reduce_summarize


@shared_task
def run_summary_task(event_id: int, task_id: str, content: list[str]) -> None:
    run_map_reduce_summarize(event_id=event_id, content=content, task_id=task_id)
