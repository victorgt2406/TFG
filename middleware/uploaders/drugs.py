import json
import asyncio

if __name__ == "__main__":
    import sys
    sys.path.append("/home/vic/personal-ws/TFG/middleware")
    print(sys.path)
    from utils import index_docs

    async def upload_to_opensearch():
        with open('data/drugs.json', 'r', encoding="utf-8") as file:
            docs:list[dict] = json.load(file)

        docs = list(map(lambda doc: {"_id": doc["drug_name"],**doc},docs))

        def divide_list(arr: list, n: int):
            return [arr[i:i + n] for i in range(0, len(arr), n)]

        div_docs = divide_list(docs, 500)
        len_div_docs = len(div_docs)
        for i, div_doc in enumerate(div_docs):
            index_docs(div_doc)
            await asyncio.sleep(2)
            print(f"{i+1}/{len_div_docs} indexed.")

    asyncio.run(upload_to_opensearch())