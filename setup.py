from setuptools import setup

with open("requirements.txt", "r") as f:
    required_packages = f.read().splitlines()

setup(
    name="ai-baseballcoach",
    version="0.1",
    packages=[
        "app",
    ],
    install_requires=required_packages,
    entry_points={
        "console_scripts": [
            "ai-baseballcoach=app.main:main",
        ],
    },
)
