from pathlib import Path
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory: str, file_path: str):
    try:
        abs_working_dir = Path(working_directory).resolve()
        target_path = abs_working_dir.joinpath(file_path).resolve()

        # 1.Security Check
        if not target_path.is_relative_to(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # 2. File Check
        if not target_path.is_file():
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content_str = ""
        with open(target_path) as f:
            file_content_str = f.read(MAX_CHARS)
            if f.read(1):
                file_content_str += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_str
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Open file in a specified file path relative to the working directory, providing file content",
    parameters=types.Schema(
        required=['file_path'],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to open and provide its contents",
            ),
        },
    ),
)