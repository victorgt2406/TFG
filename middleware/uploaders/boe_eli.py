"Boe eli store data to filesystem and update it to OpenSearch"
import httpx
import json
import asyncio
import xmltodict
from bs4 import BeautifulSoup


def is_eli_url(url: str):
    if not url.startswith("https://www.boe.es/eli/"):
        raise ValueError(
            f"URL must start with: 'https://www.boe.es/eli/' not {url}")


def is_day_url(url: str) -> bool:
    url_split = url.split("/")
    url_date = url_split[6:]
    return len(url_date) == 3


async def eli_urls(url: str) -> list[str]:
    is_eli_url(url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=3600)
    soup = BeautifulSoup(response.content, 'html.parser')

    urls = []
    class_name = "lista-eli"

    if is_day_url(url):
        class_name = "bullet"

    elements = soup.find_all(class_=class_name)
    urls = [element.find('a').get('href') for element in elements]

    return urls


def eli_path_to_url(path: str):
    return f"https://www.boe.es{path}"


def eli_paths_to_urls(paths: list[str]):
    return list(map(eli_path_to_url, paths))


async def get_all_eli_urls(url: str) -> list[str]:
    if is_day_url(url):
        return await eli_urls(url)
    else:
        all_urls = []
        urls = eli_paths_to_urls(await eli_urls(url))
        for x in urls:
            all_urls += await get_all_eli_urls(x)
        return all_urls


async def get_xmldata_from_eli_urls(urls: list[str]) -> list[dict]:
    data = []
    for index, url in enumerate(urls):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}/dof/spa/xml", timeout=3600)
            # print(response.text)
            res_xml_text = response.text
            res_dict = xmltodict.parse(res_xml_text)
            data.append({
                "_id": url.split("https://www.boe.es/")[-1],
                **res_dict
            })
            print(url.split("https://www.boe.es/")[-1])
            # print(json.dumps(res_dict,indent=2, ensure_ascii=False))
        if (index % 10 == 0):
            await asyncio.sleep(5)
    return data

async def get_htmldata_from_eli_urls(urls: list[str]) -> list[dict]:
    data = []
    for index, url in enumerate(urls):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}", timeout=3600)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")
            contenedor = soup.find("div", {"id": "textoxslt"})
            texto_extraido = ""

            for element in contenedor.find_all(['h4', 'h5', 'p']):
                texto_extraido += element.get_text() + "\n"
            data.append({
                "_id": url.split("https://www.boe.es/")[-1],
                "text": texto_extraido
            })
            # print(texto_extraido)
        if (index % 10 == 0):
            await asyncio.sleep(2)
            print(f"{index}/{len(urls)}")
    return data


if __name__ == "__main__":
    import sys
    sys.path.append("/home/vic/personal-ws/TFG/middleware")
    print(sys.path)
    from utils import index_docs

    async def fecth_all_data():
        tipos = ["c", "l", "lo"]
        years = range(1975, 2024)
        data = []
        for tipo in tipos:
            for year in years:
                data += await get_all_eli_urls(f"https://www.boe.es/eli/es/{tipo}/{year}")
                await asyncio.sleep(20)
                print(f"Year {year} loaded...")
        # To save the JSON data to a file, you can do the following:
        with open('data/eli_urls.json', 'w', encoding="utf-8") as file:
            json.dump(data, file)

    async def download_all_xmls():
        with open('data/eli_urls.json', 'r', encoding="utf-8") as file:
            urls = json.load(file)
        data = await get_xmldata_from_eli_urls(urls)
        # index_docs(data)
        with open('data/eli_data.json', 'w', encoding="utf-8") as file:
            json.dump(data, file)

    async def download_all_html():
        with open('data/eli_urls.json', 'r', encoding="utf-8") as file:
            urls = json.load(file)
        data = await get_htmldata_from_eli_urls(urls)
        # index_docs(data)
        with open('data/eli_data_html.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)

    # async def upload_to_opensearch():
    #     with open('data/eli_data.json', 'r', encoding="utf-8") as file:
    #         docs:list[dict] = json.load(file)

    #     def divide_list(arr: list, n: int):
    #         return [arr[i:i + n] for i in range(0, len(arr), n)]

    #     div_docs = divide_list(docs, 500)
    #     len_div_docs = len(div_docs)
    #     for i, div_doc in enumerate(div_docs):
    #         index_docs(div_doc)
    #         await asyncio.sleep(2)
    #         print(f"{i+1}/{len_div_docs} indexed.")

    async def main():
        # await fecth_all_data()
        # await download_all_xmls()
        await download_all_html()
        # await upload_to_opensearch()

    asyncio.run(main())
    # asyncio.run(upload_to_opensearch())
