# text_puppeteer.py

from crawlee import PuppeteerCrawler

class TextDataPuppeteerCrawler(PuppeteerCrawler):
    async def handle_page(self, page, response):
        # Extract all text from the current page
        page_text = await page.evaluate('''() => {
            return document.body.innerText;
        }''')

        # Save the extracted text data
        await self.push_data({
            'url': response.url,
            'text_content': page_text
        })

        # Follow all links on the page
        links = await page.$$eval('a', lambda elements: [element.href for element in elements])
        for link in links:
            await self.enqueue_request(link)

    async def parse(self, response):
        # You can add your Scrapy-like parsing logic here if needed
        pass

# Define your starting URLs
start_urls = [
    'https://wiki.tripsit.me/',
    'https://psychonautwiki.org/',
    'https://harmreduction.org/',
    'https://erowid.org/chemicals/dxm/faq/dxm_faq.shtml'
]

# Set up and run the Crawlee PuppeteerCrawler
async def run_crawler():
    crawler = TextDataPuppeteerCrawler()
    
    for url in start_urls:
        await crawler.enqueue_request(url)

    await crawler.run()

# Run the Crawlee PuppeteerCrawler
run_crawler()
