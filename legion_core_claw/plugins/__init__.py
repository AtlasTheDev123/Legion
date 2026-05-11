"""Plugin system for Legion Core Claw."""

import logging
import importlib
import inspect
from typing import Dict, Any, List, Optional, Type, Callable
from abc import ABC, abstractmethod
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


class PluginBase(ABC):
    """Base class for all plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description."""
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with configuration."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the plugin."""
        pass


class ToolPlugin(PluginBase):
    """Plugin that provides tools."""

    @abstractmethod
    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of tools provided by this plugin."""
        pass

    @abstractmethod
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool provided by this plugin."""
        pass


class InterfacePlugin(PluginBase):
    """Plugin that provides interfaces."""

    @abstractmethod
    def start_interface(self) -> None:
        """Start the interface."""
        pass

    @abstractmethod
    def stop_interface(self) -> None:
        """Stop the interface."""
        pass


class ProcessorPlugin(PluginBase):
    """Plugin that provides data processing capabilities."""

    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process input data and return result."""
        pass


class PluginManager:
    """Manages plugin loading, registration, and lifecycle."""

    def __init__(self, plugin_dirs: Optional[List[str]] = None):
        self.plugin_dirs = plugin_dirs or [
            "plugins",
            "legion_core_claw/plugins",
            str(Path(__file__).parent / "plugins")
        ]
        self.loaded_plugins: Dict[str, PluginBase] = {}
        self.plugin_configs: Dict[str, Dict[str, Any]] = {}
        self._ensure_plugin_dirs()

    def _ensure_plugin_dirs(self) -> None:
        """Ensure plugin directories exist."""
        for plugin_dir in self.plugin_dirs:
            Path(plugin_dir).mkdir(parents=True, exist_ok=True)

    def discover_plugins(self) -> List[str]:
        """Discover available plugins in plugin directories."""
        discovered_plugins = []

        for plugin_dir in self.plugin_dirs:
            plugin_path = Path(plugin_dir)
            if not plugin_path.exists():
                continue

            # Look for Python files
            for py_file in plugin_path.glob("*.py"):
                if py_file.name.startswith("__"):
                    continue

                module_name = py_file.stem
                discovered_plugins.append(f"{plugin_dir}.{module_name}")

        return discovered_plugins

    def load_plugin(self, plugin_path: str, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Load a plugin from the given path.

        Args:
            plugin_path: Path to plugin module (e.g., 'plugins.my_plugin')
            config: Plugin configuration

        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            # Import the module
            module = importlib.import_module(plugin_path)

            # Find plugin classes
            plugin_classes = []
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and
                    issubclass(obj, PluginBase) and
                    obj != PluginBase):
                    plugin_classes.append(obj)

            if not plugin_classes:
                logger.warning(f"No plugin classes found in {plugin_path}")
                return False

            # Load the first plugin class found
            plugin_class = plugin_classes[0]
            plugin_instance = plugin_class()

            # Initialize plugin
            plugin_config = config or {}
            plugin_instance.initialize(plugin_config)

            # Register plugin
            self.loaded_plugins[plugin_instance.name] = plugin_instance
            self.plugin_configs[plugin_instance.name] = plugin_config

            logger.info(f"Loaded plugin: {plugin_instance.name} v{plugin_instance.version}")
            return True

        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_path}: {e}")
            return False

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin."""
        if plugin_name not in self.loaded_plugins:
            logger.warning(f"Plugin {plugin_name} not loaded")
            return False

        try:
            plugin = self.loaded_plugins[plugin_name]
            plugin.shutdown()
            del self.loaded_plugins[plugin_name]
            del self.plugin_configs[plugin_name]
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            return False

    def get_plugin(self, plugin_name: str) -> Optional[PluginBase]:
        """Get a loaded plugin by name."""
        return self.loaded_plugins.get(plugin_name)

    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins."""
        return [
            {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "type": type(plugin).__name__
            }
            for plugin in self.loaded_plugins.values()
        ]

    def get_tools_from_plugins(self) -> List[Dict[str, Any]]:
        """Get all tools from loaded tool plugins."""
        all_tools = []
        for plugin in self.loaded_plugins.values():
            if isinstance(plugin, ToolPlugin):
                try:
                    tools = plugin.get_tools()
                    all_tools.extend(tools)
                except Exception as e:
                    logger.error(f"Failed to get tools from plugin {plugin.name}: {e}")
        return all_tools

    def execute_tool_from_plugin(self, tool_name: str, parameters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a tool from loaded plugins."""
        for plugin in self.loaded_plugins.values():
            if isinstance(plugin, ToolPlugin):
                try:
                    tools = plugin.get_tools()
                    tool_names = [t.get("name") for t in tools]
                    if tool_name in tool_names:
                        return plugin.execute_tool(tool_name, parameters)
                except Exception as e:
                    logger.error(f"Failed to execute tool {tool_name} from plugin {plugin.name}: {e}")
        return None

    def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a plugin."""
        if plugin_name not in self.loaded_plugins:
            return False

        config = self.plugin_configs[plugin_name]
        plugin_path = None

        # Find the plugin path
        for loaded_plugin in self.loaded_plugins.values():
            if loaded_plugin.name == plugin_name:
                # This is a simplified approach - in practice you'd need to track the path
                plugin_path = f"plugins.{plugin_name.lower().replace(' ', '_')}"
                break

        if not plugin_path:
            return False

        # Unload and reload
        if self.unload_plugin(plugin_name):
            return self.load_plugin(plugin_path, config)
        return False


class PluginTemplate:
    """Template for creating new plugins."""

    @staticmethod
    def create_tool_plugin_template(plugin_name: str, tools: List[Dict]) -> str:
        """Generate template code for a tool plugin."""
        template = f'''"""
{plugin_name} Tool Plugin for Legion Core Claw.
"""

from legion_core_claw.plugins import ToolPlugin
from typing import Dict, Any, List


class {plugin_name.replace(" ", "")}Plugin(ToolPlugin):
    """{plugin_name} tool plugin."""

    @property
    def name(self) -> str:
        return "{plugin_name}"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "{plugin_name} integration plugin"

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin."""
        self.config = config
        print(f"Initialized {{self.name}} plugin")

    def shutdown(self) -> None:
        """Shutdown the plugin."""
        print(f"Shutdown {{self.name}} plugin")

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of tools."""
        return {tools}

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool."""
        # Implement tool execution logic here
        return {{
            "tool": tool_name,
            "status": "executed",
            "result": "Tool executed successfully"
        }}
