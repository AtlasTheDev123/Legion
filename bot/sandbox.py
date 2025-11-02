"""Sandboxed simulator — returns canned, non-actionable outputs for safe testing."""
import time

def simulate_execution(function_name: str, params: dict) -> dict:
    # lightweight simulation: echo inputs + fake status
    time.sleep(0.05)
    return {
        'function': function_name,
        'status': 'simulated',
        'input': params,
        'result': f"Simulated result for {function_name}"
    }
