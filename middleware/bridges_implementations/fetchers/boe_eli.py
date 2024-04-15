import httpx
import json
import asyncio
import xmltodict
from bs4 import BeautifulSoup
from bridges import Fetcher


def is_eli_url(url:str):
    if not url.startswith("https://www.boe.es/eli/"):
        raise ValueError(f"URL must start with: 'https://www.boe.es/eli/' not {url}")

def is_day_url(url:str) -> bool:
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
    

async def get_data_from_eli_urls(urls: list[str]) -> list[dict]:
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
        if(index%10 == 0):
            await asyncio.sleep(5)
    return data

class BoeEli(Fetcher[dict, str]):
    "Fetch raw-data from the database of BOE, the official law Spanish Documents"
    
    def __init__(self) -> None:
        super().__init__("boe_eli")

    async def fetch_data(self, place: str, **args):
        pass
        # data = await get_data_from_eli_urls(urls)


if __name__ == "__main__":
    import sys
    sys.path.append("/home/vic/personal-ws/TFG/middleware")
    print(sys.path)
    from utils import index_docs
    async def  fecth_all_data():
        tipos = ["c", "l", "lo"]
        years = range(1975, 2024)
        data = []
        for tipo in tipos:
            for year in years:
                data+=await get_all_eli_urls(f"https://www.boe.es/eli/es/{tipo}/{year}")
                await asyncio.sleep(20)
                print(f"Year {year} loaded...")
        # To save the JSON data to a file, you can do the following:
        with open('data/eli_urls.json', 'w', encoding="utf-8") as file:
            json.dump(data, file)
    async def download_all_xmls():
        with open('data/eli_urls.json', 'r', encoding="utf-8") as file:
            urls = json.load(file)
        data = await get_data_from_eli_urls(urls)
        # index_docs(data)
        with open('data/eli_data.json', 'w', encoding="utf-8") as file:
            json.dump(data, file)

    # asyncio.run(fecth_all_data()) 
    asyncio.run(download_all_xmls()) 