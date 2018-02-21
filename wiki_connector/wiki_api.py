import asyncio
import json
import re
from typing import List, Dict

import aiohttp
from async_timeout import timeout

# How long the scraper will continue with the request
REQUEST_TIMEOUT = 10
# The API endpoint for getting the necessary data
API_FORMAT_STRING = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts|revisions&exintro=&explaintext=&titles={title}&redirects=1&rvprop=content&formatversion=2"
# Create one HTTP session for all requests - this might be really stupid
session = aiohttp.ClientSession()


class Page:
    def __init__(self, jsonb: Dict):
        """
        Create a Page from a MediaWiki API JSON blob.
        This will extract links in the order they appear, which the pip Wikipedia package cannot.
        :param jsonb: The JSON blob.
        """
        self.title = jsonb["title"]
        content = jsonb['revisions'][0]['content']
        self.links = self.extract_links(content)
        self.description = jsonb["extract"]

    def __str__(self):
        """
        String version of the Page.
        :return: String version of the Page.
        """
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


async def fetch_page(title: str) -> Page:
    """
    Asynchronously fetch a page.
    Uses asyncio and the async/await keywords - we should use it for this just to keep performance decent.
    :param title: The name of the page to fetch.
    :return: A Page.
    """
    global REQUEST_TIMEOUT, API_FORMAT_STRING, session
    async with timeout(10):
        response = await session.get(API_FORMAT_STRING.format(title=title))
        text = await response.text()
        blob = json.loads(text)
        blob = blob['query']['pages'][0]
        page = Page(blob)
        print(page)
        return page


# Get philosophy, and everything one link away.
# We might want to reduce the number of links we follow.
loop = asyncio.get_event_loop()
page1 = loop.run_until_complete(fetch_page("Philosophy"))
for link in page1.links:
    loop.create_task(fetch_page(link))
loop.run_forever()