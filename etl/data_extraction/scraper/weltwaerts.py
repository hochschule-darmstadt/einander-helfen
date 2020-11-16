import scrapy
from scrapy.crawler import CrawlerProcess



class crawler(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['weltwaerts.de']
    start_urls = ['https://www.weltwaerts.de/de/ep-ergebnis.html']



    def parse(self, response):
        hrefs = response.xpath("//h3/a[1]/@href")
        for href in hrefs:
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_contents)
    
        next_page_url = response.xpath("//li[@class='next']//a/@href").extract_first()
        if next_page_url:
            url = response.urljoin(next_page_url)
            yield scrapy.Request(url)
            
    def parse_contents(self, response):
        Ids = response.xpath("//div[@class='parameter__box']")
        for Id in Ids:
            nr = Id.xpath(
                ".//li[4]/span/text()").extract()
            
        headlines = response.xpath("//div[@class='parameter__box']/div")
        for headline in headlines:
            hl = headline.xpath(
                ".//h1/text()").extract_first()
        
        locations = response.xpath("//div[@class='parameter__box']")
        for location in locations:
            loc = location.xpath(
                ".//li[1]/span/text()").extract()
        
        tasks = response.xpath("//div[2][@class='text-block']")
        for task in tasks:
            tk = task.xpath(
                ".//p/text()").extract()
       
        times = response.xpath("//div[@class='parameter__box']")
        for time in times:
            tm = time.xpath(
                ".//li[3]/span/text()").extract()
            
        organizations = response.xpath("//div[4][@class='text-block']")
        for organization in organizations:
            orga = organization.xpath(
                ".//p[1]/text()").extract()
            
        yield {'id': nr,'title': hl, 'Location': loc, 'task': tk, 'timing': tm, 'organization': orga}
            

def runCrawler(name):
    c = CrawlerProcess({
        'USER_AGENT': 'HochschuleDarmstadt-MasterProjekt',
        'FEED_FORMAT': 'csv',
        'FEED_URI': name+'.csv',
        'ROBOTSTXT_OBEY': True,
        'HTTPCACHE_ENABLED': True

    })
    c.crawl(eval(name))
    c.start() # the script will block here until the crawling is finished


runCrawler('crawler')