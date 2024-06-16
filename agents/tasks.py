from agents.utils import run_url_marketing_report
from celery import shared_task


@shared_task
def run_marketing_report_task(
    url: str,
    user_id: int,
    task_id: str,
    event_id: int,
) -> None:
    run_url_marketing_report(url, user_id, task_id, event_id)
