from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Callable, Any
from langchain_openai import ChatOpenAI
import asyncio
from datetime import datetime
from .tools.document_tools import DocumentParserTool
from .tools.serper_tool import WebResearchTool
from .status_manager import status_manager

@CrewBase
class ContentGenerator():
    """Content Generator crew for creating engaging content"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        self.llm = ChatOpenAI(
            model_name="gpt-4-turbo-preview",
            temperature=0.7,
        )

    @agent
    def content_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['content_strategist'],
            llm=self.llm,
            verbose=True,
            tools=[WebResearchTool()]
        )

    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator'],
            llm=self.llm,
            verbose=True
        )

    @agent
    def content_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_optimizer'],
            llm=self.llm,
            verbose=True
        )

    @task
    def content_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_strategy_task'],
            context_format=True
        )

    @task
    def content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_creation_task'],
            context_format=True
        )

    @task
    def content_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_optimization_task'],
            context_format=True
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Pitch crew for analyzing pitch decks"""
        async def status_callback(event_type: str, event_data: dict):
            if 'job_id' in event_data:
                # Convert any non-serializable output to string
                output = event_data.get('output', '')
                if output and not isinstance(output, (str, int, float, bool, list, dict)):
                    output = str(output)

                status_data = {
                    "status": "in_progress",
                    "type": event_type,
                    "message": str(event_data.get('message', 'Processing...')),
                    "progress": event_data.get('progress'),
                    "timestamp": event_data.get('timestamp', ''),
                    "agent": str(event_data.get('agent', '')),
                    "task": str(event_data.get('task', '')),
                    "output": output
                }
                await status_manager.broadcast_status(event_data['job_id'], status_data)

        def task_started(task: Task) -> None:
            asyncio.create_task(status_callback('task_started', {
                'job_id': task.context.get('job_id'),
                'message': f"Starting task: {task.description[:100]}...",
                'agent': task.agent.name,
                'task': task.description,
                'timestamp': datetime.now().isoformat()
            }))

        def task_completed(task: Task) -> None:
            asyncio.create_task(status_callback('task_completed', {
                'job_id': task.context.get('job_id'),
                'message': f"Completed task: {task.description[:100]}...",
                'agent': task.agent.name,
                'task': task.description,
                'output': task.output,
                'timestamp': datetime.now().isoformat()
            }))

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            task_started_callback=task_started,
            task_completed_callback=task_completed
        )
