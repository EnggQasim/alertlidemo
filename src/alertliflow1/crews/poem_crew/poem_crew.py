from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
import os

llm1 = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=os.environ['GEMINI_API_KEY'],
)

google_embedder = {
    "provider": "google",
    "config": {
         "model": "models/text-embedding-004",
         "api_key": os.environ['GEMINI_API_KEY'],
         }
}


# Create a knowledge source
content_source = CrewDoclingSource(
    file_paths=[
        "https://www.alertli.com/privacy.html"
    ],
)

@CrewBase
class AlertLiCrew:
    """Poem Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["manager"],
        )
    
    @agent
    def sql_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["sql_expert"],
        )
    
    @agent
    def knowldge_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["knowldge_expert"],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def write_poem(self) -> Task:
        return Task(
            config=self.tasks_config["alertli_search"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=[self.knowldge_expert(), self.sql_expert()],  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_agent=self.manager(),
            planning=True,
            planning_llm=llm1,
            embedder=google_embedder,
            knowledge_sources=[content_source]
        )
