import asyncio
import aiohttp
import aiofiles
import os
from bs4 import BeautifulSoup
import random
import requests
import re

UAList = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/84.0.4316.125",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/50.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36"
]

BASE_DIR = 'result/12_爬取小说《星辰变》/'
os.makedirs(BASE_DIR, exist_ok=True)

pattern = r'请收藏本站.*$'

async def download_one_page(session: aiohttp.ClientSession, url: str, title: str) -> None:
    try:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            content_div = soup.find('div', id='chaptercontent')

            # Replace <br> with newline character
            for br in content_div.find_all('br'):
                br.replace_with('\n')

            # Get cleaned content
            content = content_div.get_text()
            result = re.sub(pattern, '', content, flags=re.DOTALL)

            # Write to file
            async with aiofiles.open(os.path.join(BASE_DIR, title + '.txt'), 'w', encoding='utf-8') as f:
                await f.write(title + '\n\n')
                await f.write(result)

            print(f"Downloaded {title}")

    except aiohttp.ClientError as e:
        print(f"Aiohttp ClientError - Failed to download {title} from {url}: {e}")
    except Exception as e:
        print(f"Failed to download {title} from {url}: {e}")

async def main(url: str):
    try:
        # Fetching main page
        response = requests.get(url, headers={'User-Agent': random.choice(UAList)})
        main_page = BeautifulSoup(response.text, 'html.parser')

        # Extracting chapter list
        catalog = main_page.find('div', class_='listmain')
        page_list = catalog.find_all('dd')

        # Creating asynchronous session
        async with aiohttp.ClientSession(headers={'User-Agent': random.choice(UAList)}) as session:
            task_list = []
            for dd in page_list:
                dd_a = dd.find('a')
                title, page_href = dd_a.text, dd_a['href']
                page_href = url + page_href.split('/')[-1]

                # Create task for each chapter download
                task = asyncio.create_task(download_one_page(session, page_href, title))
                task_list.append(task)

            # Run tasks concurrently
            await asyncio.gather(*task_list)

    except requests.RequestException as e:
        print(f"Requests RequestException - Failed to fetch main page from {url}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    novel_url = 'https://www.bqgui.cc/book/486/'
    asyncio.run(main(novel_url))
    print('爬取完成')
