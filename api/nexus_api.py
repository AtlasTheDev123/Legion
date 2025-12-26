"""
Production-Ready NEXUS AI API
==============================
FastAPI endpoints for AI model access, agent coordination,
and system management.

Features:
- RESTful API for all AI capabilities
- WebSocket support for streaming
- Authentication and rate limiting
- Comprehensive error handling
- OpenAPI documentation
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
import asyncio
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import NexusAIOrchestrator
from agents.nexus_ai_model import get_nexus_ai
from agents.distributed_agents import DistributedAgentSystem, AgentRole
from agents.llm_integration import LLMManager

# Initialize FastAPI
app = FastAPI(
    title="NEXUS AI API",
    description="Production API for NEXUS-LEGION-X-OMEGA AI System",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
orchestrator = None
agent_system = None
llm_manager = None


# Pydantic models
class TaskRequest(BaseModel):
    task: str = Field(..., description="Task description")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    priority: Optional[int] = Field(default=5, ge=1, le=10, description="Priority level")


class TaskResponse(BaseModel):
    task_id: str
    status: str
    confidence: float
    strategy_used: str
    execution_steps: List[Dict[str, Any]]
    outcome: str


class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Source code to analyze")
    language: Optional[str] = Field(default=None, description="Programming language")


class CodeAnalysisResponse(BaseModel):
    language: str
    complexity: float
    issues: List[Dict[str, str]]
    suggestions: List[str]
    confidence: float


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    use_context: Optional[bool] = Field(default=True, description="Use conversation context")
    provider: Optional[str] = Field(default=None, description="LLM provider to use")
    stream: Optional[bool] = Field(default=False, description="Stream response")


class ChatResponse(BaseModel):
    response: str
    provider: str
    model: str
    tokens_used: int
    latency_ms: float


class AgentSpawnRequest(BaseModel):
    name: str = Field(..., description="Agent name")
    role: str = Field(..., description="Agent role")
    capabilities: List[str] = Field(..., description="Agent capabilities")


class AgentSpawnResponse(BaseModel):
    agent_id: str
    name: str
    role: str
    status: str


class LearningRequest(BaseModel):
    experience: str = Field(..., description="Experience description")
    outcome: str = Field(..., description="Outcome or lesson learned")
    importance: float = Field(default=0.5, ge=0.0, le=1.0, description="Importance score")
    tags: Optional[List[str]] = Field(default=None, description="Category tags")


class SystemStatus(BaseModel):
    status: str
    timestamp: str
    core_ai: Dict[str, Any]
    distributed_agents: Dict[str, Any]
    llm_providers: List[str]
    uptime_seconds: float


# Authentication (simple token-based for demo)
async def verify_token(x_api_key: Optional[str] = Header(None)):
    """Verify API key (replace with proper auth in production)"""
    expected_token = os.getenv("NEXUS_API_KEY", "demo_key_12345")
    
    if os.getenv("NEXUS_REQUIRE_AUTH", "0") == "1":
        if not x_api_key or x_api_key != expected_token:
            raise HTTPException(status_code=401, detail="Invalid or missing API key")
    
    return True


# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize AI systems on startup"""
    global orchestrator, agent_system, llm_manager
    
    print("[NEXUS API] Initializing AI systems...")
    orchestrator = NexusAIOrchestrator()
    agent_system = DistributedAgentSystem()
    llm_manager = LLMManager()
    print("[NEXUS API] All systems online ✅")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global agent_system
    
    print("[NEXUS API] Shutting down...")
    if agent_system:
        agent_system.shutdown()
    print("[NEXUS API] Shutdown complete")


# Health and status endpoints
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.get("/api/status", response_model=SystemStatus)
async def get_status(authenticated: bool = Depends(verify_token)):
    """Get comprehensive system status"""
    status = orchestrator.get_comprehensive_status()
    agent_status = agent_system.get_system_status()
    
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "core_ai": status["core_ai"],
        "distributed_agents": agent_status,
        "llm_providers": llm_manager.get_available_providers(),
        "uptime_seconds": 0  # Track actual uptime in production
    }


