import scrapy


class DivanSpider(scrapy.Spider):
    name = "divan"  # Имя паука
    allowed_domains = ["divan.ru"]  # Домен, который мы парсим
    start_urls = ["https://www.divan.ru/category/divany"]  # URL категории диванов

    def parse(self, response):
        # Находим все карточки товаров
        products = response.css("div.catalog-product-card")
        for product in products:
            yield {
                "name": product.css("a.catalog-product-card__title::text").get().strip(),  # Название дивана
                "price": product.css("span.catalog-product-card__price::text").get().strip(),  # Цена
                "link": response.urljoin(product.css("a.catalog-product-card__title::attr(href)").get()),  # Ссылка на товар
            }

        # Пагинация: переходим на следующую страницу, если есть
        next_page = response.css("a.pagination__next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
