
import httpx
from bs4 import BeautifulSoup


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
            


if __name__ == "__main__":
    import asyncio
    async def  main():
        tipos = ["c", "l", "lo"]
        years = range(1975, 2024)
        for tipo in tipos:
            for year in years:
                print(await get_all_eli_urls(f"https://www.boe.es/eli/es/{tipo}/{year}"))

    asyncio.run(main())