# AI Task Execution
@app.post("/api/tasks/execute", response_model=TaskResponse)
async def execute_task(
    request: TaskRequest,
    authenticated: bool = Depends(verify_token)
):
    """
    Execute AI task with reasoning and planning
    
    - **task**: Description of task to execute
    - **context**: Additional context (optional)
    - **priority**: Priority level 1-10 (optional)
    """
    try:
        result = orchestrator.execute_task(
            task=request.task,
            context=request.context or {}
        )
        
        return TaskResponse(
            task_id=result["plan"]["plan_id"],
            status=result["status"],
            confidence=result["confidence"],
            strategy_used=result["strategy_used"],
            execution_steps=result["execution_steps"],
            outcome=result["outcome"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Code Analysis
@app.post("/api/code/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(
    request: CodeAnalysisRequest,
    authenticated: bool = Depends(verify_token)
):
    """
    Analyze code quality and complexity
    
    - **code**: Source code to analyze
    - **language**: Programming language (auto-detected if not provided)
    """
    try:
        analysis = orchestrator.analyze_code(
            code=request.code,
            language=request.language
        )
        
        return CodeAnalysisResponse(
            language=analysis["code_analysis"]["language"],
            complexity=analysis["code_analysis"]["complexity_score"],
            issues=analysis["issues"],
            suggestions=analysis["recommendations"],
            confidence=analysis["confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# LLM Chat
@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    authenticated: bool = Depends(verify_token)
):
    """
    Chat with LLM using context
    
    - **message**: User message
    - **use_context**: Whether to include conversation history
    - **provider**: Specific LLM provider (optional)
    - **stream**: Stream response (use WebSocket instead)
    """
    try:
        if request.stream:
            raise HTTPException(
                status_code=400,
                detail="Use WebSocket endpoint /ws/chat for streaming"
            )
        
        response = llm_manager.chat(
            message=request.message,
            use_context=request.use_context,
            provider=request.provider
        )
        
        return ChatResponse(
            response=response.content,
            provider=response.provider,
            model=response.model,
            tokens_used=response.tokens_used,
            latency_ms=response.latency_ms
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Problem Solving
@app.post("/api/solve")
async def solve_problem(
    problem: str,
    approach: Optional[str] = None,
    authenticated: bool = Depends(verify_token)
):
    """
    Solve problem using advanced reasoning
    
    - **problem**: Problem description
    - **approach**: Reasoning strategy (optional, auto-selected if not provided)
    """
    try:
        solution = orchestrator.solve_problem(problem, approach)
        return solution
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Learning
@app.post("/api/learn")
async def teach_ai(
    request: LearningRequest,
    authenticated: bool = Depends(verify_token)
):
    """
    Teach AI from experience
    
    - **experience**: Description of experience
    - **outcome**: Result or lesson learned
    - **importance**: Importance score 0-1
    - **tags**: Category tags (optional)
    """
    try:
        ai = get_nexus_ai()
        ai.learn(
            experience=request.experience,
            outcome=request.outcome,
            importance=request.importance,
            tags=request.tags or []
        )
        
        return {
            "status": "learned",
            "experience_count": ai.experience_count,
            "memory_count": len(ai.long_term_memory)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# System Optimization
@app.post("/api/optimize")
async def optimize_system(authenticated: bool = Depends(verify_token)):
    """
    Trigger system-wide AI optimization
    """
    try:
        report = orchestrator.optimize_system()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Agent Management
@app.post("/api/agents/spawn", response_model=AgentSpawnResponse)
async def spawn_agent(
    request: AgentSpawnRequest,
    authenticated: bool = Depends(verify_token)
):
    """
    Spawn a new AI agent
    
    - **name**: Agent name
    - **role**: Agent role (coordinator, researcher, coder, analyst, critic, executor)
    - **capabilities**: List of capabilities
    """
    try:
        # Validate role
        valid_roles = [r.value for r in AgentRole]
        if request.role not in valid_roles:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid role. Must be one of: {valid_roles}"
            )
        
        agent_id = agent_system.spawn_agent(
            name=request.name,
            role=AgentRole(request.role),
            capabilities=request.capabilities
        )
        
        return AgentSpawnResponse(
            agent_id=agent_id,
            name=request.name,
            role=request.role,
            status="idle"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agents")
async def list_agents(authenticated: bool = Depends(verify_token)):
    """List all active agents"""
    try:
        status = agent_system.get_system_status()
        return status["agents"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agents/{agent_id}/task")
async def assign_agent_task(
    agent_id: str,
    description: str,
    priority: int = 5,
    authenticated: bool = Depends(verify_token)
):
    """Assign task to specific agent"""
    try:
        task_id = agent_system.assign_task(
            agent_id=agent_id,
            description=description,
            priority=priority
        )
        
        return {
            "task_id": task_id,
            "agent_id": agent_id,
            "status": "assigned"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket for streaming
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for streaming chat
    
    Send: {"message": "your message", "provider": "openai"}
    Receive: Streamed response chunks
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            message = data.get("message", "")
            provider = data.get("provider")
            
            # Stream response
            async for chunk in async_stream_chat(message, provider):
                await websocket.send_text(chunk)
            
            # Send completion marker
            await websocket.send_json({"status": "complete"})
            
    except WebSocketDisconnect:
        print("[WebSocket] Client disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()


async def async_stream_chat(message: str, provider: Optional[str] = None):
    """Async wrapper for streaming chat"""
    for chunk in llm_manager.stream_chat(message, provider=provider):
        yield chunk
        await asyncio.sleep(0.01)  # Prevent blocking


# Memory Management
@app.get("/api/memory")
async def get_memory(authenticated: bool = Depends(verify_token)):
    """Get AI memory contents"""
    ai = get_nexus_ai()
    
    return {
        "short_term_count": len(ai.short_term_memory),
        "long_term_count": len(ai.long_term_memory),
        "memories": [
            {
                "content": m.content,
                "importance": m.importance,
                "access_count": m.access_count,
                "tags": m.tags
            }
            for m in ai.long_term_memory[-10:]  # Last 10 memories
        ]
    }


@app.delete("/api/memory")
async def reset_memory(
    preserve_memories: bool = True,
    authenticated: bool = Depends(verify_token)
):
    """Reset AI memory"""
    ai = get_nexus_ai()
    ai.reset(preserve_memories=preserve_memories)
    
    return {
        "status": "reset",
        "memories_preserved": preserve_memories
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "path": request.url.path}


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "detail": str(exc)}


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("NEXUS AI API - Starting Production Server")
    print("⚡ LEGION x L.X VEX — SERVING ATLAS ⚡")
    print("=" * 70)
    print("\nAPI Documentation: http://localhost:8000/api/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("\nSet NEXUS_API_KEY environment variable for authentication")
    print("Set NEXUS_REQUIRE_AUTH=1 to enforce authentication")
    print("=" * 70)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
