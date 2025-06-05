from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Callable, Any
from langchain_openai import ChatOpenAI
import asyncio
from datetime import datetime
# Enhanced tool imports
from .tools.document_tools import DocumentParserTool
from .tools.serper_tool import WebResearchTool
from .tools.github_tool import GithubRepoTool
from .tools.custom_tool import (
    MarketResearchTool, CompetitorAnalysisTool, TrendAnalysisTool,
    ContentOptimizationTool, HashtagResearchTool, VisualContentAdvisorTool,
    AnalyticsTool, ABTestingAdvisorTool, PerformancePredictorTool,
    PlatformAnalyzerTool, AlgorithmInsightsTool, FormatOptimizerTool,
    AudienceAnalysisTool, PsychographicProfilerTool, EngagementPredictorTool,
    KeywordResearchTool, SEOAnalyzerTool, SERPAnalyzerTool,
    ViralAnalysisTool, TrendDetectorTool, TimingOptimizerTool,
    BrandVoiceAnalyzerTool, ConsistencyCheckerTool, ToneCalibratorTool,
    GithubAnalyzerTool, CodeDocumentationTool, DeveloperCommunityInsightsTool,
    QualityCheckerTool, FactVerifierTool, StyleGuideEnforcerTool
)
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
            tools=[
                MarketResearchTool(),
                CompetitorAnalysisTool(),
                TrendAnalysisTool(),
                WebResearchTool()
            ]
        )

    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator'],
            llm=self.llm,
            verbose=True,
            tools=[
                ContentOptimizationTool(),
                HashtagResearchTool(),
                VisualContentAdvisorTool()
            ]
        )

    @agent
    def content_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_optimizer'],
            llm=self.llm,
            verbose=True,
            tools=[
                AnalyticsTool(),
                ABTestingAdvisorTool(),
                PerformancePredictorTool()
            ]
        )

    @agent
    def platform_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['platform_specialist'],
            llm=self.llm,
            verbose=True,
            tools=[
                PlatformAnalyzerTool(),
                AlgorithmInsightsTool(),
                FormatOptimizerTool()
            ]
        )

    @agent
    def audience_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['audience_researcher'],
            llm=self.llm,
            verbose=True,
            tools=[
                AudienceAnalysisTool(),
                PsychographicProfilerTool(),
                EngagementPredictorTool()
            ]
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_specialist'],
            llm=self.llm,
            verbose=True,
            tools=[
                KeywordResearchTool(),
                SEOAnalyzerTool(),
                SERPAnalyzerTool()
            ]
        )

    @agent
    def viral_content_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['viral_content_analyst'],
            llm=self.llm,
            verbose=True,
            tools=[
                ViralAnalysisTool(),
                TrendDetectorTool(),
                TimingOptimizerTool()
            ]
        )

    @agent
    def brand_voice_guardian(self) -> Agent:
        return Agent(
            config=self.agents_config['brand_voice_guardian'],
            llm=self.llm,
            verbose=True,
            tools=[
                BrandVoiceAnalyzerTool(),
                ConsistencyCheckerTool(),
                ToneCalibratorTool()
            ]
        )

    @agent
    def github_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['github_specialist'],
            llm=self.llm,
            verbose=True,
            tools=[
                GithubRepoTool(),
                GithubAnalyzerTool(),
                CodeDocumentationTool(),
                DeveloperCommunityInsightsTool()
            ]
        )

    @agent
    def quality_assurance_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_assurance_specialist'],
            llm=self.llm,
            verbose=True,
            tools=[
                QualityCheckerTool(),
                FactVerifierTool(),
                StyleGuideEnforcerTool()
            ]
        )

    @task
    def audience_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['audience_research_task'],
            context_format=True
        )

    @task
    def market_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_analysis_task'],
            context_format=True
        )

    @task
    def content_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_strategy_task'],
            context_format=True
        )

    @task
    def seo_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization_task'],
            context_format=True
        )

    @task
    def brand_voice_calibration_task(self) -> Task:
        return Task(
            config=self.tasks_config['brand_voice_calibration_task'],
            context_format=True
        )

    @task
    def content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_creation_task'],
            context_format=True
        )

    @task
    def viral_potential_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['viral_potential_analysis_task'],
            context_format=True
        )

    @task
    def github_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['github_analysis_task'],
            context_format=True
        )

    @task
    def github_content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['github_content_creation_task'],
            context_format=True
        )

    @task
    def content_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_optimization_task'],
            context_format=True
        )

    @task
    def quality_assurance_task(self) -> Task:
        return Task(
            config=self.tasks_config['quality_assurance_task'],
            context_format=True
        )

    @task
    def performance_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['performance_planning_task'],
            context_format=True
        )

    @task
    def feedback_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['feedback_analysis_task'],
            context_format=True
        )

    @task
    def content_iteration_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_iteration_task'],
            context_format=True
        )

    @task
    def quick_content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['quick_content_creation_task'],
            context_format=True
        )

    def get_task_list(self, platform: str = None, feedback: str = None, quick_mode: bool = False) -> List[Task]:
        """Get the appropriate task list based on conditions - CONTENT FIRST APPROACH"""
        
        # Quick mode: Just create content without extensive research
        if quick_mode:
            task_list = [
                self.quick_content_creation_task(),
                self.quality_assurance_task()
            ]
            return task_list
        
        # CONTENT-FIRST APPROACH: Generate content immediately, then enhance with research
        task_list = [
            # 🎯 PHASE 1: IMMEDIATE CONTENT GENERATION (User gets content fast!)
            self.quick_content_creation_task(),  # Generate initial content immediately
            
            # 🔬 PHASE 2: RESEARCH & ANALYSIS (Gather data to enhance content)
            self.audience_research_task(),       # Research to understand audience better
            self.market_analysis_task(),         # Market insights for optimization
            
            # ✨ PHASE 3: CONTENT ENHANCEMENT (Apply research to improve content)
            self.content_optimization_task(),    # Apply research to enhance content
            
            # 🎨 PHASE 4: FINAL CONTENT DELIVERY (MUST BE LAST!)
            self.quality_assurance_task(),       # Final quality check with enhanced content
        ]
        
        # Add GitHub-specific tasks if platform is GitHub
        if platform and platform.lower() == "github":
            # Insert GitHub tasks before content optimization
            github_tasks = [
                self.github_analysis_task(),
                self.github_content_creation_task()
            ]
            # Insert after market analysis but before content optimization
            task_list = task_list[:3] + github_tasks + task_list[3:]
        
        # Add feedback-based tasks if feedback is provided
        if feedback and feedback.strip():
            task_list.extend([
                self.feedback_analysis_task(),
                self.content_iteration_task()
            ])
        
        # NOTE: Performance planning, SEO, viral analysis etc. are REMOVED from default flow
        # These were causing strategy/analysis outputs instead of actual content
        # The quality_assurance_task is the FINAL task that delivers the actual content
        
        return task_list
        
        return task_list

    @crew
    def crew(self) -> Crew:
        """Creates the Content Generator crew"""
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
                'agent': task.agent.name if task.agent else 'Unknown',
                'task': task.description,
                'timestamp': datetime.now().isoformat()
            }))

        def task_completed(task: Task) -> None:
            asyncio.create_task(status_callback('task_completed', {
                'job_id': task.context.get('job_id'),
                'message': f"Completed task: {task.description[:100]}...",
                'agent': task.agent.name if task.agent else 'Unknown',
                'task': task.description,
                'output': getattr(task, 'output', ''),
                'timestamp': datetime.now().isoformat()
            }))

        # Get all agents
        all_agents = [
            self.content_strategist(),
            self.content_creator(),
            self.content_optimizer(),
            self.platform_specialist(),
            self.audience_researcher(),
            self.seo_specialist(),
            self.viral_content_analyst(),
            self.brand_voice_guardian(),
            self.github_specialist(),
            self.quality_assurance_specialist()
        ]

        # Get all tasks (will be filtered based on inputs during kickoff)
        all_tasks = [
            self.quick_content_creation_task(),
            self.audience_research_task(),
            self.market_analysis_task(),
            self.content_strategy_task(),
            self.seo_optimization_task(),
            self.brand_voice_calibration_task(),
            self.content_creation_task(),
            self.viral_potential_analysis_task(),
            self.github_analysis_task(),
            self.github_content_creation_task(),
            self.content_optimization_task(),
            self.quality_assurance_task(),
            self.performance_planning_task(),
            self.feedback_analysis_task(),
            self.content_iteration_task()
        ]

        return Crew(
            agents=all_agents,
            tasks=all_tasks,
            process=Process.sequential,
            verbose=True,
            task_started_callback=task_started,
            task_completed_callback=task_completed
        )

    def create_dynamic_crew(self, platform: str = None, feedback: str = None, quick_mode: bool = False) -> Crew:
        """Create a crew with tasks filtered based on conditions"""
        # Get base task list
        task_list = self.get_task_list(platform=platform, feedback=feedback, quick_mode=quick_mode)
        
        # Get all agents
        all_agents = [
            self.content_strategist(),
            self.content_creator(),
            self.content_optimizer(),
            self.platform_specialist(),
            self.audience_researcher(),
            self.seo_specialist(),
            self.viral_content_analyst(),
            self.brand_voice_guardian(),
            self.github_specialist(),
            self.quality_assurance_specialist()
        ]

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
                'agent': task.agent.name if task.agent else 'Unknown',
                'task': task.description,
                'timestamp': datetime.now().isoformat()
            }))

        def task_completed(task: Task) -> None:
            asyncio.create_task(status_callback('task_completed', {
                'job_id': task.context.get('job_id'),
                'message': f"Completed task: {task.description[:100]}...",
                'agent': task.agent.name if task.agent else 'Unknown',
                'task': task.description,
                'output': getattr(task, 'output', ''),
                'timestamp': datetime.now().isoformat()
            }))

        return Crew(
            agents=all_agents,
            tasks=task_list,
            process=Process.sequential,
            verbose=True,
            task_started_callback=task_started,
            task_completed_callback=task_completed
        )
