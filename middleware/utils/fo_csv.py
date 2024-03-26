import csv
from utils.fo_json import index_docs

def update_csvfile(filepath: str) -> None:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            # Convert CSV rows to list of dicts
            docs = list(reader)
            if not docs:
                print("CSV file is empty")
                return
            file_name = filepath.split("/")[-1].split(".")[0]
            # Set _id for opensearch and the filename of the csv
            for doc in docs:
                doc['_id'] = f"{filepath}-{doc.get('id', 'unknown')}"
                doc['file_name'] = file_name
            index_docs(docs)
    except Exception as e:
        print(f"Error decoding CSV: {e}")
