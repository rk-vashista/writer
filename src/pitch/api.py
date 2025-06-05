from fastapi import FastAPI, WebSocket, BackgroundTasks, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import uuid
import os
from typing import Dict, Optional
from datetime import datetime

from .crew import ContentGenerator
from .status_manager import status_manager

app = FastAPI(title="Content Generator")

# Mount static files
app.mount("/static", StaticFiles(directory="src/pitch/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def generate_content(
    job_id: str, 
    platform: str,
    content_type: str,
    topic: str,
    tone: str,
    target_audience: str,
    content_goals: str,
    github_token: str = None,
    repo_url: str = None,
    feedback: str = None,
    quick_mode: bool = False
):
    """Background task to generate content"""
    generator = ContentGenerator()
    
    try:
        # Initialize
        await status_manager.broadcast_status(job_id, {
            "status": "started",
            "type": "task_started",
            "message": "Starting content generation",
            "timestamp": datetime.now().isoformat()
        })
            
        # Run the crew with the inputs
        inputs = {
            'platform': platform,
            'content_type': content_type,
            'topic': topic,
            'tone': tone,
            'target_audience': target_audience,
            'content_goals': content_goals,
            'feedback': feedback,
            'job_id': job_id
        }

        # Handle GitHub-specific inputs
        if platform == 'github':
            if not repo_url:
                raise ValueError("Repository URL is required for GitHub content generation")
            inputs['repo_url'] = repo_url
            inputs['description'] = f"... and analyze GitHub repository: {repo_url}"
            if github_token:
                os.environ['GITHUB_TOKEN'] = github_token
        
        print(f"\nStarting content generation with:")
        print(f"- Platform: {platform}")
        print(f"- Content Type: {content_type}")
        print(f"- Topic: {topic}")
        print(f"- Tone: {tone}")
        print(f"- Target Audience: {target_audience}")
        print(f"- Goals: {content_goals}")
        if platform == 'github':
            print(f"- GitHub Repo: {repo_url}")
        if feedback:
            print(f"- Feedback: {feedback}")

        # Run tasks and send updates
        try:
            # Create a dynamic crew based on platform, feedback, and mode
            dynamic_crew = generator.create_dynamic_crew(platform=platform, feedback=feedback, quick_mode=quick_mode)
            result = dynamic_crew.kickoff(inputs=inputs)
            
            # Extract the actual content from CrewOutput
            result_text = ""
            
            # Debug: Print CrewOutput structure
            print(f"\n🔍 Debug - Result type: {type(result)}")
            print(f"🔍 Debug - Result attributes: {dir(result)}")
            
            # Try to get the actual content from the last task (quality_assurance_task)
            if hasattr(result, 'tasks_output') and result.tasks_output:
                print(f"🔍 Debug - Found {len(result.tasks_output)} task outputs")
                
                # Get the last task output (should be quality_assurance_task with final content)
                last_task_output = result.tasks_output[-1]
                print(f"🔍 Debug - Last task: {getattr(last_task_output, 'name', 'unknown')}")
                
                # Try different attributes to get the actual content
                if hasattr(last_task_output, 'raw') and last_task_output.raw:
                    result_text = last_task_output.raw
                elif hasattr(last_task_output, 'output') and last_task_output.output:
                    result_text = last_task_output.output
                elif hasattr(last_task_output, 'result') and last_task_output.result:
                    result_text = last_task_output.result
                else:
                    result_text = str(last_task_output)
                    
                print(f"🔍 Debug - Last task content preview: {result_text[:100]}...")
                
                # If the last task doesn't have content, try the second-to-last (content_optimization_task)
                if len(result_text.strip()) < 100 and len(result.tasks_output) > 1:
                    print("🔍 Debug - Last task output too short, trying previous task...")
                    second_last_output = result.tasks_output[-2]
                    
                    if hasattr(second_last_output, 'raw') and second_last_output.raw:
                        result_text = second_last_output.raw
                    elif hasattr(second_last_output, 'output') and second_last_output.output:
                        result_text = second_last_output.output
                    elif hasattr(second_last_output, 'result') and second_last_output.result:
                        result_text = second_last_output.result
                        
                    print(f"🔍 Debug - Second-to-last task content preview: {result_text[:100]}...")
            
            # Fallback to raw attribute
            if not result_text or len(result_text.strip()) < 100:
                if hasattr(result, 'raw'):
                    result_text = result.raw
                else:
                    result_text = str(result) if result else ""
            
            print(f"🔍 Debug - Result content preview: {result_text[:100]}...")
            
            # Ensure we have actual content, not just task descriptions
            if not result_text or len(result_text.strip()) < 50:
                result_text = "Content generation completed, but no substantial output was returned. Please try again with different parameters."
            
            # Check if the result looks like a task description instead of content
            if any(phrase in result_text.lower() for phrase in [
                'performance benchmarks', 'key performance indicators', 
                'strategic actions', 'outlined', 'analysis', 'recommendations'
            ]):
                print("⚠️ Warning: Result appears to be strategy/analysis instead of content")
                result_text = f"⚠️ SYSTEM ERROR: The AI returned strategy analysis instead of actual content.\n\nReceived: {result_text}\n\nPlease try again - the system should deliver ready-to-publish content, not analysis."
            
            print(f"\n✅ Final result length: {len(result_text)} characters")
            print(f"✅ Final result preview: {result_text[:200]}...")
            
            # Send completion status
            await status_manager.broadcast_status(job_id, {
                "status": "completed",
                "type": "completed",
                "message": "Content generated successfully",
                "result": result_text
            })
            
        except Exception as crew_error:
            await status_manager.broadcast_status(job_id, {
                "status": "error",
                "type": "error",
                "message": f"Error during content generation: {str(crew_error)}"
            })
            raise crew_error

    except Exception as e:
        await status_manager.broadcast_status(job_id, {
            "status": "error",
            "message": f"Error during content generation: {str(e)}"
        })
    finally:
        # Clear GitHub token from environment if it was set
        if platform == 'github' and github_token:
            os.environ.pop('GITHUB_TOKEN', None)

@app.post("/generate")
async def create_content(
    background_tasks: BackgroundTasks,
    platform: str = Form(...),
    content_type: str = Form(...),
    topic: str = Form(...),
    tone: str = Form(...),
    target_audience: str = Form(...),
    content_goals: str = Form(...),
    github_token: Optional[str] = Form(None),
    repo_url: Optional[str] = Form(None),
    feedback: Optional[str] = Form(None),
    quick_mode: bool = Form(False)
):
    """
    Generate content based on provided parameters
    """
    # Validate GitHub inputs
    if platform == 'github':
        if not repo_url:
            raise HTTPException(status_code=400, detail="Repository URL is required for GitHub content")
        if not repo_url.startswith(('http://', 'https://')):
            raise HTTPException(status_code=400, detail="Invalid repository URL")

    # Generate job ID
    job_id = str(uuid.uuid4())

    # Start generation in background
    background_tasks.add_task(
        generate_content,
        job_id=job_id,
        platform=platform,
        content_type=content_type,
        topic=topic,
        tone=tone,
        target_audience=target_audience,
        content_goals=content_goals,
        github_token=github_token,
        repo_url=repo_url,
        feedback=feedback,
        quick_mode=quick_mode
    )

    return {
        "job_id": job_id,
        "message": "Content generation started",
        "websocket_url": f"/ws/{job_id}"
    }

@app.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    """WebSocket endpoint for real-time status updates"""
    await status_manager.connect(websocket, job_id)
    try:
        while True:
            await websocket.receive_text()
    except:
        status_manager.disconnect(websocket, job_id)

@app.get("/")
async def read_root():
    """Serve the index.html file"""
    return FileResponse("src/pitch/static/index.html")

# Server will be started by uvicorn
