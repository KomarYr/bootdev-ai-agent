from pathlib import Path
from google.genai import types


def get_files_info(working_directory: str, directory="."):
    try:
        abs_working_dir = Path(working_directory).resolve()
        target_dir = abs_working_dir.joinpath(directory).resolve()

        # 1.Security Check
        if not target_dir.is_relative_to(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # 2. Directory Check
        if not target_dir.is_dir():
            return f'Error: "{directory}" is not a directory'

        return 'n'.join(
            f"- {item.name}: file_size={item.stat().st_size}, is_dir={item.is_dir()}"
            for item in target_dir.iterdir()
        )
    except Exception as e:
        return f'Error: {e}'


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
