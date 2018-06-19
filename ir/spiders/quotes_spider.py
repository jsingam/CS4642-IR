import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'yamu-places'
    i=10
    url='https://www.yamu.lk/place'
    start_urls=[]
    for page in range(1,i):
        u=url+("?page="+str(page))
        start_urls.append(u)

    def parse(self,response):
        def extract_with_css(query):
            return response.css(query).extract_first()
        for href in response.css('div.row div.col-md-4.col-sm-6 a.list-group-item::attr(href)'):
            yield response.follow(href, self.parse_place)








    def getText(self,text):
        if text==None:
            return text
        text=text.replace("\n","")
        return text.strip()

    def get_text_array(self,array):
        arr=[]
        for t in array:
            txt=self.getText(t)
            if not txt=="":
                arr.append(txt)
        return arr

    def parse_place(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()


        yield {
            'title':self.getText(extract_with_css("div.place-title-box h2::text")),
            'address': self.getText(extract_with_css("div.place-title-box p::text")),
            'contact':self.getText(extract_with_css("ul.place-title-list.list-inline li a.emph::text")),
            'rating':self.getText(extract_with_css("div.place-rating-box-item p a::text")),
            'abstract':self.getText(extract_with_css("div.place-title-box p.excerpt::text")),
            'reviewer': self.getText(extract_with_css("div.media-body.header-info-no-border.author-body div.pull-left a span::text")),     # 'birthdate': extract_with_css('.author-born-date::text'),
            "comments": self.get_text_array(response.css("div.media-body div.comment-decoration p.comment-text::text").extract()),
            "similar places": self.get_text_array(response.css("div.col-md-4.media.front-media strong.red::text").extract()),
            "topics on review": self.get_text_array(response.css('div.bodycopy h2::text').extract())
        }

        for href in response.css('div.row.topten a::attr(href)'):
            yield response.follow(href, self.parse_place)