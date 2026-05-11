"""Database persistence layer for Legion Core Claw."""

from sqlalchemy import create_engine, Column, String, DateTime, JSON, Text, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class AgentModel(Base):
    """Database model for agents."""
    __tablename__ = 'agents'

    id = Column(String(255), primary_key=True)
    role = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default='idle')
    config = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = Column(DateTime, nullable=True)

    # Relationships
    tasks = relationship("TaskModel", back_populates="agent", cascade="all, delete-orphan")


class TaskModel(Base):
    """Database model for tasks."""
    __tablename__ = 'tasks'

    id = Column(String(255), primary_key=True)
    agent_id = Column(String(255), ForeignKey('agents.id'), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default='pending')
    dependencies = Column(JSON, nullable=True)  # List of task IDs
    parameters = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    agent = relationship("AgentModel", back_populates="tasks")


class ExecutionModel(Base):
    """Database model for execution history."""
    __tablename__ = 'executions'

    id = Column(String(255), primary_key=True)
    task_id = Column(String(255), ForeignKey('tasks.id'), nullable=True)
    tool_name = Column(String(100), nullable=False)
    parameters = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    status = Column(String(50), nullable=False)
    execution_time = Column(Integer, nullable=True)  # milliseconds
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLogModel(Base):
    """Database model for audit logs."""
    __tablename__ = 'audit_logs'

    id = Column(String(255), primary_key=True)
    event_type = Column(String(100), nullable=False)
    actor = Column(String(255), nullable=False)
    action = Column(String(255), nullable=False)
    resource = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """Database connection and session management."""

    def __init__(self, connection_string: str = "sqlite:///legion.db"):
        """
        Initialize database manager.

        Args:
            connection_string: Database connection string
        """
        self.connection_string = connection_string
        self.engine = None
        self.SessionLocal = None

    def initialize(self) -> None:
        """Initialize database connection and create tables."""
        try:
            self.engine = create_engine(
                self.connection_string,
                pool_pre_ping=True,
                echo=False  # Set to True for SQL debugging
            )

            # Create tables
            Base.metadata.create_all(bind=self.engine)

            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

            logger.info(f"Database initialized: {self.connection_string}")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def get_session(self):
        """Get database session."""
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self.SessionLocal()

    def close(self) -> None:
        """Close database connections."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")


class AgentRepository:
    """Repository for agent data operations."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def save_agent(self, agent_data: Dict[str, Any]) -> None:
        """Save agent to database."""
        with self.db_manager.get_session() as session:
            agent = AgentModel(
                id=agent_data['agent_id'],
                role=agent_data['role'],
                status=agent_data['status'],
                config=agent_data.get('config', {}),
                last_active=datetime.utcnow()
            )
            session.merge(agent)  # Insert or update
            session.commit()

    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID."""
        with self.db_manager.get_session() as session:
            agent = session.query(AgentModel).filter(AgentModel.id == agent_id).first()
            if agent:
                return {
                    'agent_id': agent.id,
                    'role': agent.role,
                    'status': agent.status,
                    'config': agent.config,
                    'created_at': agent.created_at.isoformat(),
                    'last_active': agent.last_active.isoformat() if agent.last_active else None
                }
            return None

    def list_agents(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all agents, optionally filtered by status."""
        with self.db_manager.get_session() as session:
            query = session.query(AgentModel)
            if status:
                query = query.filter(AgentModel.status == status)

            agents = query.all()
            return [{
                'agent_id': agent.id,
                'role': agent.role,
                'status': agent.status,
                'created_at': agent.created_at.isoformat(),
                'last_active': agent.last_active.isoformat() if agent.last_active else None
            } for agent in agents]

    def update_agent_status(self, agent_id: str, status: str) -> None:
        """Update agent status."""
        with self.db_manager.get_session() as session:
            agent = session.query(AgentModel).filter(AgentModel.id == agent_id).first()
            if agent:
                agent.status = status
                agent.last_active = datetime.utcnow()
                session.commit()

    def delete_agent(self, agent_id: str) -> None:
        """Delete agent."""
        with self.db_manager.get_session() as session:
            agent = session.query(AgentModel).filter(AgentModel.id == agent_id).first()
            if agent:
                session.delete(agent)
                session.commit()


