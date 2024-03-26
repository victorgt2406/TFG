import json
from utils import index_docs

def update_jsonfile(filepath: str) -> None:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            file_content = file.read()
            # Ensure file_content is not empty
            if not file_content.strip():
                print("File is empty")
                return
            jsonfile = json.loads(file_content)
        index_docs(jsonfile)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
