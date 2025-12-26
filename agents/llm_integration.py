"""
LLM Integration Layer for NEXUS AI
===================================
Provides unified interface to multiple LLM providers:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Local models (Ollama, LlamaCpp)
- Custom endpoints

Supports streaming, function calling, and context management.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional, Iterator, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
from abc import ABC, abstractmethod


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    CUSTOM = "custom"


@dataclass
class LLMMessage:
    """Structured message for LLM conversation"""
    role: str  # system, user, assistant
    content: str
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None


@dataclass
class LLMResponse:
    """Structured LLM response"""
    content: str
    model: str
    provider: str
    tokens_used: int
    finish_reason: str
    latency_ms: float
    function_calls: Optional[List[Dict[str, Any]]] = None
    raw_response: Optional[Dict[str, Any]] = None


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key
        self.model = model
        
    @abstractmethod
    def complete(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """Generate completion"""
        pass
    
    @abstractmethod
    def stream(self, messages: List[LLMMessage], **kwargs) -> Iterator[str]:
        """Stream completion"""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider implementation"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        super().__init__(api_key or os.getenv("OPENAI_API_KEY"), model)
        self.has_openai = False
        
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
            self.has_openai = True
        except ImportError:
            print("[LLM] OpenAI library not installed. Install with: pip install openai")
    
    def complete(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """Generate completion using OpenAI API"""
        if not self.has_openai:
            return self._mock_response("OpenAI not available - install openai library")
        
        if not self.api_key:
            return self._mock_response("OpenAI API key not configured")
        
        start_time = time.time()
        
        try:
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000),
                top_p=kwargs.get("top_p", 1.0),
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=response.model,
                provider="openai",
                tokens_used=response.usage.total_tokens,
                finish_reason=response.choices[0].finish_reason,
                latency_ms=latency_ms,
                raw_response=response.model_dump()
            )
            
        except Exception as e:
            return self._mock_response(f"OpenAI error: {str(e)}")
    
    def stream(self, messages: List[LLMMessage], **kwargs) -> Iterator[str]:
        """Stream completion using OpenAI API"""
        if not self.has_openai or not self.api_key:
            yield "[OpenAI streaming not available]"
            return
        
        try:
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
            
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                stream=True,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000),
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"[Streaming error: {str(e)}]"
    
    def _mock_response(self, message: str) -> LLMResponse:
        """Generate mock response for testing"""
        return LLMResponse(
            content=f"[SIMULATED] {message}",
            model=self.model,
            provider="openai_mock",
            tokens_used=0,
            finish_reason="simulated",
            latency_ms=0.0
        )


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider implementation"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        super().__init__(api_key or os.getenv("ANTHROPIC_API_KEY"), model)
        self.has_anthropic = False
        
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.has_anthropic = True
        except ImportError:
            print("[LLM] Anthropic library not installed. Install with: pip install anthropic")
    
    def complete(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """Generate completion using Anthropic API"""
        if not self.has_anthropic:
            return self._mock_response("Anthropic not available - install anthropic library")
        
        if not self.api_key:
            return self._mock_response("Anthropic API key not configured")
        
        start_time = time.time()
        
        try:
            # Extract system message if present
            system_msg = None
            user_messages = []
            
            for msg in messages:
                if msg.role == "system":
                    system_msg = msg.content
                else:
                    user_messages.append({"role": msg.role, "content": msg.content})
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.7),
                system=system_msg if system_msg else None,
                messages=user_messages
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            return LLMResponse(
                content=response.content[0].text,
                model=response.model,
                provider="anthropic",
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                finish_reason=response.stop_reason,
                latency_ms=latency_ms,
                raw_response={"id": response.id, "usage": asdict(response.usage)}
            )
            
        except Exception as e:
            return self._mock_response(f"Anthropic error: {str(e)}")
    
    def stream(self, messages: List[LLMMessage], **kwargs) -> Iterator[str]:
        """Stream completion using Anthropic API"""
        if not self.has_anthropic or not self.api_key:
            yield "[Anthropic streaming not available]"
            return
        
        try:
            system_msg = None
            user_messages = []
            
            for msg in messages:
                if msg.role == "system":
                    system_msg = msg.content
                else:
                    user_messages.append({"role": msg.role, "content": msg.content})
            
            with self.client.messages.stream(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.7),
                system=system_msg if system_msg else None,
                messages=user_messages
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            yield f"[Streaming error: {str(e)}]"
    
    def _mock_response(self, message: str) -> LLMResponse:
        """Generate mock response for testing"""
        return LLMResponse(
            content=f"[SIMULATED] {message}",
            model=self.model,
            provider="anthropic_mock",
            tokens_used=0,
            finish_reason="simulated",
            latency_ms=0.0
        )


class OllamaProvider(BaseLLMProvider):
    """Ollama local model provider"""
    
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        super().__init__(None, model)
        self.base_url = base_url
        self.has_requests = False
        
        try:
            import requests
            self.requests = requests
            self.has_requests = True
        except ImportError:
            print("[LLM] requests library not installed. Install with: pip install requests")
    
    def complete(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        """Generate completion using Ollama"""
        if not self.has_requests:
            return self._mock_response("Requests library not available")
        
        start_time = time.time()
        
        try:
            # Convert messages to prompt
            prompt = self._messages_to_prompt(messages)
            
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get("temperature", 0.7),
                        "num_predict": kwargs.get("max_tokens", 2000)
                    }
                },
                timeout=60
            )
            
            response.raise_for_status()
            data = response.json()
            
            latency_ms = (time.time() - start_time) * 1000
            
            return LLMResponse(
                content=data.get("response", ""),
                model=self.model,
                provider="ollama",
                tokens_used=data.get("eval_count", 0),
                finish_reason="complete",
                latency_ms=latency_ms,
                raw_response=data
            )
            
        except Exception as e:
            return self._mock_response(f"Ollama error: {str(e)}")
    
    def stream(self, messages: List[LLMMessage], **kwargs) -> Iterator[str]:
        """Stream completion using Ollama"""
        if not self.has_requests:
            yield "[Ollama streaming not available]"
            return
        
        try:
            prompt = self._messages_to_prompt(messages)
            
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": True,
                    "options": {
                        "temperature": kwargs.get("temperature", 0.7),
                        "num_predict": kwargs.get("max_tokens", 2000)
                    }
                },
                stream=True,
                timeout=60
            )
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        yield data["response"]
                        
        except Exception as e:
            yield f"[Streaming error: {str(e)}]"
    
    def _messages_to_prompt(self, messages: List[LLMMessage]) -> str:
        """Convert messages to single prompt"""
        prompt_parts = []
        for msg in messages:
            if msg.role == "system":
                prompt_parts.append(f"System: {msg.content}")
            elif msg.role == "user":
                prompt_parts.append(f"User: {msg.content}")
            elif msg.role == "assistant":
                prompt_parts.append(f"Assistant: {msg.content}")
        return "\n\n".join(prompt_parts)
    
    def _mock_response(self, message: str) -> LLMResponse:
        """Generate mock response for testing"""
        return LLMResponse(
            content=f"[SIMULATED] {message}",
            model=self.model,
            provider="ollama_mock",
            tokens_used=0,
            finish_reason="simulated",
            latency_ms=0.0
        )


class LLMManager:
    """
    Unified LLM management with automatic provider selection,
    fallback handling, and context management
    """
    
    def __init__(self, default_provider: str = "openai"):
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.default_provider = default_provider
        self.context_history: List[LLMMessage] = []
        self.max_context_messages = 20
        
        # Initialize available providers
        self._init_providers()
        
    def _init_providers(self):
        """Initialize all available LLM providers"""
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            self.providers["openai"] = OpenAIProvider()
            print("[LLM Manager] OpenAI provider initialized")
        
        # Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            self.providers["anthropic"] = AnthropicProvider()
            print("[LLM Manager] Anthropic provider initialized")
        
        # Ollama (local)
        self.providers["ollama"] = OllamaProvider()
        print("[LLM Manager] Ollama provider initialized")
        
        if not self.providers:
            print("[LLM Manager] Warning: No LLM providers configured. Set API keys in environment.")
    
    def complete(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        provider: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate completion with automatic provider selection
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            provider: Specific provider to use (or default)
            **kwargs: Additional parameters
            
        Returns:
            LLMResponse object
        """
        messages = []
        
        if system_prompt:
            messages.append(LLMMessage(role="system", content=system_prompt))
        
        messages.append(LLMMessage(role="user", content=prompt))
        
        # Select provider
        provider_name = provider or self.default_provider
        if provider_name not in self.providers:
            provider_name = list(self.providers.keys())[0] if self.providers else None
        
        if not provider_name:
            return LLMResponse(
                content="[ERROR] No LLM providers available",
                model="none",
                provider="none",
                tokens_used=0,
                finish_reason="error",
                latency_ms=0.0
            )
        
        # Generate completion
        response = self.providers[provider_name].complete(messages, **kwargs)
        
        # Update context
        self.context_history.extend(messages)
        self.context_history.append(
            LLMMessage(role="assistant", content=response.content)
        )
        self._trim_context()
        
        return response
    
    def chat(
        self,
        message: str,
        provider: Optional[str] = None,
        use_context: bool = True,
        **kwargs
    ) -> LLMResponse:
        """
        Chat with context retention
        
        Args:
            message: User message
            provider: Specific provider to use
            use_context: Whether to include conversation history
            **kwargs: Additional parameters
            
        Returns:
            LLMResponse object
        """
        messages = []
        
        if use_context:
            messages = self.context_history.copy()
        
        messages.append(LLMMessage(role="user", content=message))
        
        provider_name = provider or self.default_provider
        if provider_name not in self.providers:
            provider_name = list(self.providers.keys())[0] if self.providers else None
        
        if not provider_name:
            return LLMResponse(
                content="[ERROR] No LLM providers available",
                model="none",
                provider="none",
                tokens_used=0,
                finish_reason="error",
                latency_ms=0.0
            )
        
        response = self.providers[provider_name].complete(messages, **kwargs)
        
        # Update context
        self.context_history.append(LLMMessage(role="user", content=message))
        self.context_history.append(
            LLMMessage(role="assistant", content=response.content)
        )
        self._trim_context()
        
        return response
    
    def stream_chat(
        self,
        message: str,
        provider: Optional[str] = None,
        use_context: bool = True,
        **kwargs
    ) -> Iterator[str]:
        """
        Stream chat response with context
        
        Args:
            message: User message
            provider: Specific provider to use
            use_context: Whether to include conversation history
            **kwargs: Additional parameters
            
        Yields:
            Response chunks
        """
        messages = []
        
        if use_context:
            messages = self.context_history.copy()
        
        messages.append(LLMMessage(role="user", content=message))
        
        provider_name = provider or self.default_provider
        if provider_name not in self.providers:
            provider_name = list(self.providers.keys())[0] if self.providers else None
        
        if not provider_name:
            yield "[ERROR] No LLM providers available"
            return
        
        full_response = []
        for chunk in self.providers[provider_name].stream(messages, **kwargs):
            full_response.append(chunk)
            yield chunk
        
        # Update context
        self.context_history.append(LLMMessage(role="user", content=message))
        self.context_history.append(
            LLMMessage(role="assistant", content="".join(full_response))
        )
        self._trim_context()
    
    def _trim_context(self):
        """Trim context to max length, preserving system messages"""
        if len(self.context_history) <= self.max_context_messages:
            return
        
        # Keep system messages
        system_msgs = [m for m in self.context_history if m.role == "system"]
        other_msgs = [m for m in self.context_history if m.role != "system"]
        
        # Keep most recent messages
        trimmed = system_msgs + other_msgs[-(self.max_context_messages - len(system_msgs)):]
        self.context_history = trimmed
    
    def reset_context(self):
        """Clear conversation context"""
        self.context_history = []
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    def set_default_provider(self, provider: str):
        """Set default provider"""
        if provider in self.providers:
            self.default_provider = provider
        else:
            raise ValueError(f"Provider '{provider}' not available")


