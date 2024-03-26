import csv
import sys
from utils.fo_json import index_docs

def update_csvfile(filepath: str) -> None:
    try:
        # Increase the maximum field size limit
        csv.field_size_limit(sys.maxsize)
        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            print("CSV read as json")
            # Convert CSV rows to list of dicts
            docs = list(reader)
            if not docs:
                print("CSV file is empty")
                return
            file_name = filepath.split("/")[-1].split(".")[0]
            # Set _id for opensearch and the filename of the csv
            for index, doc in enumerate(docs):
                if(index == 0):
                    print(doc)
                doc['_id'] = f"{filepath}-{doc.get('id', 'unknown')}"
                doc['file_name'] = file_name
            print("CSV indexing docs")
            index_docs(docs)
    except Exception as e:
        print(f"Error decoding CSV: {e}")
