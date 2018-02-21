from typing import List, Dict
import aiohttp
import asyncio
import re
from async_timeout import timeout
import json

REQUEST_TIMEOUT = 10
API_FORMAT_STRING = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts|revisions&exintro=&explaintext=&titles={title}&redirects=1&rvprop=content&formatversion=2"
# Create one HTTP session for all requests - may change this later
session = aiohttp.ClientSession()


class Page:
    def __init__(self, jsonb: Dict[str, str]):
        self.title = jsonb["title"]
        content = jsonb['revisions'][0]['content']
        self.links = self.extract_links(content)
        self.description = jsonb["extract"]

    def __str__(self):
        return f"{self.title}\n{self.description}\n({len(self.links)} links)"

    @staticmethod
    def extract_links(text: str) -> List[str]:
        all_links = re.findall("\[\[[A-Za-z0-9^|]+\]\] | \[\[[A-Za-z0-9]+\]\]", text, 0)
        def clean_link(link:str):
            link = link.replace("[", "").replace("]", "")
            if len(link.split("|")) == 2:
                link = link.split("|")[1]
            return link
        all_links = [clean_link(x) for x in all_links]
        return all_links

    @staticmethod
    def extract_description(text: str):
        matches = re.search("\\n\\n[^(\\n\\n)]+?\\n\\n", text, 0)
        return matches


async def fetch_page(title: str) -> Page:
    global REQUEST_TIMEOUT, API_FORMAT_STRING, session
    async with timeout(10):
        response = await session.get(API_FORMAT_STRING.format(title=title))
        text = await response.text()
        blob = json.loads(text)
        blob = blob['query']['pages'][0]
        page = Page(blob)
        print(page)
        return page


loop = asyncio.get_event_loop()
page1 = loop.run_until_complete(fetch_page("Philosophy"))
for link in page1.links:
    loop.create_task(fetch_page(link))
loop.run_forever()