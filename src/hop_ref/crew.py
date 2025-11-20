from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from hop_ref.tools.linkedin_research_tool import LinkedInResearchTool
from hop_ref.tools.hashtag_generator_tool import HashtagGeneratorTool


@CrewBase
class LinkedInContentStudio():
    """
    LinkedIn Content Studio - HOP crew that creates LinkedIn posts with carousel outlines.
    4 agents work sequentially: Hook Crafter → Value Builder → Engagement Architect → Format Alchemist
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def hook_crafter(self) -> Agent:
        """Creates compelling hooks using LinkedIn research data"""
        return Agent(
            config=self.agents_config['hook_crafter'],
            verbose=True,
            tools=[LinkedInResearchTool()]
        )

    @agent
    def value_builder(self) -> Agent:
        """Transforms topics into actionable content"""
        return Agent(
            config=self.agents_config['value_builder'],
            verbose=True
        )

    @agent
    def engagement_architect(self) -> Agent:
        """Adds CTAs, comment prompts, and strategic hashtags"""
        return Agent(
            config=self.agents_config['engagement_architect'],
            verbose=True,
            tools=[HashtagGeneratorTool()]
        )

    @agent
    def format_alchemist(self) -> Agent:
        """Creates carousel slide outlines"""
        return Agent(
            config=self.agents_config['format_alchemist'],
            verbose=True
        )

    @task
    def make_hook(self) -> Task:
        """Create 3 alternative hooks"""
        return Task(
            config=self.tasks_config['make_hook']
        )

    @task
    def build_value(self) -> Task:
        """Develop post body with examples"""
        return Task(
            config=self.tasks_config['build_value'],
        )

    @task
    def add_engagement(self) -> Task:
        """Add CTA, comment prompt, and hashtags"""
        return Task(
            config=self.tasks_config['add_engagement']
        )

    @task
    def compose_carousel(self) -> Task:
        """Create 6-8 slide carousel outline"""
        return Task(
            config=self.tasks_config['compose_carousel'],
            output_file='output/carousel_outline.md',
        )

    @crew
    def crew(self) -> Crew:
        """Assemble the crew with a sequential process or hierarchical"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
