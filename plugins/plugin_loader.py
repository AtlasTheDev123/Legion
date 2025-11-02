"""Simple dynamic plugin loader (imports plugins from `plugins/` directory)."""
import importlib
import pkgutil


def discover_plugins():
    plugins = []
    for finder, name, ispkg in pkgutil.iter_modules(['plugins']):
        try:
            mod = importlib.import_module('plugins.' + name)
            plugins.append(mod)
        except Exception:
            continue
    return plugins
