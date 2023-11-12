# AI Baseball Coach

[![CI](https://github.com/susumutomita/ai-baseball-coach/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/susumutomita/ai-baseball-coach/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/susumutomita/ai-baseball-coach/graph/badge.svg?token=jQWnU0GsXp)](https://codecov.io/gh/susumutomita/ai-baseball-coach)

## Overview

This project aims to assist baseball coaching efforts through the use of AI. It integrates team rules and responds to specific coaching queries.

## Requirements

- Python 3.x
- Transformers Library
- Authlib
- Flask
- flask-restx

## Installation

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Setting up Auth0

Use the following script to configure Auth0:

```bash
tool/infrastructure/build.sh
```

For more details, refer to [README.md](tool/infrastructure/README.md).

## Usage

1. Write down your team's rules in Markdown format in a file named `team_rules.md`.
2. Provide a prompt template for text generation in a file named `prompt_template.txt`.
3. Run `main.py`.

```bash
python main.py
```

## Docker

You can also run the application using Docker. Set your Auth0 information as environment variables in the docker-compose.yaml file and run:

```bash
docker compose build && docker compose up
```
