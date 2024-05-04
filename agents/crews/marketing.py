from conductor.agents import (
    query_builder_agent,
    apollo_email_agent,
    answer_agent,
    create_query_task,
    apollo_email_task,
    answer_email_task
)
from crewai import Crew


market_email_crew = Crew(
    agents=[
        query_builder_agent,
        apollo_email_agent,
        answer_agent,
    ],
    tasks=[
        create_query_task,
        apollo_email_task,
        answer_email_task,
    ],
    verbose=True,
    memory=True,
    cache=True,
    share_crew=False,
)