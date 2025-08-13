# vibepython: AI-Powered Interactive Python Code Generator

vibepython is an interactive command-line tool that uses AI to generate executable Python code from user prompts. Powered by OpenAI or alternative providers, it allows you to create, run, and capture code outputs while maintaining a contextual history stored in JSON. Ideal for developers, experimenters, and AI enthusiasts looking for a seamless coding experience.

## Example of work

![alt text](https://raw.githubusercontent.com/OldTyT/vibepython/main/resources/img/example.png)


## Features
- **Interactive Prompting**: Enter your ideas and receive AI-generated Python code.
- **AI Code Generation**: Leverages AI models with prompt history for accurate scripts.
- **Safe Code Execution**: Run generated code and capture stdout/stderr outputs.
- **Persistent History**: Uses Pydantic models to store interactions in JSON for ongoing context.
- **Customization via Environment Variables**: Adjust settings for personalized control.
- **Docker Support**: Easy deployment in containerized environments.

## Installation

### From PyPI
1. Install the package:
   ```
   pip install vibepython
   ```
2. Run the tool:
   ```
   vibepython
   ```

### From Source
1. Clone the repository:
   ```
   git clone https://github.com/OldTyT/vibepython.git
   ```
2. Navigate to the directory:
   ```
   cd vibepython
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Launch the application:
   ```
   python3 main.py
   ```

### Using Docker
Run the container with this command:
```
docker run --rm -ti -e HISTORY_PATH=/history/history.json -v my_history:/history ghcr.io/oldtyt/vibepython
```
- Set your OpenAI API key via the `OPENAI_API_KEY` environment variable (required for the 'openai' provider).

## Usage
Start the tool and follow the prompts:
- Enter a prompt (e.g., "Write a function to calculate factorial").
- The AI generates code based on your input and history.
- Choose to execute the code (Y/N) and view captured outputs.
- All interactions are logged to history for context.

To exit, press Ctrl+C.

## Environment Variables
Customize the tool using these environment variables:
- **HISTORY_PATH**: Path to the JSON history file. Default: `history.json`.
- **HISTORY_SIZE**: Number of past interactions to include in AI context. Default: `7`.
- **OPENAI_API_KEY**: Required for the 'openai' provider; your OpenAI API key.
- **PROVIDER**: AI provider to use. Supports 'gpt4free' (default) and 'openai'.
- **MODEL_NAME**: Model to use with the provider. For 'gpt4free': 'gpt-4o'. For 'openai': 'gpt-5-mini'.

Example configuration:
```
export PROVIDER=openai
export OPENAI_API_KEY=your-api-key
export MODEL_NAME=gpt-5-mini
export HISTORY_SIZE=10
python3 main.py
```

## Dependencies
- **Python 3.10+** (Compatible up to 3.13).
- Required libraries: openai, pydantic, loguru, and others listed in `requirements.txt`.

## Contributing
Have suggestions? Open an issue or submit a pull request to help improve the project. Contributions are welcome!