if __name__ == "__main__":
    print("=" * 70)
    print("LLM INTEGRATION - Demo")
    print("=" * 70)
    
    manager = LLMManager()
    
    print(f"\nAvailable providers: {manager.get_available_providers()}")
    
    # Demo 1: Simple completion
    print("\n[DEMO 1] Simple Completion:")
    response = manager.complete(
        prompt="Explain what NEXUS AI is in one sentence.",
        system_prompt="You are a helpful AI assistant."
    )
    print(f"Provider: {response.provider}")
    print(f"Model: {response.model}")
    print(f"Response: {response.content}")
    print(f"Tokens: {response.tokens_used}")
    print(f"Latency: {response.latency_ms:.0f}ms")
    
    # Demo 2: Chat with context
    print("\n[DEMO 2] Chat with Context:")
    r1 = manager.chat("What is 2+2?")
    print(f"Q: What is 2+2?")
    print(f"A: {r1.content}\n")
    
    r2 = manager.chat("What about multiplying that by 3?")
    print(f"Q: What about multiplying that by 3?")
    print(f"A: {r2.content}")
    
    print(f"\nContext length: {len(manager.context_history)} messages")
    
    print("\n" + "=" * 70)
    print("⚡ LLM Integration Ready ⚡")
    print("=" * 70)
