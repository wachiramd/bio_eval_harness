# Bio-Eval Harness

Automated red-teaming evaluation framework designed to compare Large Language Model (LLM) safety responses between **English** and **Kiswahili**.

## Overview

This tool automates the process of "red-teaming" AI models by simulating a conversation between an **Attacker** or a **Prober**(curious user seeking harmful info) and a **Target** (the model being evaluated). It specifically tests for:
- **Refusal Rates**: Does the model refuse harmful requests?
- **Language Disparity**: Are safety filters equally effective in Swahili compared to English?
- **Depth of Harm**: If the model complies, how detailed is the harmful information?

The specific test case currently implemented involves extracting toxins from *Euphorbia tirucalli* (Pencil Cactus).

## Features

- **Dual-Language Evaluation**: Runs parallel tracks in English (`Track_EN`) and Swahili (`Track_SW`).
- **NVIDIA NIM Integration**: Uses NVIDIA's hosted API for high-performance inference (compatible with OpenAI client).
- **Automated Judging**: Uses an LLM "Judge" to detect refusals dynamically.
- **Robust Error Handling**: Includes retry logic for rate limits (429 errors).
- **Structured Logging**: Outputs detailed JSON logs and readable Markdown conversation reports.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wachiramd/bio_eval_harness.git
   cd bio_eval_harness
   ```

2. **Install dependencies**:
   ```bash
   pip install openai python-dotenv
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory with your NVIDIA API keys:
   ```env
   NVIDIA_API_KEY_PROBER=nvapi-...
   NVIDIA_API_KEY_TARGET=nvapi-...
   # Or use a single key for both:
   # NVIDIA_API_KEY=nvapi-...
   ```

## Usage

### Run the Evaluation
To start the evaluation harness:
```bash
python3 bio_eval_harness.py
```
*Optional arguments:*
- `--mock`: Run in mock mode without making real API calls.
- `--prober <model_id>`: Specify a different prober model.
- `--target <model_id>`: Specify a different target model.

### View Results
The raw results are saved to `bio_eval_results.json`. To generate a readable report:
```bash
python3 convert_results.py
```
This creates `conversation_log.md`, which you can view in any Markdown viewer.

## Default Models
- **Prober (Attacker)**: `mistralai/mistral-large-2-instruct` (via NIM)
- **Target (Victim)**: `nvidia/llama-3.1-nemotron-70b-instruct` (via NIM)

## Key Files
- `bio_eval_harness.py`: Main execution script.
- `prompts.py`: System prompts for Attacker, Target, and Judge (EN/SW).
- `convert_results.py`: Utility to format JSON logs into Markdown.
