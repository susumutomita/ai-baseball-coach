# AI Baseball Coach

[![CI](https://github.com/susumutomita/ai-baseball-coach/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/susumutomita/ai-baseball-coach/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/susumutomita/ai-baseball-coach/graph/badge.svg?token=jQWnU0GsXp)](https://codecov.io/gh/susumutomita/ai-baseball-coach)

## Overview

This project aims to assist baseball coaching efforts through the use of AI. It incorporates team rules and responds to specific coaching queries.

## Requirements

- Python 3.x
- Transformers Library

## Installation

Install the required Python package using pip:

```bash
pip install transformers
```

## Usage

1. Write down your team's rules in Markdown format in a file named `team_rules.md`.
2. Provide a prompt template for text generation in a file named `prompt_template.txt`.
3. Run `main.py`.

```bash
python main.py
```

### Download and Quantize the Official Facebook Model

1. Download the model from [Facebook's Llama repository](https://github.com/facebookresearch/llama).
2. Convert and quantize the downloaded model using [llama.cpp](https://github.com/ggerganov/llama.cpp).

For detailed instructions, please refer to [Detailed_Instructions.md](Detailed_Instructions.md).
