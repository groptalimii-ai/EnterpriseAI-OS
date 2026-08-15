#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EnterpriseAI-OS Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("backend/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="enterpriseai-os",
    version="1.0.0",
    author="FHNUDAH",
    author_email="contact@fhnudah.com",
    description="EnterpriseAI-OS - AI-Powered Enterprise Management System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FHNUDAH/EnterpriseAI-OS",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0",
            "pytest-asyncio>=0.23",
            "black>=24.0",
            "flake8>=7.0",
            "mypy>=1.10",
        ],
        "gpu": [
            "torch[cuda]>=2.3",
        ],
    },
)
