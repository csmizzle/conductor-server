"""
Agent workflows
"""
from django.contrib.auth.models import User
import logging
from chains import models as chains_models
from reports import models as report_models
from agents import models as agents_models
from conductor.crews.marketing import run_marketing_crew, create_marketing_report
from conductor.reports.models import Report, ReportStyle
from conductor.crews.models import CrewRun

logger = logging.getLogger(__name__)


def save_pydantic_crew_run(
    pydantic_crew_run: CrewRun, user: User
) -> agents_models.CrewRun:
    """
    Save a Pydantic crew run to the database
    """
    crew_run = agents_models.CrewRun.objects.create(
        created_by=user,
        result=pydantic_crew_run.result,
    )
    for task in pydantic_crew_run.task_outputs:
        task_model = agents_models.CrewTask.objects.create(
            created_by=user,
            description=task.description,
            output=task.raw_output,
        )
        crew_run.tasks.add(task_model)
    crew_run.save()
    return crew_run


def save_pydantic_report(
    pydantic_report: Report,
    user: User,
    task: chains_models.ChainTask,
) -> report_models.Report:
    """
    Save a Pydantic report to the database
    """
    parsed_report = report_models.ParsedReport.objects.create(
        created_by=user,
        task=task,
        title=pydantic_report.report.title,
        description=pydantic_report.report.description,
    )
    report = report_models.Report.objects.create(
        created_by=user,
        report=parsed_report,
        raw=pydantic_report.raw,
        style=pydantic_report.style.value,
    )
    # create sections and paragraphs
    for section_entry in pydantic_report.report.sections:
        logger.info("Creating section ...")
        section = report_models.Section.objects.create(
            created_by=user, title=section_entry.title
        )
        for paragraph in section_entry.paragraphs:
            logger.info("Creating paragraph ...")
            paragraph = report_models.Paragraph.objects.create(
                created_by=user,
                title=paragraph.title,
                content=paragraph.content,
            )
            logger.info("Adding paragraph to section ...")
            section.paragraphs.add(paragraph)
        report.report.sections.add(section)
    logger.info("Saving report ...")
    report.save()
    return report


def run_url_marketing_report(
    url: str, user_id: int, task_id: str, event_id: int, report_style: str
) -> report_models.Report:
    report_style_enum = style_input_to_enum(report_style)
    task = chains_models.ChainTask.objects.get(pk=task_id)
    event = chains_models.ChainEvent.objects.get(pk=event_id)
    user = User.objects.get(pk=user_id)
    logging.info(f"Task {task_id} started ...")
    task.status = chains_models.ChainTaskStatus.RUNNING
    task.save()
    try:
        # run crew
        logger.info("Running crew ...")
        crew_run = run_marketing_crew(
            url=url,
            report_style=report_style_enum,
        )
        # save crew run
        logger.info("Saving crew run ...")
        crew_run = save_pydantic_crew_run(
            user=user,
            pydantic_crew_run=crew_run,
        )
        # create marketing report
        logger.info("Creating marketing report ...")
        url_report = create_marketing_report(
            crew_run=crew_run,
            report_style=report_style_enum,
        )
        # save event status and save report
        logger.info("Saving raw result ...")
        event.output = url_report.raw
        event.save()
        logger.info("Creating report ...")
        report = save_pydantic_report(
            pydantic_report=url_report,
            user=user,
            task=task,
        )
        # save crew run to report
        logger.info("Saving crew run to report ...")
        report.crew_run = crew_run
        report.save()
        # update task status to completed
        logger.info("Updating task status to completed ...")
        task.status = chains_models.ChainTaskStatus.COMPLETED
        task.save()
        # update event output
        logger.info("Saving event output ...")
        event.output = url_report.raw
        event.save()
        return report
    except Exception as exception:
        logging.error(f"Error in task {task_id}")
        task.status = chains_models.ChainTaskStatus.FAILED
        task.save()
        raise exception


def style_input_to_enum(style: str) -> ReportStyle:
    """
    Convert style input to ReportStyle enum
    """
    if style == "BULLETED":
        return ReportStyle.BULLETED
    elif style == "NARRATIVE":
        return ReportStyle.NARRATIVE
