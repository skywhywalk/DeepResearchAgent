import os
from typing import Optional
from dotenv import load_dotenv
load_dotenv(verbose=True)

from markitdown._base_converter import DocumentConverterResult
from crawl4ai import AsyncWebCrawler
from firecrawl import FirecrawlApp,ScrapeOptions

async def firecrawl_fetch_url(url: str):
    try:
        app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY", None))

        response = app.crawl_url(
            url,
            limit=1,
            scrape_options=ScrapeOptions(formats=['markdown', 'html']),
        )

        result = response.data[0].markdown

        return result
    except Exception as e:
        return None

async def fetch_crawl4ai_url(url: str):
    """Fetch content from a given URL using the crawl4ai library."""
    try:
        async with AsyncWebCrawler() as crawler:
            response = await crawler.arun(
                url=url,
            )

            if response:
                result = response.markdown
                return result
            else:
                return None
    except Exception as e:
        return None

async def fetch_url(url: str) -> Optional[DocumentConverterResult]:
    try:
        firecrawl_result = await firecrawl_fetch_url(url)

        if firecrawl_result:
            return DocumentConverterResult(
                markdown=firecrawl_result,
                title=f"Fetched content from {url}",
            )

        crawl4ai_result = await fetch_crawl4ai_url(url)
        if crawl4ai_result:
            return DocumentConverterResult(
                markdown=crawl4ai_result,
                title=f"Fetched content from {url}",
            )

    except Exception as e:
        return None