class TaskRepository:
    """Repository for task data operations."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def save_task(self, task_data: Dict[str, Any]) -> None:
        """Save task to database."""
        with self.db_manager.get_session() as session:
            task = TaskModel(
                id=task_data['task_id'],
                agent_id=task_data['agent_id'],
                description=task_data['description'],
                status=task_data['status'],
                dependencies=task_data.get('dependencies', []),
                parameters=task_data.get('parameters', {}),
                result=task_data.get('result'),
                error=task_data.get('error'),
                started_at=task_data.get('started_at'),
                completed_at=task_data.get('completed_at')
            )
            session.merge(task)
            session.commit()

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task by ID."""
        with self.db_manager.get_session() as session:
            task = session.query(TaskModel).filter(TaskModel.id == task_id).first()
            if task:
                return {
                    'task_id': task.id,
                    'agent_id': task.agent_id,
                    'description': task.description,
                    'status': task.status,
                    'dependencies': task.dependencies or [],
                    'parameters': task.parameters or {},
                    'result': task.result,
                    'error': task.error,
                    'created_at': task.created_at.isoformat(),
                    'started_at': task.started_at.isoformat() if task.started_at else None,
                    'completed_at': task.completed_at.isoformat() if task.completed_at else None
                }
            return None

    def list_tasks(self, agent_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List tasks, optionally filtered."""
        with self.db_manager.get_session() as session:
            query = session.query(TaskModel)
            if agent_id:
                query = query.filter(TaskModel.agent_id == agent_id)
            if status:
                query = query.filter(TaskModel.status == status)

            tasks = query.all()
            return [{
                'task_id': task.id,
                'agent_id': task.agent_id,
                'description': task.description[:50] + '...' if len(task.description) > 50 else task.description,
                'status': task.status,
                'created_at': task.created_at.isoformat()
            } for task in tasks]

    def update_task_status(self, task_id: str, status: str, result: Optional[Dict] = None, error: Optional[str] = None) -> None:
        """Update task status and result."""
        with self.db_manager.get_session() as session:
            task = session.query(TaskModel).filter(TaskModel.id == task_id).first()
            if task:
                task.status = status
                if result is not None:
                    task.result = result
                if error is not None:
                    task.error = error

                if status == 'executing' and not task.started_at:
                    task.started_at = datetime.utcnow()
                elif status in ['completed', 'error'] and not task.completed_at:
                    task.completed_at = datetime.utcnow()

                session.commit()


class AuditRepository:
    """Repository for audit log operations."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def log_event(self, event_data: Dict[str, Any]) -> None:
        """Log audit event."""
        with self.db_manager.get_session() as session:
            audit_log = AuditLogModel(
                id=event_data.get('id', f"audit-{datetime.utcnow().timestamp()}"),
                event_type=event_data['event_type'],
                actor=event_data['actor'],
                action=event_data['action'],
                resource=event_data.get('resource'),
                status=event_data['status'],
                details=event_data.get('details', {}),
                ip_address=event_data.get('ip_address'),
                user_agent=event_data.get('user_agent')
            )
            session.add(audit_log)
            session.commit()

    def get_audit_trail(self, actor: Optional[str] = None, event_type: Optional[str] = None,
                       limit: int = 100) -> List[Dict[str, Any]]:
        """Get audit trail with optional filters."""
        with self.db_manager.get_session() as session:
            query = session.query(AuditLogModel).order_by(AuditLogModel.created_at.desc())

            if actor:
                query = query.filter(AuditLogModel.actor == actor)
            if event_type:
                query = query.filter(AuditLogModel.event_type == event_type)

            logs = query.limit(limit).all()
            return [{
                'id': log.id,
                'event_type': log.event_type,
                'actor': log.actor,
                'action': log.action,
                'resource': log.resource,
                'status': log.status,
                'details': log.details,
                'created_at': log.created_at.isoformat()
            } for log in logs]


# Global instances
db_manager = DatabaseManager()
agent_repo = AgentRepository(db_manager)
task_repo = TaskRepository(db_manager)
audit_repo = AuditRepository(db_manager)
