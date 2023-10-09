import scrapy

class CategorySpider(scrapy.Spider):
    name = 'category'
    start_urls = ['https://www.goldonecomputer.com/']

    def parse(self,response):

        #getting all category links
        #1-get links
        category_links = response.xpath('//div[@class="box-content"]/ul[@id="nav-one"]/li/a/@href').extract()
        
        #Check if have links
        if category_links :
            #go to link
            for category_link in category_links :
                yield response.follow(category_link, callback=self.parse_product_links)
        else:
            self.log("Category Links Not found")

    def parse_product_links(self,response):

        #getting product links
        product_links = response.xpath('//div[@class="product-block-inner"]//div[@class="product-details"]//div[@class="caption"]/h4/a/@href').extract()

        #following product links
        if product_links:
            for product_link in product_links:
                #url joining
                abs_product_link = response.urljoin(product_link)
                product = response.follow(abs_product_link, callback = self.parse_products)
                yield product
        else:
            self.log("Product Links not found")


    def parse_products(self,response):
        
        #getting product information
        product_content = response.xpath('//div[@id="content"]//div[@class="caption"]//h4//a/text()').extract()
        product_brand = response.xpath('//div[@id="content"]//ul[@class="list-unstyled"]//li[1]/a/text()')[0].extract()
        product_code = response.xpath('//div[@id="content"]//ul[@class="list-unstyled"]//li[2]/text()')[0].extract()
        product_price = response.xpath('//div[@id="content"]//ul[@class="list-unstyled price"]/li/h3/text()')[0].extract()
        product_review = response.xpath('//ul[@class="nav nav-tabs"]//li[2]/a/text()')[0].extract().split()
        product_image = response.xpath('//div[@id="content"]//div[@class="col-sm-6 product-left"]//div[@class="product-info"]//div[@class="left product-image thumbnails"]//div[@class="image"]/a[@class="thumbnail"]/@href')[0].extract()

        #Storing as json format
        product_detail = {
            'Brand' : product_brand,
            'Code' : product_code,
            'Price' : product_price,
            'Review Count' : product_review[1],
            'Image' : product_image
        }
        
        yield product_detail

    







