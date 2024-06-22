from agents.utils import run_url_marketing_report
from celery import shared_task


@shared_task
def run_marketing_report_task(
    url: str, user_id: int, task_id: str, event_id: int, report_style: str
) -> None:
    run_url_marketing_report(
        url=url,
        user_id=user_id,
        task_id=task_id,
        event_id=event_id,
        report_style=report_style,
    )
