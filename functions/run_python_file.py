import subprocess
from pathlib import Path
from google.genai import types


def run_python_file(working_directory: str, file_path: str, args=None):
    try:
        abs_working_dir = Path(working_directory).resolve()
        target_path = abs_working_dir.joinpath(file_path).resolve()

        # 1.Security Check
        if not target_path.is_relative_to(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # 2. File Check
        if not target_path.is_file():
            return f'Error: "{file_path}" does not exist'

        # 3. Python file check
        if not target_path.suffix == '.py':
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]   # Now target_path = PosixPath

        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=abs_working_dir, capture_output=True, text=True, timeout=30)

        output_string = []

        if exitcode := result.returncode != 0:
            output_string.append(f"Process exited with code {exitcode}")
        if not result.stdout and not result.stderr:
            output_string = ["No output produced"]
        if result.stdout:
            output_string.append(f"STDOUT:\n {result.stdout}")
        if result.stderr:
            output_string.append(f"STDERR:\n {result.stderr}")
        return "\n".join(output_string)

    except Exception as e:
        return f'Error: executing Python file: {e}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run Python file with the python interpreter. Accept additional CLI arguments as an optional array.",
    parameters=types.Schema(
        required=['file_path'],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                nullable=True,
                description="An optional array of strings to be used as the CLI args for the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="individual arguments"
                )
            )
        },
    ),
)