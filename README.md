# ollama-text-formatter
# Local AI Text Formatter & Translator 🚀

A lightweight Python project that uses local Large Language Models (LLMs) via Ollama to process, format, and translate multi-paragraph texts into a structured bilingual format (Arabic & English).

## Features ✨
- 100% Local & Private: Runs entirely on your machine using Ollama without sending data to external cloud APIs.
- Bilingual Structuring: Automatically ensures text is available in both Arabic and English with clear labels.
- Clean Formatting: Standardizes IDs, serial numbers, and separators across all paragraphs.
- File-based Input/Output: Reads raw text from input files and outputs clean structured results.

## Prerequisites 🛠️
1. Python 3.8+ installed on your system.
2. [Ollama](https://ollama.com) installed and running locally.
3. Download the model used in the script (e.g., llama3.2):
   `bash
   ollama pull llama3.2
