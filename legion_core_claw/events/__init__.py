"""Event system for Legion Core Claw."""

import logging
import threading
import time
import json
from typing import Dict, Any, List, Optional, Callable, Set
from abc import ABC, abstractmethod
from enum import Enum
from queue import Queue, Empty
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class EventPriority(Enum):
    """Event priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class Event:
    """Represents an event in the system."""

    def __init__(self, event_type: str, data: Dict[str, Any], source: str = "system",
                 priority: EventPriority = EventPriority.NORMAL, timestamp: Optional[float] = None):
        self.event_type = event_type
        self.data = data
        self.source = source
        self.priority = priority
        self.timestamp = timestamp or time.time()
        self.id = f"{event_type}-{int(self.timestamp * 1000000)}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            "id": self.id,
            "event_type": self.event_type,
            "data": self.data,
            "source": self.source,
            "priority": self.priority.value,
            "timestamp": self.timestamp
        }

    def __str__(self) -> str:
        return f"Event({self.event_type}, {self.source}, {self.priority.name})"


class EventHandler(ABC):
    """Abstract base class for event handlers."""

    @abstractmethod
    def handle_event(self, event: Event) -> None:
        """Handle an event."""
        pass

    @property
    @abstractmethod
    def event_types(self) -> List[str]:
        """Return list of event types this handler can process."""
        pass


class FunctionEventHandler(EventHandler):
    """Event handler that wraps a function."""

    def __init__(self, func: Callable[[Event], None], event_types: List[str]):
        self.func = func
        self._event_types = event_types

    def handle_event(self, event: Event) -> None:
        """Handle event by calling the wrapped function."""
        try:
            self.func(event)
        except Exception as e:
            logger.error(f"Error in event handler: {e}")

    @property
    def event_types(self) -> List[str]:
        """Return event types."""
        return self._event_types


class EventBus:
    """Central event bus for pub/sub messaging."""

    def __init__(self, max_queue_size: int = 1000):
        self.handlers: Dict[str, Set[EventHandler]] = {}
        self.event_queue: Queue = Queue(maxsize=max_queue_size)
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.lock = threading.RLock()

    def start(self) -> None:
        """Start the event processing thread."""
        if self.running:
            return

        self.running = True
        self.worker_thread = threading.Thread(target=self._process_events, daemon=True)
        self.worker_thread.start()
        logger.info("Event bus started")

    def stop(self) -> None:
        """Stop the event processing thread."""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        logger.info("Event bus stopped")

    def publish(self, event: Event) -> None:
        """Publish an event to the bus."""
        try:
            self.event_queue.put(event, timeout=1)
            logger.debug(f"Published event: {event}")
        except Exception as e:
            logger.error(f"Failed to publish event: {e}")

    def subscribe(self, handler: EventHandler) -> None:
        """Subscribe a handler to events."""
        with self.lock:
            for event_type in handler.event_types:
                if event_type not in self.handlers:
                    self.handlers[event_type] = set()
                self.handlers[event_type].add(handler)
                logger.debug(f"Subscribed handler to {event_type}")

    def unsubscribe(self, handler: EventHandler) -> None:
        """Unsubscribe a handler from events."""
        with self.lock:
            for event_type in handler.event_types:
                if event_type in self.handlers:
                    self.handlers[event_type].discard(handler)
                    if not self.handlers[event_type]:
                        del self.handlers[event_type]

    def _process_events(self) -> None:
        """Process events from the queue."""
        while self.running:
            try:
                event = self.event_queue.get(timeout=1)
                self._dispatch_event(event)
                self.event_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}")

    def _dispatch_event(self, event: Event) -> None:
        """Dispatch event to registered handlers."""
        with self.lock:
            handlers = self.handlers.get(event.event_type, set()).copy()

        if not handlers:
            logger.debug(f"No handlers for event type: {event.event_type}")
            return

        for handler in handlers:
            try:
                # Run handler in thread pool to avoid blocking
                executor = ThreadPoolExecutor(max_workers=10)
                executor.submit(handler.handle_event, event)
                executor.shutdown(wait=False)
            except Exception as e:
                logger.error(f"Error dispatching event to handler: {e}")


class EventStore:
    """Persistent storage for events."""

    def __init__(self, max_events: int = 10000):
        self.events: List[Event] = []
        self.max_events = max_events
        self.lock = threading.RLock()

    def store_event(self, event: Event) -> None:
        """Store an event."""
        with self.lock:
            self.events.append(event)
            # Maintain max size
            if len(self.events) > self.max_events:
                self.events.pop(0)

    def get_events(self, event_type: Optional[str] = None, limit: int = 100) -> List[Event]:
        """Get events, optionally filtered by type."""
        with self.lock:
            events = self.events
            if event_type:
                events = [e for e in events if e.event_type == event_type]
            return events[-limit:]

    def get_event_stats(self) -> Dict[str, Any]:
        """Get event statistics."""
        with self.lock:
            total_events = len(self.events)
            event_types = {}
            for event in self.events:
                event_types[event.event_type] = event_types.get(event.event_type, 0) + 1

            return {
                "total_events": total_events,
                "event_types": event_types,
                "max_events": self.max_events
            }

    def clear_events(self) -> None:
        """Clear all stored events."""
        with self.lock:
            self.events.clear()


class EventManager:
    """High-level event management system."""

    def __init__(self):
        self.event_bus = EventBus()
        self.event_store = EventStore()
        self._setup_default_handlers()

    def _setup_default_handlers(self) -> None:
        """Setup default event handlers."""

        # Handler to store all events
        def store_handler(event: Event) -> None:
            self.event_store.store_event(event)

        store_all_handler = FunctionEventHandler(store_handler, ["*"])
        self.event_bus.subscribe(store_all_handler)

        # Handler for system events
        def system_event_handler(event: Event) -> None:
            if event.event_type.startswith("system."):
                logger.info(f"System event: {event}")

        system_handler = FunctionEventHandler(system_event_handler, ["system.*"])
        self.event_bus.subscribe(system_handler)

    def start(self) -> None:
        """Start the event system."""
        self.event_bus.start()

    def stop(self) -> None:
        """Stop the event system."""
        self.event_bus.stop()

    def publish_event(self, event_type: str, data: Dict[str, Any], source: str = "system",
                     priority: EventPriority = EventPriority.NORMAL) -> None:
        """Publish an event."""
        event = Event(event_type, data, source, priority)
        self.event_bus.publish(event)

    def subscribe_to_events(self, event_types: List[str], handler_func: Callable[[Event], None]) -> EventHandler:
        """Subscribe to events with a function."""
        handler = FunctionEventHandler(handler_func, event_types)
        self.event_bus.subscribe(handler)
        return handler

    def get_recent_events(self, event_type: Optional[str] = None, limit: int = 50) -> List[Event]:
        """Get recent events."""
        return self.event_store.get_events(event_type, limit)

    def get_event_statistics(self) -> Dict[str, Any]:
        """Get event statistics."""
        return self.event_store.get_event_stats()


# Global event manager instance
event_manager = EventManager()

# Convenience functions
def publish_event(event_type: str, data: Dict[str, Any], source: str = "system",
                 priority: EventPriority = EventPriority.NORMAL) -> None:
    """Publish an event."""
    event_manager.publish_event(event_type, data, source, priority)

def subscribe_to_events(event_types: List[str], handler_func: Callable[[Event], None]) -> EventHandler:
    """Subscribe to events."""
    return event_manager.subscribe_to_events(event_types, handler_func)

def get_recent_events(event_type: Optional[str] = None, limit: int = 50) -> List[Event]:
    """Get recent events."""
    return event_manager.get_recent_events(event_type, limit)

# Agent lifecycle events
def publish_agent_spawned(agent_id: str, role: str) -> None:
    """Publish agent spawned event."""
    publish_event("agent.spawned", {"agent_id": agent_id, "role": role}, "orchestrator")

def publish_agent_terminated(agent_id: str, role: str) -> None:
    """Publish agent terminated event."""
    publish_event("agent.terminated", {"agent_id": agent_id, "role": role}, "orchestrator")

# Task events
def publish_task_created(task_id: str, agent_id: str, description: str) -> None:
    """Publish task created event."""
    publish_event("task.created", {
        "task_id": task_id,
        "agent_id": agent_id,
        "description": description
    }, "orchestrator")

def publish_task_completed(task_id: str, agent_id: str, status: str, duration: float) -> None:
    """Publish task completed event."""
    publish_event("task.completed", {
        "task_id": task_id,
        "agent_id": agent_id,
        "status": status,
        "duration": duration
    }, "orchestrator")

# Tool events
def publish_tool_executed(tool_name: str, status: str, duration: float) -> None:
    """Publish tool executed event."""
    publish_event("tool.executed", {
        "tool_name": tool_name,
        "status": status,
        "duration": duration
    }, "registry")

# System events
def publish_system_error(error_type: str, message: str, component: str) -> None:
    """Publish system error event."""
    publish_event("system.error", {
        "error_type": error_type,
        "message": message,
        "component": component
    }, "system", EventPriority.HIGH)

def publish_system_warning(message: str, component: str) -> None:
    """Publish system warning event."""
    publish_event("system.warning", {
        "message": message,
        "component": component
    }, "system", EventPriority.NORMAL)

# Start the event system
event_manager.start()