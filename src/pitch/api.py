from fastapi import FastAPI, WebSocket, BackgroundTasks, Form
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
    feedback: str = None
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
        
        print(f"\nStarting content generation with:")
        print(f"- Platform: {platform}")
        print(f"- Content Type: {content_type}")
        print(f"- Topic: {topic}")
        print(f"- Tone: {tone}")
        print(f"- Target Audience: {target_audience}")
        print(f"- Goals: {content_goals}")
        if feedback:
            print(f"- Feedback: {feedback}")

        # Run tasks and send updates
        try:
            result = generator.crew().kickoff(inputs=inputs)
            
            # Convert CrewOutput to string if needed
            result_text = str(result) if result else ""
            
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

@app.post("/generate")
async def create_content(
    background_tasks: BackgroundTasks,
    platform: str = Form(...),
    content_type: str = Form(...),
    topic: str = Form(...),
    tone: str = Form(...),
    target_audience: str = Form(...),
    content_goals: str = Form(...),
    feedback: Optional[str] = Form(None)
):
    """
    Generate content based on provided parameters
    """
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
        feedback=feedback
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
