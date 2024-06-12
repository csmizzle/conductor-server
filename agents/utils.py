"""
Agent workflows
"""
from django.contrib.auth.models import User
import logging
from chains import models as chains_models
from reports import models as report_models
from conductor.crews.marketing import run_url_marketing_report as url_marketing_report

logger = logging.getLogger(__name__)


def run_url_marketing_report(
    url: str,
    user_id: int,
    task_id: str,
    event_id: int,
) -> report_models.Report:
    task = chains_models.ChainTask.objects.get(pk=task_id)
    event = chains_models.ChainEvent.objects.get(pk=event_id)
    user = User.objects.get(pk=user_id)
    logging.info(f"Task {task_id} started ...")
    task.status = chains_models.ChainTaskStatus.RUNNING
    task.save()
    try:
        url_report = url_marketing_report(url)
        # save event status and save report
        logger.info("Creating report ...")
        report = report_models.Report.objects.create(
            created_by=user,
            task=task,
            title=url_report.title,
            description=url_report.description,
        )
        # create paragraphs
        for paragraph in url_report.paragraphs:
            logger.info("Creating paragraph ...")
            paragraph = report_models.Paragraph.objects.create(
                created_by=user, title=paragraph.title, content=paragraph.content
            )
            logger.info("Adding paragraph to report ...")
            report.paragraphs.add(paragraph)
        logger.info("Saving report ...")
        report.save()
        # update task status to completed
        logger.info("Updating task status to completed ...")
        task.status = chains_models.ChainTaskStatus.COMPLETED
        task.save()
        # update event output
        logger.info("Saving event output ...")
        event.output = url_report.dict()
        event.save()
        return report
    except Exception as exception:
        logging.error(f"Error in task {task_id}")
        task.status = chains_models.ChainTaskStatus.FAILED
        task.save()
        raise exception
