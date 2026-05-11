#!/usr/bin/env python
"""Setup script for Legion Core Claw."""

from setuptools import setup, find_packages

setup(
    name="legion-core-claw",
    version="3.0.0",
    author="ATLAS",
    author_email="atlas@nexus-legion.com",
    description="Unified AI-driven DevSecOps and autonomous automation framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AtlasTheDev123/Legion",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8+",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.95.0",
        "uvicorn[standard]>=0.21.0",
        "pydantic>=1.10.0",
        "openai>=0.27.0",
        "langchain>=0.0.200",
        "python-telegram-bot>=20.0",
        "pymongo>=4.3.0",
        "cryptography>=38.0.0",
        "python-dotenv>=0.21.0",
    ],
    entry_points={
        "console_scripts": [
            "legion=legion_core_claw.main:main",
        ],
    },
)
