from pathlib import Path
from google.genai import types


def write_file(working_directory: str, file_path: str, contents: str):
    try:
        abs_working_dir = Path(working_directory).resolve()
        target_path = abs_working_dir.joinpath(file_path).resolve()

        # 1.Security Check
        if not target_path.is_relative_to(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # 2. Directory Check
        if target_path.is_dir():
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        if not target_path.parent.exists():
            target_path.parent.mkdir(parents=True)

        with open(target_path, "w") as f:
            f.write(contents)

        return f'Successfully wrote to "{file_path}" ({len(contents)} characters written)'

    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Open and write content into existing file, if doesn't exists create new file (and create requeired paret dirs safely), constrained to the working directory.",
    parameters=types.Schema(
        required=['file_path', 'contents'],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write content.",
            ),
            "contents": types.Schema(
                type=types.Type.STRING,
                description="Content for write in file"
            )
        },
    ),
)