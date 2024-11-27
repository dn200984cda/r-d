import scrapy


class Q7Spider(scrapy.Spider):
    name = "q7"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    current = 0
    max_page = 1

    def parse(self, response):
        #quote //div[contains(@class, 'quote')]/span[contains(@class, 'text')]
            # //div[contains(@class, 'quote')]/span[contains(@class, 'text')]/text()
        #author //div[contains(@class, 'quote')]//small[contains(@class, 'author')]
        quotes = response.xpath("//div[contains(@class, 'quote')]")

        for qoute in quotes:
            txt = qoute.xpath("./span[contains(@class,'text')]/text()").get()
            author = qoute.xpath(".//small[contains(@class,'author')]/text()").get()
            yield {
                "text": txt,
                "author": author
            }

        next_page = response.xpath("//li/a/@href").get()
        if next_page is not None and self.current < self.max_page:
            self.current += 1
            yield response.follow(next_page, callback=self.parse)