'''
        return template

    @staticmethod
    def create_interface_plugin_template(plugin_name: str) -> str:
        """Generate template code for an interface plugin."""
        template = f'''"""
{plugin_name} Interface Plugin for Legion Core Claw.
"""

from legion_core_claw.plugins import InterfacePlugin
from typing import Dict, Any
import threading


class {plugin_name.replace(" ", "")}InterfacePlugin(InterfacePlugin):
    """{plugin_name} interface plugin."""

    @property
    def name(self) -> str:
        return "{plugin_name}"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "{plugin_name} interface integration"

    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin."""
        self.config = config
        self.running = False
        print(f"Initialized {{self.name}} plugin")

    def shutdown(self) -> None:
        """Shutdown the plugin."""
        self.stop_interface()
        print(f"Shutdown {{self.name}} plugin")

    def start_interface(self) -> None:
        """Start the interface."""
        if not self.running:
            self.running = True
            # Start interface in a separate thread
            thread = threading.Thread(target=self._run_interface)
            thread.daemon = True
            thread.start()
            print(f"Started {{self.name}} interface")

    def stop_interface(self) -> None:
        """Stop the interface."""
        self.running = False
        print(f"Stopped {{self.name}} interface")

    def _run_interface(self) -> None:
        """Run the interface loop."""
        while self.running:
            # Implement interface logic here
            pass
'''
        return template


# Global plugin manager instance
plugin_manager = PluginManager()

# Auto-discover and load plugins on import
def _auto_load_plugins():
    """Automatically discover and load plugins."""
    try:
        discovered = plugin_manager.discover_plugins()
        for plugin_path in discovered:
            try:
                plugin_manager.load_plugin(plugin_path)
            except Exception as e:
                logger.warning(f"Failed to auto-load plugin {plugin_path}: {e}")
    except Exception as e:
        logger.warning(f"Plugin auto-loading failed: {e}")

# Auto-load plugins
_auto_load_plugins()