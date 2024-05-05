from conductor.agents import (
    apollo_email_agent,
    answer_agent,
    apollo_email_task,
    answer_email_task
)
from crewai import Crew


market_email_crew = Crew(
    agents=[
        apollo_email_agent,
        answer_agent,
    ],
    tasks=[
        apollo_email_task,
        answer_email_task,
    ],
    verbose=True,
    memory=True,
    cache=True,
    share_crew=False,
)