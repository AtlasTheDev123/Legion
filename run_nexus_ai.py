#!/usr/bin/env python3
"""
NEXUS AI Model - Demo Runner
=============================
Run comprehensive demonstrations of the next-gen AI model
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import demo_orchestrator


if __name__ == "__main__":
    print("\n🚀 Starting NEXUS AI Model Demonstration...\n")
    demo_orchestrator()
    print("\n✅ Demo complete!\n")
