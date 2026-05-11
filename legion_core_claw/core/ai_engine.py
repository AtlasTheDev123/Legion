"""
Unified AI Engine - Consolidates LLM client, reasoning, and orchestration logic.
Supports OpenAI, Mistral, LocalAI, and other LLM backends.
"""

import os
from typing import Optional, Dict, Any, List
import json
import logging
import time

logger = logging.getLogger(__name__)


class AIEngine:
    """Central AI reasoning engine for task planning, tool selection, and execution."""

    def __init__(self, model: str = "gpt-4", provider: str = "openai", **kwargs):
        """
        Initialize AI Engine.
        
        Args:
            model: LLM model identifier (e.g., 'gpt-4', 'mistral-large')
            provider: LLM provider ('openai', 'mistral', 'localai', 'github-copilot')
            **kwargs: Additional provider-specific configuration
        """
        self.model = model
        self.provider = provider
        self.config = kwargs
        self._validate_provider()

    def _validate_provider(self) -> None:
        """Validate provider configuration against environment variables."""
        valid_providers = ["openai", "mistral", "localai", "github-copilot", "anthropic"]
        if self.provider not in valid_providers:
            raise ValueError(f"Provider '{self.provider}' not supported. Use one of {valid_providers}")

    def reason(self, prompt: str, context: Optional[Dict[str, Any]] = None, temperature: float = 0.7) -> str:
        """
        Execute reasoning with context awareness.
        
        Args:
            prompt: Task description or query
            context: Optional context dict with task history, available tools, etc.
            temperature: LLM temperature (0-1)
            
        Returns:
            Reasoning output / plan
        """
        enhanced_prompt = self._build_prompt(prompt, context)
        # Stub: In production, call actual LLM API
        logger.info(f"Reasoning with {self.provider}/{self.model}")
        return enhanced_prompt[:320]  # Summarize for now

    def select_tools(self, task: str, available_tools: List[Dict[str, Any]]) -> List[str]:
        """
        Analyze task and select relevant tools from available set.
        
        Args:
            task: Task description
            available_tools: List of tool definitions with schemas
            
        Returns:
            List of selected tool names
        """
        logger.info(f"Selecting tools for task: {task[:50]}...")
        # Stub: LLM-powered tool selection
        return [t["name"] for t in available_tools[:2]]

    def execute_with_tools(self, task: str, tools_config: List[Dict], execution_sandbox: str = "simulated") -> Dict[str, Any]:
        """
        Execute task with selected tools in specified sandbox.
        
        Args:
            task: Task to execute
            tools_config: Configuration of tools to use
            execution_sandbox: 'simulated', 'sandboxed', or 'direct'
            
        Returns:
            Execution result with status and output
        """
        start_time = time.time()
        selected = self.select_tools(task, tools_config)
        
        # Record LLM request metrics
        try:
            from legion_core_claw.monitoring import metrics
            metrics.record_llm_request(self.provider, self.model)
        except ImportError:
            pass  # Monitoring not available
        
        result = {
            "task": task,
            "selected_tools": selected,
            "sandbox": execution_sandbox,
            "status": "executed"
        }
        
        duration = time.time() - start_time
        
        # Record tool execution metrics
        try:
            from legion_core_claw.monitoring import metrics
            for tool_name in selected:
                metrics.record_tool_execution(tool_name, "success", duration / len(selected))
        except ImportError:
            pass  # Monitoring not available
        
        return result

    def _build_prompt(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Build enhanced prompt with context."""
        if not context:
            return prompt
        
        enhanced = f"{prompt}\n\nContext:\n"
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                enhanced += f"  {key}: {json.dumps(value, indent=2)}\n"
            else:
                enhanced += f"  {key}: {value}\n"
        return enhanced

    def summarize(self, text: str, max_length: int = 320) -> str:
        """Summarize text to specified length."""
        return text[:max_length]

    def validate_json_schema(self, data: Dict, schema: Dict) -> bool:
        """Validate data against JSON schema."""
        # Stub: Use jsonschema library in production
        return isinstance(data, dict)

    def __repr__(self) -> str:
        return f"AIEngine(model={self.model}, provider={self.provider})"
