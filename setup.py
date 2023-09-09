from setuptools import setup

setup(
    name="ai-baseballcoach",
    version="0.1",
    packages=[
        "app",
    ],
    install_requires=[
        "pytest-watch",
    ],
    entry_points={
        "console_scripts": [
            "ai-baseballcoach=app.main:main",
        ],
    },
)
