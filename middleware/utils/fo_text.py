from utils import index_docs


def update_textfile(filepath: str) -> None:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            file_content = file.read()
            # Ensure file_content is not empty
            if not file_content.strip():
                print("File is empty")
                return
            file_name = filepath.split("/")[-1].split(".")[0]
            doc = {
                "_id": filepath,
                "file_name": file_name,
                "text": file_content
            }
        index_docs([doc])
    except Exception as e:
        print(f"Error decoding Txt: {e}")
