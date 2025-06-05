#!/usr/bin/env python
import sys
import warnings
import uvicorn
from datetime import datetime

from .crew import ContentGenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'platform': 'twitter',
        'content_type': 'social media post',
        'topic': 'AI LLMs',
        'tone': 'professional',
        'target_audience': 'developers',
        'content_goals': 'engagement and education',
        'current_year': str(datetime.now().year),
        'feedback': None
    }
    
    try:
        generator = ContentGenerator()
        result = generator.crew().kickoff(inputs=inputs)
        print("Content generated successfully:")
        print(result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'platform': 'twitter',
        'content_type': 'social media post',
        'topic': 'AI LLMs',
        'tone': 'professional',
        'target_audience': 'developers',
        'content_goals': 'engagement and education',
        'current_year': str(datetime.now().year)
    }
    try:
        ContentGenerator().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ContentGenerator().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'platform': 'twitter',
        'content_type': 'social media post',
        'topic': 'AI LLMs',
        'tone': 'professional',
        'target_audience': 'developers',
        'content_goals': 'engagement and education',
        'current_year': str(datetime.now().year)
    }
    
    try:
        ContentGenerator().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def serve():
    """
    Start the FastAPI server for the content generator.
    """
    uvicorn.run("pitch.api:app", host="0.0.0.0", port=8000, reload=True)
