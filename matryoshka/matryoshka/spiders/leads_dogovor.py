import re
from urllib.parse import urlencode
from datetime import date, timedelta
import scrapy
from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess
import tokens


class LeadsSpider(scrapy.Spider):
    name = 'leads'
    allowed_domains = [tokens.ALLOWED_DOMAINS]
    start_urls = [tokens.START_URLS]

    def parse(self, response):
        formdata = {
            'password': tokens.MATR_PASS,
            'username': tokens.MATR_USERNAME
            }
        return FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.load_main_page
        )

    def load_main_page(self, response):
        today = date.today()
        delta = timedelta(days=15)
        daystart = (today - delta).strftime('%d/%m/%Y')
        params = {
            "limit": "300",
            "daystart": daystart,
            "status_code": 'Договор',
        }
        url = "http://best.matryoshki.info/?" + urlencode(params)
        yield scrapy.Request(url, self.scrape_page)

    def scrape_page(self, response):
        leads = response.xpath('//*[@id="work-table"]/table//tr[contains(@id, "order-id")]')

        for lead in leads:
            status = lead.xpath('td[8]/span[1]/text()').get()
            status = re.sub(r"\s+", " ", status).strip()
            source = lead.xpath('td[2]/text()').get()
            order_id = lead.xpath('td[1]/span[1]/text()').get()
            dates = lead.xpath('td[6]/text()').get()
            date = dates.split()[0]
            yield {
                'ID': order_id,
                'Статус': status,
                'Источник': source,
                'Регистрация заявки': date,
            }


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'leads.csv'
})

process.crawl(LeadsSpider)
process.start()
