from shop.crawler.crawler import crawl_category


def importer(request):
    crawl_category("category-electronic-devices")