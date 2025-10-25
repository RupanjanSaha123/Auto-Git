# setup.py - Package configuration for GitScheduler

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gitscheduler",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Schedule your git commits and pushes for later execution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gitscheduler",
    py_modules=["gitscheduler"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "gitpython>=3.1.40",
        "apscheduler>=3.10.4",
        "click>=8.1.7",
        "python-dateutil>=2.8.2",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "gitscheduler=gitscheduler:cli",
        ],
    },
)
