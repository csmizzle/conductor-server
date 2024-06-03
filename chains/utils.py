"""
Utility functions for the collect module.
"""
import logging
from conductor.chains import map_reduce_summarize
from chains import models

logger = logging.getLogger(__name__)


def run_map_reduce_summarize(content: list[str], task_id: str, event_id: int) -> None:
    task = models.ChainTask.objects.get(pk=task_id)
    event = models.ChainEvent.objects.get(pk=event_id)
    logging.info(f"Task {task_id} started ...")
    task.status = models.ChainTaskStatus.RUNNING
    task.save()
    try:
        summary = map_reduce_summarize(contents=content)
        # serialize the data into URLSummary objects
        logging.info("Saving summary ...")
        summary_object = models.Summary(
            task_id=task,
            content=content,
            summary=summary["output_text"],
        )
        summary_object.save()
        # update task status to completed
        task.status = models.ChainTaskStatus.COMPLETED
        task.save()
        # update event output
        event.output = summary
        event.save()
    except Exception as e:
        logging.error(f"Error in task {task_id}: {str(e)}")
        task.status = models.ChainTaskStatus.FAILED
        task.save()
        raise e
